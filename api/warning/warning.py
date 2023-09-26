from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database
from utils.dto import WarningDTO

warning = WarningDTO.api

# category(경고 종류)
WARNING_CATEGORY = {-2: '경고 차감', -1: '주의 차감', 1: '주의 부여', 2: '경고 부여', 0: '경고 초기화'}

# index 데이터를 문자열로 변경
def convert_to_string(dictionary, index):
    return dictionary.get(index, None)

# 문자열 데이터를 index로 변경
def convert_to_index(dictionary, string):
    for key, value in dictionary.items():
        if value == string:
            return key
    return None

@warning.route('')
class WarningStatusUserAPI(Resource):
    # 회원의 경고 목록 얻기
    @warning.expect(WarningDTO.query_user_id, validate=True)
    @warning.response(200, 'OK', WarningDTO.model_warning_list)
    def get(self):
        # 추후 토큰으로 대신할 예정
        user_id = request.args['user_id']

        # DB 예외 처리
        try:
            # DB에서 user_id값에 맞는 경고 목록 불러오기
            database = Database()
            sql = f"SELECT * FROM warnings WHERE user_id = '{user_id}';"
            warning_list = database.execute_all(sql)
        except:
            return {'message': '데이터베이스 오류가 발생했어요 :('}, 400
        finally:
            database.close()

        if not warning_list: # 경고를 받은 적이 없을 때 처리
            return [], 200
        else:
            for idx, warning in enumerate(warning_list):
                # date 및 category를 문자열로 변환
                warning_list[idx]['date'] = warning['date'].strftime('%Y-%m-%d')
                warning_list[idx]['category'] = convert_to_string(WARNING_CATEGORY, warning['category'])
            return warning_list, 200
    
    # 회원에 대한 경고 추가
    @warning.expect(WarningDTO.query_user_id, WarningDTO.model_warning, validate=True)
    @warning.response(200, 'OK', WarningDTO.warning_response_message)
    def post(self):
        # 추후 토큰으로 대신할 예정
        user_id = request.args['user_id']

        # Body 데이터 읽어오기
        warning = request.get_json()

        # user_id 설정, category를 index로 변환
        warning['category'] = convert_to_index(WARNING_CATEGORY, warning['category'])

        # DB 예외 처리
        try:
            # 경고 현황을 DB에 추가
            database = Database()
            sql = f"INSERT INTO warnings "\
                f"VALUES(NULL, '{user_id}', {warning['category']}, "\
                f"'{warning['date']}', '{warning['description']}', '{warning['comment']}');"
            database.execute(sql)
            database.commit()
        except:
            return {'message': '데이터베이스 오류가 발생했어요 :('}, 400
        finally:
            database.close()

        return {'message': '경고 정보를 추가했어요 :)'}, 201

    # 경고 현황 수정
    @warning.expect(WarningDTO.query_user_id, WarningDTO.model_warning_with_id, validate=True)
    @warning.response(200, 'OK', WarningDTO.warning_response_message)
    def put(self):
        # 추후 토큰으로 대신할 예정
        user_id = request.args['user_id']

        # Body 데이터 받아오기
        warning = request.get_json()

        # category를 index로 변환
        warning['category'] = convert_to_index(WARNING_CATEGORY, warning['category'])

        # DB 예외 처리
        try:
            # 수정된 사항을 DB에 반영
            database = Database()
            sql = f"UPDATE warnings SET "\
            f"id = {warning['id']}, user_id = '{user_id}', category = {warning['category']}, "\
            f"date = '{warning['date']}', description = '{warning['description']}', comment = '{warning['comment']}' "\
            f"WHERE id = {warning['id']};"
            database.execute(sql)
            database.commit()
        except:
            return {'message': '데이터베이스 오류가 발생했어요 :('}, 400
        finally:
            database.close()

        return {'message': '경고 정보를 수정했어요 :)'}, 200

    # 경고 현황 삭제
    @warning.expect(WarningDTO.query_warning_id, validate=True)
    @warning.response(200, 'OK', WarningDTO.warning_response_message)
    def delete(self):
        warning_id = request.args['id']

        # DB 예외 처리
        try:
            # 경고 현황을 DB에서 삭제
            database = Database()
            sql = f"DELETE FROM warnings WHERE id = {warning_id};"
            database.execute(sql)
            database.commit()
        except:
            return {'message': '데이터베이스 오류가 발생했어요 :('}, 400
        finally:
            database.close()

        return {'message': '경고 정보를 삭제했어요 :)'}, 200