from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database

WARNING_CATEGORY = {-2: '경고 차감', -1: '주의 차감', 1: '주의 부여', 2: '경고 부여', 0: '경고 초기화'}

warning_status = Namespace('warning_status')

@warning_status.route('/<int:user_id>')
class WarningStatusUserAPI(Resource):
    # 회원의 경고 현황 반환
    def get(self, user_id):
        # 데이터베이스에서 user_id값에 맞는 경고 목록 불러오기
        database = Database()
        sql = f"select * from warning_status where user_id = {user_id}"
        warning_status_list = database.execute_all(sql)
        database.close()

        if not warning_status_list: # 경고를 받은 적이 없을 때 처리
            return [], 200
        else:
            for idx, warning_status in enumerate(warning_status_list):
                # 날짜를 문자열로 변경
                warning_status_list[idx]['date'] = warning_status['date'].strftime('%Y-%m-%d')
                # 종류를 문자열로 매핑
                warning_status_list[idx]['category'] = WARNING_CATEGORY[warning_status['category']]
            return warning_status_list, 200
    
    # 회원에 대한 경고 추가
    def post(self, user_id):
        # Body 데이터 읽어오기
        warning_status = request.get_json()
        # user_id 추가
        warning_status['user_id'] = user_id
        # 종류를 int로 매핑
        for key, value in WARNING_CATEGORY.items():
            if value == warning_status['category']:
                warning_status['category'] = key
                break

        # 데이터베이스에 추가
        database = Database()
        sql = f"insert into warning_status ({', '.join(warning_status.keys())}) VALUES ({', '.join(warning_status.values())})"
        database.execute()
        database.commit()
        database.close()

        return warning_status, 200

@warning_status.route('/<int:warning_status_id>/modify')
class WarningStatusEditAPI(Resource):
    # 경고 현황 수정
    def put(self, warning_status_id):
        warning_status = request.get_json()
        pass

    # 경고 현황 삭제
    def delete(self, warning_status_id):
        warning_status = request.get_json()
        pass