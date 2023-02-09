import requests
from flask import Flask, redirect, request, make_response, jsonify
from flask_restx import Resource, Api, Namespace

rent = Namespace('rent')

@rent.route("/list")
class RentList(Resource):
    def get(self):
        data = [
            {
                "id": 1,
                "deadline": "2022-11-01",
                "d_day": 50,
                "rent_day": "2022-09-10",
                "product": {
                    "id": 60,
                    "is_available": False,
                    "name": "테스트 물품",
                    "category": "도서", # String,
                    "location": "A-123", # String,
                    "status": "대여중", # String,
                    "author": "김판큐", # String?,
                    "publisher": "판큐출판사", # String?
                },
            },
            {
                "id": 2,
                "deadline": "2022-11-01",
                "d_day": 50,
                "rent_day": "2022-09-10",
                "product": {
                    "id": 60,
                    "is_available": False,
                    "name": "테스트 물품",
                    "category": "도서", # String,
                    "location": "A-123", # String,
                    "status": "대여중", # String,
                    "author": "김판큐", # String?,
                    "publisher": "판큐출판사", # String?
                },
            },
            {
                "id": 3,
                "deadline": "2022-11-01",
                "d_day": 50,
                "rent_day": "2022-09-10",
                "product": {
                    "id": 60,
                    "is_available": False,
                    "name": "테스트 물품",
                    "category": "도서", # String,
                    "location": "A-123", # String,
                    "status": "대여중", # String,
                    "author": "김판큐", # String?,
                    "publisher": "판큐출판사", # String?
                },
            },
        ]
        return data

@rent.route("/<int:rent_id>")
class RentProduct(Resource):
    def get(self, rent_id):
        data1 = {
            "id": 1,
            "deadline": "2022-11-01",
            "d_day": 50,
            "rent_day": "2022-09-10",
            "product": {
                "id": 60,
                "is_available": False,
                "name": "테스트 도서_이용불가",
                "category": "도서", # String,
                "location": "A-123", # String,
                "status": "대여중", # String,
                "author": "김판큐", # String?,
                "publisher": "판큐출판사", # String?
            },
        }
        data2 = {
            "id": 1,
            "deadline": "2022-11-01",
            "d_day": 50,
            "rent_day": "2022-09-10",
            "product": {
                "id": 60,
                "is_available": True,
                "name": "테스트 물품_이용가능",
                "category": "타블렛", # String,
                "location": "A-123", # String,
                "status": "대여 가능", # String,
                "author": None, # String?,
                "publisher": None, # String?
            },
        }
        if rent_id == 1:
            return data1
        else:
            return data2

    def put(self, rent_id):
        if rent_id == 'book_84523':
            return make_response(jsonify({}), status=200)
        else:
            return make_response(jsonify({'reason': '해당 도서를 찾을 수 없어요 :('}), status=404)

@rent.route("/list/<string:product_name>")
class ProductList(Resource):
    def get(self, product_name):
        data = [
            {
            "id": 1, # int
            "deadline": "2022-11-01", # Date?
            "d_day": 50, # int?
            "rent_day": "2022-09-10", # Date?
            "product": {
                "id": 60,
                "is_available": False,
                "name": product_name,
                "category": "도서", # String,
                "location": "A-123", # String,
                "status": "대여중", # String,
                "author": "김판큐", # String?,
                "publisher": "판큐출판사", # String?
                },
            },
            {
                "id": 2,
                "deadline": "2022-11-01",
                "d_day": 50,
                "rent_day": "2022-09-10",
                "product": {
                    "id": 60,
                    "is_available": False,
                    "name": "테스트 물품",
                    "category": "도서", # String,
                    "location": "A-123", # String,
                    "status": "대여중", # String,
                    "author": "김판큐", # String?,
                    "publisher": "판큐출판사", # String?
                },
            },
            {
                "id": 3,
                "deadline": "2022-11-01",
                "d_day": 50,
                "rent_day": "2022-09-10",
                "product": {
                    "id": 60,
                    "is_available": False,
                    "name": "테스트 물품",
                    "category": "도서", # String,
                    "location": "A-123", # String,
                    "status": "대여중", # String,
                    "author": "김판큐", # String?,
                    "publisher": "판큐출판사", # String?
                },
            },
        ]
        return data