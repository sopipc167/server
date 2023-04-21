from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database

warning_status = Namespace('warning_status')

@warning_status.route('/<int:user_id>')
class WarningStatusUserAPI(Resource):
    def get(self, user_id):
        # 데이터베이스에서 user_id값에 맞는 경고 목록 불러오기
        database = Database()
        sql = f"select * from warning_status where user_id = {user_id}"
        warning_status_list = database.execute_all(sql)

        if not warning_status_list: # 경고를 받은 적이 없을 때 처리
            database.close()
            return [], 200
        else:
            for idx, warning_status in enumerate(warning_status_list):
                # 날짜를 문자열로 변경
                warning_status_list[idx]['date'] = warning_status['date'].strftime('%Y-%m-%d')
            return warning_status_list, 200