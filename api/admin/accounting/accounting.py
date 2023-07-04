from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database
from datetime import datetime, date

accounting = Namespace('accounting')

@accounting.route('/')
class HelloWorld(Resource):
    def get(self):
        return {"hello": "world!"}