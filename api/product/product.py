from flask import Flask, request, make_response, jsonify
from flask_restx import Resource, Namespace
from database.database import Database

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
'''
# 구현중
@product.route("/rent/<string:product_code>")
class RentProduct(Resource):
    def put(self, product_code):
        database = Database()
        sql = f"SELECT * FROM products where code = {product_code}"
        product = database.execute_one(sql)
        
        if product['is_available']:
            # 물품에 대한 내용
            sql = f"UPDATE products SET is_available = {False} WHERE code = {product_code};"
            database.execute(sql)
            
            # 반납 기한, 디데이, 대여한 날짜 설정
            sql = f"UPDATE rent_list SET is_available = {False} WHERE code = {product_code};"
            database.close()
            return {}, 200
        else:
            database.close()
            message = { 'message': '현재 대여가 불가능한 물품이에요 :(' }
            return message, 400
'''
