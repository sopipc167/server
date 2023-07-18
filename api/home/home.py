from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database
from datetime import datetime, date

home = Namespace('home')

@home.route('/attendance')
class HomeAttendanceAPI(Resource):
    def get(self):
        pass

@home.route('/schedule')
class HomeScheduleAPI(Resource):
    def get(self):
        pass

@home.route('/product')
class HomeProductAPI(Resource):
    def get(self):
        pass