from flask_restx import Resource, Namespace, fields
from flask import jsonify
from database.database import Database
from datetime import datetime, timedelta
from utils import adminProductDTO

def DateChangetoString(list, item):
    for idx, lst in enumerate(list):
        if lst[item]:
            list[idx][item] = lst[item].strftime('%Y-%m-%d')

admin_product = adminProductDTO.api
_admin_product_all = adminProductDTO.admin_product_response_all
_admin_product_internal  =adminProductDTO.internal_error
_admin_product_not_found = adminProductDTO.no_product_find
@admin_product.route("/all")
@admin_product.response(200,'Success',_admin_product_all)
@admin_product.response(400,'Bad Request',_admin_product_not_found)
@admin_product.response(500,'Internal Server Error',_admin_product_internal)
class ProductList(Resource):
    def get(self):
        """전체 물품의 목록을 가져옵니다. 대여중인 물품은 대여 정보도 같이 가져옵니다."""
        database = Database()
        #left join으로 대여중인 물품은 대여 정보까지 함께 가져오도록 함
        sql = f"SELECT * FROM products AS p LEFT JOIN rent_list AS r ON p.code = r.product_code;"
        product_list = database.execute_all(sql)
        print(product_list)
        database.close()


        #json으로 전송하기 위해 python 클래스로 저장된 날짜 정보를 문자열로 변환
        try:
            DateChangetoString(product_list, 'deadline')
            DateChangetoString(product_list, 'rent_day')
        except (AttributeError, TypeError) as e:
            print(f'에러가 발생했습니다:{e}')

        if not product_list: #대여할 물품이 존재하지 않을 경우 예외처리
            message = {'message': '물품이 존재하지 않습니다.'}
            return message, 400
        else:
            return product_list, 200

@admin_product.response(200,'Success',_admin_product_all)
@admin_product.response(400,'Bad Request',_admin_product_not_found)
@admin_product.response(500,'Internal Server Error',_admin_product_internal)
@admin_product.route("/list/<string:product_name>")
class SearchProductList(Resource):
    def get(self, product_name):
        """특정물품의 검색 결과를 가져옵니다. 대여중인 물품은 대여 정보도 같이 가져옵니다."""
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