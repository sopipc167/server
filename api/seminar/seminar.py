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
        
    # 세미나 추가
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