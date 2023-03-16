from flask import Flask, request, make_response, jsonify
from flask_restx import Resource, Namespace
from database.database import Database
from datetime import datetime, timedelta

product = Namespace('product')

@product.route("/<string:product_code>")
class Product(Resource):
    def get(self, product_code):
        database = Database()
        sql = f"SELECT * FROM products where code = {product_code};"
        product = database.execute_one(sql)
        database.close()
        
        if not product:     # 물품이 없을 때의 처리
            message = { 'message': '해당 물품이 존재하지 않아요 :(' }
            return message, 400
        else:
            return product, 200

@product.route("/list")
class ProductList(Resource):
    def get(self):
        database = Database()
        sql = f"SELECT * FROM products;"
        product_list = database.execute_all(sql)
        database.close()
        
        if not product_list:
            message = { 'message': '물품이 존재하지 않아요 :(' }
            return message, 400
        else:
            return product_list, 200

@product.route("/list/<string:product_name>")
class SpecificProductList(Resource):
    def get(self, product_name):
        database = Database()
        sql = f"SELECT * FROM products where name = {product_name};"
        product_list = database.execute_all(sql)
        database.close()
        
        if not product_list:
            message = { 'message': '해당 물품이 존재하지 않아요 :(' }
            return message, 400
        else:
            return product_list, 200

@product.route("/rent/<string:product_code>")
class RentProduct(Resource):
    def post(self, product_code):
        database = Database()
        sql = f"SELECT * FROM products WHERE code = '{product_code}';"
        product = database.execute_one(sql)
        user_id_temp = 2
        
        if product['is_available']: # 물품 대여에 대한 로직
            # 물품 정보를 대여중인 상태로 업데이트
            status = "대여중"
            sql = f"UPDATE products SET is_available = {0}, status = '{status}' WHERE code = '{product_code}';"
            database.execute(sql)
            database.commit()

            # 물품 대여 내역 추가
            now = datetime.now()
            rent_day = now.date()
            deadline = rent_day + timedelta(days=30)
            sql = f"INSERT INTO rent_list(product_code, user_id, deadline, rent_day, return_day) "\
                f"VALUES('{product_code}', {user_id_temp}, '{deadline}', '{rent_day}', NULL);"
            database.execute(sql)
            database.commit()

            # 물품 정보가 변경 되었으므로 물품 상세 정보 재조회
            sql = f"SELECT * FROM products WHERE code = '{product_code}';"
            product_data = database.execute_one(sql)

            # 빌린 사람 이름 조회
            sql = f"SELECT name FROM users WHERE id = {user_id_temp}"
            rent_user = database.execute_one(sql)

            # 디데이 계산
            d_day = (deadline - rent_day).days

            # 물품 정보에 대여 관련 정보 추가
            product_data['deadline'] = deadline.strftime('%Y/%m/%d')
            product_data['rent_day'] = rent_day.strftime('%Y/%m/%d')
            product_data['d_day'] = d_day
            product_data['return_day'] = None
            product_data['status'] = { 'value': status, 'rent_user': rent_user['name'] }

            database.close()
            return product_data, 200
        else:
            database.close()
            message = {}
            if not product:
                message['message'] = '등록되지 않은 물품이에요 :('
                message['value'] = 0
            elif product['status'] == "대여중":
                message["message"] = '현재 대여중인 물품이에요 :('
                message['value'] = 1
            else:
                message['message'] = "현재 대여 불가능한 물품이에요 :("
                message['value'] = 2
            return message, 400

@product.route("/return/<string:product_code>")
class ReturnProduct(Resource):
    def put(self, product_code):
        database = Database()
        sql = f"SELECT * FROM products WHERE code = '{product_code}';"
        product = database.execute_one(sql)

        # JWT 적용 전 임시 user_id 값
        user_id = 2

        # 물품 반납에 대한 로직
        if not product['is_available']:
            if product['status'] == "대여중":
                # 맞는 대여 내역이 있는지 검증 
                sql = f"SELECT * FROM rent_list "\
                    f"WHERE product_code = '{product_code}' and user_id = {user_id} and return_day is null;"
                rent_data = database.execute_one(sql)
                if not rent_data:
                    return { 'message': '데이터가 올바르지 않아요 :(\n지속적으로 발생 시 문의해주세요!' }, 500
                
                # 물품 대여 내역에 반납일자 반영
                now = datetime.now()
                return_day = now.date()
                status = "대여 가능"
                sql = f"UPDATE rent_list SET return_day = '{return_day}' "\
                    f"WHERE product_code = '{product_code}' and user_id = {user_id} and return_day is null;"
                database.execute(sql)
                database.commit()

                # 물품 정보 수정
                sql = f"UPDATE products SET is_available = {1}, status = '{status}' WHERE code = '{product_code}';"
                database.execute(sql)
                database.commit()

                # 물품 정보가 변경 되었으므로 물품 상세 정보 재조회
                sql = f"SELECT * FROM products WHERE code = '{product_code}';"
                product_data = database.execute_one(sql)

                # 물품 정보에 대여 관련 정보 추가
                product_data['deadline'] = rent_data['deadline'].strftime('%Y/%m/%d')
                product_data['rent_day'] = rent_data['rent_day'].strftime('%Y/%m/%d')
                product_data['d_day'] = None
                product_data['return_day'] = return_day.strftime('%Y/%m/%d')
                product_data['status'] = { 'value': status, 'rent_user': None }

                database.close()

                return product_data, 200    
            else:
                database.close()
                return { 'message': '반납을 할 수 없는 물품이에요 :(' }, 400
        else:
            # 대여 가능한 경우
            database.close()
            return { 'message': '대여 중인 물품만 반납할 수 있어요 :(' }, 400
