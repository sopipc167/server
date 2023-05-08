from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database

# category(세미나 종류)
SEMINAR_CATEGORY = {0: '재학생', 1: '프로그래밍', 2: '디자인', 3: '아트'}

# category를 문자열로 변환
def sc_int_to_str(category):
    return SEMINAR_CATEGORY.get(category, None)

# category를 index로 변환
def sc_str_to_int(category):
    for key, value in SEMINAR_CATEGORY.items():
        if value == category:
            return key
    return None

seminar = Namespace('seminar')

@seminar.route('/<int:user_id>')
class SeminarUserAPI(Resource):
    # 회원의 세미나 목록 얻기
    def get(self, user_id):
        # DB에서 user_id값에 맞는 세미나 목록 불러오기
        database = Database()
        sql = f"SELECT * FROM seminars WHERE user_id = {user_id}"
        seminar_list = database.execute_all(sql)
        database.close()

        if not seminar_list: # 세미나를 한 적이 없을 때 처리
            return [], 200
        else:
            for idx, seminar in enumerate(seminar_list):
                # date 및 category를 문자열로 변경
                seminar_list[idx]['date'] = seminar['date'].strftime('%Y-%m-%d')
                seminar_list[idx]['category'] = sc_int_to_str(seminar['category'])
            return seminar_list, 200
        
    # 세미나 정보 추가
    def post(self, user_id):
        # Body 데이터 읽어오기
        seminar = request.get_json()

        # user_id 설정, category를 index로 변환
        seminar['user_id'] = user_id
        seminar['category'] = sc_str_to_int(seminar['category'])

        # 세미나 정보를 DB에 추가
        database = Database()
        sql = f"INSERT INTO seminars "\
            f"VALUES({seminar['id']}, {seminar['user_id']}, '{seminar['title']}', "\
            f"'{seminar['url']}', {seminar['category']}, '{seminar['date']}');"
        database.execute(sql)
        database.commit()
        database.close()

        return seminar, 200
    

@seminar.route('/<int:seminar_id>/modify')
class SeminarEditAPI(Resource):
    # 세미나 정보 수정
    def put(self, seminar_id):
        # Body 데이터 받아오기
        seminar = request.get_json()

        # id 설정, category를 index로 변환
        seminar['id'] = seminar_id
        seminar['category'] = sc_str_to_int(seminar['category'])

        # 수정된 사항을 DB에 반영
        database = Database()
        sql = f"UPDATE seminars SET "\
        f"id = {seminar['id']}, user_id = {seminar['user_id']}, title = '{seminar['title']}', "\
        f"url = '{seminar['url']}', category = {seminar['category']}, date = '{seminar['date']}' "\
        f"WHERE id = {seminar_id};"
        database.execute(sql)
        database.commit()
        database.close()

        return {'message': '세미나 정보를 수정했어요 :)'}, 200

    # 세미나 정보 삭제
    def delete(self, seminar_id):
        # 세미나 정보를 DB에서 삭제
        database = Database()
        sql = f"DELETE FROM seminars WHERE id = {seminar_id};"
        database.execute(sql)
        database.commit()
        database.close()

        return {'message': '세미나 정보를 삭제했어요 :)'}, 200