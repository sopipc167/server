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

# 구현중
@product.route("/rent/<string:product_code>")
class RentProduct(Resource):
    def post(self, product_code):
        database = Database()
        sql = f"SELECT * FROM products where code = {product_code}"
        product = database.execute_one(sql)
        
        if product['is_available']: # 물품 대여에 대한 로직
            # 물품 정보를 대여중인 상태로 업데이트
            status = "대여중"
            sql = f"UPDATE products SET is_available = {False}, status = {status} WHERE code = {product_code};"
            database.execute(sql)
            
            # 물품 대여 내역 추가
            now = datetime.now()
            rent_day = now.date()
            deadline = rent_day + timedelta(30)
            status_value = 0
            sql = f"INSERT INTO rent_list VALUES({product_code}, {1}, {deadline}, {rent_day}, {status_value});"
            database.execute(sql)

            # 물품 정보가 변경 되었으므로 물품 상세 정보 재조회
            sql = f"SELECT * FROM products where code = {product_code};"
            product_data = database.execute_one(sql)

            # 빌린 사람 이름 조회
            sql = f"SELECT name FROM users where id = {2}"
            rent_user = database.execute_one(sql)

            # 디데이 계산
            d_day = (deadline - rent_day).days

            # 물품 정보에 대여 관련 정보 추가
            product_data['deadline'] = deadline.strftime('%Y/%m/%d')
            product_data['rent_day'] = rent_day.strftime('%Y/%m/%d')
            product_data['d_day'] = d_day
            product_data['status'] = { 'value': '대여중', 'rent_user': rent_user['name'] }

            database.close()
            return product_data, 200
        else:
            database.close()
            message = { 'message': '현재 대여가 불가능한 물품이에요 :(' }
            return message, 400

@product.route("/return/<string:product_code>")
class ReturnProduct(Resource):
    def get(self, product_code):
        return {}, 200