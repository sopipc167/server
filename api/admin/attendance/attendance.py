from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database
#from datetime import datetime, date

attendance = Namespace('attendance')

# 출석 category
ATTENDANCE_CATEGORY = {0: '정기 회의', 1: '디자인 파트 회의', 2: '아트 파트 회의', 3: '프로그래밍 파트 회의', 4: '기타'}

# index 데이터를 문자열로 변경
def convert_to_string(dictionary, index):
    return dictionary.get(index, None)

# 문자열 데이터를 index로 변경
def convert_to_index(dictionary, string):
    for key, value in dictionary.items():
        if value == string:
            return key
    return None

@attendance.route("/category/<int:category>")
class AttendanceInfoAPI(Resource):
    # category, date에 따른 출석 정보 얻기
    def get(self, category):
        # Body 데이터 읽어오기
        date = request.get_json()['date']

        # DB에서 category, date값에 맞는 출석 정보 가져오기
        database = Database()
        sql = f"SELECT * FROM attendance WHERE category = {category} and date = '{date}';"
        attendance = database.execute_one(sql)
        database.close()

        # 출석 정보가 존재할 때 처리
        if attendance:
            # category, date, time을 문자열로 변환
            attendance['category'] = convert_to_string(ATTENDANCE_CATEGORY, attendance['category'])
            attendance['date'] = attendance['date'].strftime('%Y-%m-%d')
            attendance['first_auth_start_time'] = str(attendance['first_auth_start_time'])
            attendance['first_auth_end_time'] = str(attendance['first_auth_end_time'])
            attendance['second_auth_start_time'] = str(attendance['second_auth_start_time'])
            attendance['second_auth_end_time'] = str(attendance['second_auth_end_time'])

        return attendance, 200

    # 출석 정보 추가
    def post(self, category):
        # Body 데이터 읽어오기
        attendance = request.get_json()

        # category를 index로 변환
        attendance['category'] = convert_to_index(ATTENDANCE_CATEGORY, attendance['category'])

        # 출석 정보를 DB에 추가
        database = Database()
        sql = "INSERT INTO attendance "\
            f"VALUES(NULL, {attendance['category']}, '{attendance['date']}', "\
            f"'{attendance['first_auth_start_time']}', '{attendance['first_auth_end_time']}', "\
            f"'{attendance['second_auth_start_time']}', '{attendance['second_auth_end_time']}');"
        print(sql)
        database.execute(sql)
        database.commit()
        database.close()

        return {'message': '출석 정보를 추가했어요 :)'}, 200

@attendance.route("/modify/<int:attendance_id>")
class AttendanceEditAPI(Resource):
    # 출석 정보 수정
    def put(self, attendance_id):
        # Body 데이터 읽어오기
        attendance = request.get_json()

        # category를 index로 변환
        attendance['category'] = convert_to_index(ATTENDANCE_CATEGORY, attendance['category'])

        # 수정된 출석 정보를 DB에 반영
        database = Database()
        sql = "UPDATE attendance SET "\
            f"category = {attendance['category']}, date = '{attendance['date']}', "\
            f"first_auth_start_time = '{attendance['first_auth_start_time']}', first_auth_end_time = '{attendance['first_auth_end_time']}', "\
            f"second_auth_start_time = '{attendance['second_auth_start_time']}', second_auth_end_time = '{attendance['second_auth_end_time']}' "\
            f"WHERE id = {attendance_id}"
        database.execute(sql)
        database.commit()
        database.close()

        return {'message': '출석 정보를 수정했어요 :)'}, 200

    # 출석 정보 삭제
    def delete(self, attendance_id):
        database = Database()

        # 회원 출석 내역을 DB에서 삭제
        sql = f"DELETE FROM user_attendance WHERE attendance_id = {attendance_id};"
        database.execute(sql)

        # 출석 정보를 DB에서 삭제
        sql = f"DELETE FROM attendance WHERE id = {attendance_id};"
        database.execute(sql)

        database.commit()
        database.close()

        return {'message': '출석 정보를 삭제했어요 :)'}, 200
 
@attendance.route('/users')
class AttendanceUserListAPI(Resource):
    # 회원 목록 얻기
    def get(self):
        # DB에서 회원 목록 불러오기
        database = Database()
        sql = "SELECT * FROM users;"
        user_list = database.execute_all(sql)
        database.close()
        return user_list, 200