from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database
from datetime import datetime, date

attendance = Namespace('attendance')

attendance.route('')
class AttendanceUserAPI(Resource):
    def get(self):
        pass

    def post(self):
        pass