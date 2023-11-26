from flask_restx import Resource, Namespace, fields
from flask import jsonify
from database.database import Database
from datetime import datetime, timedelta
from utils.dto import AdminProductDTO

product = AdminProductDTO.api
_admin_product_all = AdminProductDTO.admin_product_response_all
_admin_product_internal  =AdminProductDTO.internal_error
_admin_product_not_found = AdminProductDTO.no_product_find

def date_change_to_string(list, item):
    for idx, lst in enumerate(list):
        if lst[item]:
            list[idx][item] = lst[item].strftime('%Y-%m-%d')

@product.route("/list")
@product.response(200, 'Success', _admin_product_all)
@product.response(400, 'Bad Request', _admin_product_not_found)
@product.response(500, 'Internal Server Error', _admin_product_internal)
class ProductList(Resource):
    def get(self):
        # 전체 물품의 목록을 가져옵니다. 대여중인 물품은 대여 정보도 같이 가져옵니다.
        database = Database()
        # left join으로 대여중인 물품은 대여 정보까지 함께 가져오도록 함
        sql = f"SELECT * FROM products AS p LEFT JOIN rent_list AS r ON p.code = r.product_code;"
        product_list = database.execute_all(sql)
        database.close()

        # json으로 전송하기 위해 python 클래스로 저장된 날짜 정보를 문자열로 변환
        date_change_to_string(product_list, 'deadline')
        date_change_to_string(product_list, 'rent_day')

        if not product_list: # 대여할 물품이 존재하지 않을 경우 예외처리
            message = {'message': '물품이 존재하지 않아요.'}
            return message, 400
        else:
            return product_list, 200

@product.response(200, 'Success', _admin_product_all)
@product.response(400, 'Bad Request', _admin_product_not_found)
@product.response(500, 'Internal Server Error', _admin_product_internal)
@product.route("/list/<string:product_name>")
class SearchProductList(Resource):
    def get(self, product_name):
        # 특정물품의 검색 결과를 가져옵니다. 대여중인 물품은 대여 정보도 같이 가져옵니다.
        database = Database()
        # left join으로 대여중인 물품은 대여 정보까지 함께 가져오도록 함
        sql = (f"SELECT * FROM products AS p LEFT JOIN rent_list AS r ON p.code = r.product_code"\
               f" WHERE name LIKE '%%{product_name}%%'")
        product_list = database.execute_all(sql)
        database.close()

        # json으로 전송하기 위해 python 클래스로 저장된 날짜 정보를 문자열로 변환
        date_change_to_string(product_list, 'deadline')
        date_change_to_string(product_list, 'rent_day')

        if not product_list:
            message = {'message': '해당 물품이 존재하지 않아요'}
            return message, 400
        else:
            return product_list, 200