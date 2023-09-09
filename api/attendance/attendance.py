from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database
from datetime import datetime, date

attendance = Namespace('attendance')

# 출석 category
ATTENDANCE_CATEGORY = {0: '디자인 파트 회의', 1: '아트 파트 회의', 2: '프로그래밍 파트 회의', 3: '정기 회의', 4: '기타'}

# 유저 출석 state
USER_ATTENDANCE_STATE = {0: '출석', 1: '지각', 2: '불참'}

# index 데이터를 문자열로 변경
def convert_to_string(dictionary, index):
    return dictionary.get(index, None)

# 문자열 데이터를 index로 변경
def convert_to_index(dictionary, string):
    for key, value in dictionary.items():
        if value == string:
            return key
    return None


@attendance.route('')
class AttendanceUserAPI(Resource):
    # user_id에 따른 출석 정보 얻기
    def get(self):
        # 추후 토큰으로 대신할 예정
        user_id = request.args['user_id']

        database = Database()

        # DB에서 회원의 파트와 활동 여부 불러오기
        sql = f"SELECT part_index, rest_type FROM users;"
        user = database.execute_one(sql)

        # DB에서 최근 4번의 출석 기록 불러오기
        sql = "SELECT a.date, ua.state FROM user_attendance ua JOIN attendance a ON ua.attendance_id = a.id "\
            "ORDER BY a.date DESC LIMIT 4;"
        record_list = database.execute_all(sql)
        
        # date를 문자열로 변환 
        for idx, record in enumerate(record_list):
            record_list[idx]['date'] = record['date'].strftime('%Y-%m-%d')

        # 회원이 활동 중이지 않은 경우
        if user['rest_type'] != -1:
            database.close()
            return {'attendanc_list': [], 'record_list': record_list}, 200

        # 현재 출석해야 할 회의가 있는 경우 해당 출석 정보 불러오기
        current_date = datetime.today().strftime('%Y-%m-%d')
        sql = "SELECT a.id as attendance_id, a.category, a.date, a.first_auth_start_time, a.first_auth_end_time, "\
            "a.second_auth_start_time, a.second_auth_end_time, ua.state, ua.first_auth_time, ua.second_auth_time "\
            f"FROM attendance a LEFT JOIN user_attendance ua ON a.id = ua.attendance_id and ua.user_id = '{user_id}' "\
            f"WHERE a.date = '{current_date}' and a.category = '{user['part_index']}';"
        attendance_list = database.execute_all(sql)

        database.close()

        if not attendance_list: # 현재 출석해야 할 회의가 없는 경우 처리
            return {'attendanc_list': [], 'record_list': record_list}, 200
        else:
            # date, time, category, state를 문자열로 변환
            for idx, attendance in enumerate(attendance_list):
                attendance_list[idx]['date'] = attendance['date'].strftime('%Y-%m-%d')
                attendance_list[idx]['first_auth_start_time'] = str(attendance['first_auth_start_time'])
                attendance_list[idx]['first_auth_end_time'] = str(attendance['first_auth_end_time'])
                attendance_list[idx]['second_auth_start_time'] = str(attendance['second_auth_start_time'])
                attendance_list[idx]['second_auth_end_time'] = str(attendance['second_auth_end_time'])        
                attendance_list[idx]['first_auth_time'] = str(attendance['first_auth_time'])
                attendance_list[idx]['second_auth_time'] = str(attendance['second_auth_time'])
                attendance_list[idx]['category'] = convert_to_string(ATTENDANCE_CATEGORY, attendance['category'])
                attendance_list[idx]['state'] = convert_to_string(USER_ATTENDANCE_STATE, attendance['state'])

        return {'attendanc_list': attendance_list, 'record_list': record_list}, 200
    
    # 회원의 출석 인증 정보 추가
    def post(self):
        # Body 데이터 읽어오기
        user_attendance = request.get_json()

        # 회원 출석 state를 index로 변경
        user_attendance['state'] = convert_to_index(USER_ATTENDANCE_STATE, user_attendance['state'])

        # 회원 출석 정보를 DB에 추가
        database = Database()
        sql = "INSERT INTO user_attendance "\
            f"VALUES({user_attendance['attendance_id']}, '{user_attendance['user_id']}', "\
            f"{user_attendance['state']}, '{user_attendance['first_auth_time']}', '{user_attendance['second_auth_time']}');"
        database.execute(sql)
        database.commit()
        database.close()

        return {'message': '회원의 출석 인증 정보를 추가했어요 :)'}, 201
    
    # 회원의 출석 인증 정부 수정
    def put(self):
        # Body 데이터 읽어오기
        user_attendance = request.get_json()

        # 회원 출석 state를 index로 변경
        user_attendance['state'] = convert_to_index(USER_ATTENDANCE_STATE, user_attendance['state'])

        # 수정된 회원 출석 정보를 DB에 반영
        database = Database()
        sql = "UPDATE user_attendance SET "\
            f"state = {user_attendance['state']}, first_auth_time = '{user_attendance['first_auth_time']}', second_auth_time = '{user_attendance['second_auth_time']}' "\
            f"WHERE attendance_id = {user_attendance['attendance_id']} and user_id = '{user_attendance['user_id']}';"
        database.execute(sql)
        database.commit()
        database.close()

        return {'message': '회원의 출석 인증 정보를 수정했어요 :)'}, 201