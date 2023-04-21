from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database

seminar = Namespace('seminar')

@seminar.route('/<int:user_id>')
class SeminarUserAPI(Resource):
    def get(self, user_id):
        # 데이터베이스에서 user_id값에 맞는 세미나 목록 불러오기
        database = Database()
        sql = f"select * from seminars where user_id = {user_id}"
        seminar_list = database.execute_all(sql)

        if not seminar_list: # 세미나를 한 적이 없을 때 처리
            database.close()
            return [], 200
        else:
            for idx, seminar in enumerate(seminar_list):
                # 날짜를 문자열로 변경
                seminar_list[idx]['date'] = seminar['date'].strftime('%Y-%m-%d')
            return seminar_list, 200