from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database
from utils.dto import AdminAttendanceDTO

attendance = AdminAttendanceDTO.api

# 회원 활동 여부
USER_REST_TYPE = {-1: '활동', 0: '일반휴학', 1:'군휴학'}

# 출석 category
ATTENDANCE_CATEGORY = {0: '디자인', 1: '아트', 2: '프로그래밍', 3: '정기', 4: '기타'}

# 회원 출석 state
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

class AttendanceInfoAPI(Resource):
    # category, date에 따른 출석 정보 얻기
    @attendance.expect(AdminAttendanceDTO.query_date, validate=True)
    @attendance.response(200, 'OK', AdminAttendanceDTO.response_attendance_with_code)
    @attendance.response(400, 'Bad Request', AdminAttendanceDTO.response_message_with_code)
    @attendance.route("/category/<int:category>")
    def get(self, category):
        # Query Parameter 데이터 읽어오기
        date = request.args['date']

        # DB 예외 처리
        try:
            # DB에서 category, date값에 맞는 출석 정보 가져오기
            database = Database()
            sql = f"SELECT * FROM attendance WHERE category = {category} and date = '{date}';"
            attendance = database.execute_one(sql)
        except:
            return {'message': '데이터베이스 오류가 발생했어요 :('}, 400
        finally:
            database.close()

        # 출석 정보가 존재할 때 처리
        if attendance:
            # date, time을 문자열로 변환
            attendance['date'] = attendance['date'].strftime('%Y-%m-%d')
            attendance['first_auth_start_time'] = str(attendance['first_auth_start_time'])
            attendance['first_auth_end_time'] = str(attendance['first_auth_end_time'])
            attendance['second_auth_start_time'] = str(attendance['second_auth_start_time'])
            attendance['second_auth_end_time'] = str(attendance['second_auth_end_time'])

        return attendance, 200
    
    # 출석 정보 수정
    @attendance.expect(AdminAttendanceDTO.model_attendance, validate=True)
    @attendance.response(200, 'OK', AdminAttendanceDTO.response_message_with_code)
    @attendance.response(400, 'Bad Request', AdminAttendanceDTO.response_message_with_code)
    def put(self, category):
        # Body 데이터 읽어오기
        attendance = request.get_json()

        # DB 예외처리
        try:
            # 수정된 출석 정보를 DB에 반영
            database = Database()
            sql = "UPDATE attendance SET "\
                f"category = {category}, date = '{attendance['date']}', "\
                f"first_auth_start_time = '{attendance['first_auth_start_time']}', first_auth_end_time = '{attendance['first_auth_end_time']}', "\
                f"second_auth_start_time = '{attendance['second_auth_start_time']}', second_auth_end_time = '{attendance['second_auth_end_time']}' "\
                f"WHERE id = {attendance['id']}"
            database.execute(sql)
            database.commit()
        except:
            return {'message': '데이터베이스 오류가 발생했어요 :('}, 400
        finally:
            database.close()

        return {'message': '출석 정보를 수정했어요 :)'}, 200
 
@attendance.route('/users')
class AttendanceUserListAPI(Resource):
    # 회원 목록 얻기
    @attendance.expect(AdminAttendanceDTO.query_attendance_id, validate=True)
    @attendance.response(200, 'OK', AdminAttendanceDTO.response_user_list_with_code)
    @attendance.response(400, 'Bad Request', AdminAttendanceDTO.response_message_with_code)
    def get(self):
        # Query Parameter 데이터 읽어오기
        attendance_id = request.args['attendance_id']

        # DB 예외 처리
        try:
            # DB에서 회원 목록 불러오기
            database = Database()
            sql = "SELECT u.id, u.name, u.grade, u.part_index, u.rest_type, ua.first_auth_time, ua.second_auth_time, ua.state FROM users u LEFT JOIN user_attendance ua "\
                f"ON u.id = ua.user_id WHERE ua.attendance_id = {attendance_id};"
            user_list = database.execute_all(sql)
        except:
            return {'message': '데이터베이스 오류가 발생했어요 :('}, 400
        finally:
            database.close()

        if not user_list: # 회원이 존재하지 않을 경우 처리
            return {}, 200
        else:
            # 회원의 소속 파트 index를 문자열로 변환
            for idx, user in enumerate(user_list):
                user_list[idx]['part_index'] = convert_to_string(ATTENDANCE_CATEGORY, user['part_index'])
                user_list[idx]['rest_type'] = convert_to_string(USER_REST_TYPE, user['rest_type'])
                user_list[idx]['state'] = convert_to_string(USER_ATTENDANCE_STATE, user['state'])
        return user_list, 200
    
@attendance.route('/user/<int:attendance_id>')
class AttendanceUserAPI(Resource):
    # 회원 출석 정보 얻기
    @attendance.expect(AdminAttendanceDTO.query_attendance_id, validate=True)
    @attendance.response(200, 'OK', AdminAttendanceDTO.response_user_attendance_with_code)
    @attendance.response(400, 'Bad Request', AdminAttendanceDTO.response_message_with_code)
    def get(self, attendance_id):
        # Query Parameter 데이터 읽어오기
        user_id = request.args['user_id']

        # DB 예외처리
        try:
            # DB에서 회원 출석 정보 불러오기
            database = Database()
            sql = f"SELECT * FROM user_attendance WHERE attendance_id = {attendance_id} and user_id = '{user_id}';"
            user_attendance = database.execute_one(sql)
        except:
            return {'message': '데이터베이스 오류가 발생했어요 :('}, 400
        finally:
            database.close()

        # 회원 출석 정보가 존재할 시 처리
        if user_attendance:
            # 회원 출석 state, 출석 인증 시간을 문자열로 변경
            user_attendance['state'] = convert_to_string(USER_ATTENDANCE_STATE, user_attendance['state'])
            user_attendance['first_auth_time'] = str(user_attendance['first_auth_time'])
            user_attendance['second_auth_time'] = str(user_attendance['second_auth_time'])
        
        return user_attendance, 200

    @attendance.expect(AdminAttendanceDTO.model_user_attendance, validate=True)
    @attendance.response(200, 'OK', AdminAttendanceDTO.response_message_with_code)
    @attendance.response(400, 'Bad Request', AdminAttendanceDTO.response_message_with_code)
    def put(self, attendance_id):
        # Body 데이터 읽어오기
        user_attendance = request.get_json()

        # 회원 출석 state를 index로 변경
        user_attendance['state'] = convert_to_index(USER_ATTENDANCE_STATE, user_attendance['state'])

        # DB 예외처리
        try:
            # 수정된 회원 출석 정보를 DB에 반영
            database = Database()
            sql = "INSERT INTO user_attendance (attendance_id, user_id, state, first_auth_time, second_auth_time) VALUES(%s, %s, %s, %s, %s) "\
                "ON DUPLICATE KEY UPDATE state = %s, first_auth_time = %s, second_auth_time = %s;"
            value = (attendance_id, user_attendance['user_id'], user_attendance['state'], user_attendance['first_auth_time'], user_attendance['second_auth_time'], 
                    user_attendance['state'], user_attendance['first_auth_time'], user_attendance['second_auth_time'])
            database.execute(sql, value)
            database.commit()
        except:
            return {'message': '데이터베이스 오류가 발생했어요 :('}, 400
        finally:
            database.close()

        return {'message': '유저 출석 정보를 수정했어요 :)'}, 200
