from flask_restx import Resource, Namespace
from flask import jsonify
from database.database import Database
from datetime import datetime, timedelta

admin_product = Namespace('admin_product')

def DateChangetoString(list, item):
    for idx, lst in enumerate(list):
        list[idx][item] = lst[item].strftime('%Y-%m-%d')
@admin_product.route("/all")
class ProductList(Resource):
    def get(self):
        database = Database()
        #left join으로 대여중인 물품은 대여 정보까지 함께 가져오도록 함
        sql = f"SELECT * FROM products AS p LEFT JOIN rent_list AS r ON p.code = r.product_code;"
        product_list = database.execute_all(sql)
        database.close()

        #json으로 전송하기 위해 python 클래스로 저장된 날짜 정보를 문자열로 변환
        DateChangetoString(product_list,'deadline')
        DateChangetoString(product_list, 'rent_day')


        if not product_list:
            message = { 'message': '물품이 존재하지 않습니다.' }
            return message, 400
        else:
            return product_list, 200


@admin_product.route("/list/<string:product_name>")
class SearchProductList(Resource):
    def get(self, product_name):
        database = Database()
        print(product_name)
        #left join으로 대여중인 물품은 대여 정보까지 함께 가져오도록 함
        sql = (f"SELECT * FROM products AS p LEFT JOIN rent_list AS r ON p.code = r.product_code"\
               f" WHERE name LIKE '%%{product_name}%%'")
        product_list = database.execute_all(sql)
        database.close()

        # json으로 전송하기 위해 python 클래스로 저장된 날짜 정보를 문자열로 변환
        DateChangetoString(product_list, 'deadline')
        DateChangetoString(product_list, 'rent_day')
        print(product_list)
        if not product_list:
            message = {'message': '해당 물품이 존재하지 않습니다.'}
            return message, 400
        else:
            return product_list, 200