from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database
from utils.dto import SeminarDTO

seminar = SeminarDTO.api

# category(세미나 종류)
SEMINAR_CATEGORY = {0: '디자인', 1: '아트', 2: '프로그래밍', 3: '재학생'}

# index 데이터를 문자열로 변경
def convert_to_string(dictionary, index):
    return dictionary.get(index, None)

# 문자열 데이터를 index로 변경
def convert_to_index(dictionary, string):
    for key, value in dictionary.items():
        if value == string:
            return key
    return None

@seminar.route('')
class SeminarUserAPI(Resource):
    # 회원의 세미나 목록 얻기
    @seminar.expect(SeminarDTO.query_user_id, validate=True)
    @seminar.response(200, 'OK', SeminarDTO.model_seminar_list)
    def get(self):
        user_id = request.args['user_id']

        # DB 예외 처리
        try:
            # DB에서 user_id값에 맞는 세미나 목록 불러오기
            database = Database()
            sql = f"SELECT * FROM seminars WHERE user_id = '{user_id}';"
            seminar_list = database.execute_all(sql)
        except:
            return {'message': '서버에 오류가 발생했어요 :(\n지속적으로 발생하면 문의주세요!'}, 400
        finally:
            database.close()

        if not seminar_list: # 세미나를 한 적이 없을 때 처리
            return {'seminar_list': []}, 200
        else:
            for idx, seminar in enumerate(seminar_list):
                # date 및 category를 문자열로 변경
                seminar_list[idx]['date'] = seminar['date'].strftime('%Y-%m-%d')
                seminar_list[idx]['category'] = convert_to_string(SEMINAR_CATEGORY, seminar['category'])
            return {'seminar_list': seminar_list}, 200
        
    # 세미나 정보 추가
    @seminar.expect(SeminarDTO.query_user_id, SeminarDTO.model_seminar, validate=True)
    @seminar.response(201, 'Created', SeminarDTO.seminar_response_message)
    def post(self):
        user_id = request.args['user_id']

        # Body 데이터 읽어오기
        seminar = request.get_json()

        # category를 index로 변환
        seminar['category'] = convert_to_index(SEMINAR_CATEGORY, seminar['category'])

        # DB 예외 처리
        try:
            # 세미나 정보를 DB에 추가
            database = Database()
            sql = f"INSERT INTO seminars "\
                f"VALUES(NULL, '{user_id}', '{seminar['title']}', "\
                f"'{seminar['url']}', {seminar['category']}, '{seminar['date']}');"
            database.execute(sql)
            database.commit()
        except:
            return {'message': '서버에 오류가 발생했어요 :(\n지속적으로 발생하면 문의주세요!'}, 400
        finally:
            database.close()

        return {'message': '세미나 정보를 추가했어요 :)'}, 201

    # 세미나 정보 수정
    @seminar.expect(SeminarDTO.query_user_id, SeminarDTO.model_seminar_with_id, validate=True)
    @seminar.response(200, 'OK', SeminarDTO.seminar_response_message)
    def put(self):
        user_id = request.args['user_id']

        # Body 데이터 받아오기
        seminar = request.get_json()

        # category를 index로 변환
        seminar['category'] = convert_to_index(SEMINAR_CATEGORY, seminar['category'])

        # DB 예외 처리
        try:
            # 수정된 사항을 DB에 반영
            database = Database()
            sql = f"UPDATE seminars SET "\
            f"id = {seminar['id']}, user_id = '{user_id}', title = '{seminar['title']}', "\
            f"url = '{seminar['url']}', category = {seminar['category']}, date = '{seminar['date']}' "\
            f"WHERE id = {seminar['id']};"
            database.execute(sql)
            database.commit()
        except:
            return {'message': '서버에 오류가 발생했어요 :(\n지속적으로 발생하면 문의주세요!'}, 400
        finally:
            database.close()

        return {'message': '세미나 정보를 수정했어요 :)'}, 200

    # 세미나 정보 삭제
    @seminar.expect(SeminarDTO.query_seminar_id, validate=True)
    @seminar.response(200, 'OK', SeminarDTO.seminar_response_message)
    def delete(self):
        seminar_id = request.args['id']

        # DB 예외 처리
        try:
            # 세미나 정보를 DB  에서 삭제
            database = Database()
            sql = f"DELETE FROM seminars WHERE id = {seminar_id};"
            database.execute(sql)
            database.commit()
        except:
            return {'message': '서버에 오류가 발생했어요 :(\n지속적으로 발생하면 문의주세요!'}, 400
        finally:
            database.close()

        return {'message': '세미나 정보를 삭제했어요 :)'}, 200