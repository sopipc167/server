from flask import request
from flask_restx import Resource, Namespace, fields
from database.database import Database
from utils.dto import feedbackDTO

feedback = feedbackDTO.api
@feedback.route("/<int:feedback_code>")
@feedback.response(200, 'Success',feedbackDTO.feedback_response_search)
@feedback.response(200, 'Post Success',feedbackDTO.post_sucess)
@feedback.response(400, 'Invaild Feedback',feedbackDTO.invalid_feedback)
@feedback.response(400, 'No Title',feedbackDTO.no_title)
@feedback.response(400, 'No contents',feedbackDTO.no_contents)
class FeedbackGetAPI(Resource):  # 임원만(id) 볼 수 있어야함
    def get(self, feedback_code):
        # Body 데이터 얻어오기 (user_id)
        body_data = request.get_json()
        user_id = body_data['user_id']

        # 데이터베이스에서 feedback 목록을 불러옴
        database = Database()
        sql = f"SELECT * FROM feedback WHERE feedback_code = {feedback_code};"
        feedback = database.execute_all(sql)

        # feedback이 하나도 없을 때의 처리
        if not feedback:
            database.close()
            return {'message': '존재하지 않는 피드백입니다'}, 400
        else:
            if feedback['is_anony'] == 1:  # 익명 처리
                feedback['user_id'] = 0
            return feedback, 200

    def post(self, feedback_code):
        # Body 데이터 얻어오기
        body_data = request.get_json()
        is_anony = body_data['is_anony']
        user_id = body_data['user_id']
        title = body_data['title']
        content = body_data['content']
        database = Database()

        # 피드백 개수를 세서 id를 할당함
        sql = f"SELECT COUNT(code) from feedback;"
        count = database.execute(sql)
        feedback_code = count

        # 만약 작성항목에 널값이 있는지 확인
        if not title: # 피드백 제목을 작성하지 않을때 예외 발생
            return {'message': '제목을 입력해주세요'}, 400
        elif not content: # 피드백 내용을 작성하지 않을때 예외 발생
            return {'message': '피드백 내용을 입력해주세요'}, 400
        else: # 피드백을 정상적으로 작성하고
            sql = f"INSERT INTO feedback(code, user_id, is_anony, title, content, is_answered) " \
                  f"VALUES('{feedback_code}', '{user_id}' ,{is_anony}, '{title}', '{content}', 0);"
            database.execute(sql)
            database.commit()

            database.close()
            return body_data, 200


@feedback.route("/list")
@feedback.response(200, 'Success',feedbackDTO.feedback_response_all)
@feedback.response(200, 'No feedback found',feedbackDTO.no_feedback_found)
class FeedbackListGetAPI(Resource):
    def get(self):
        body_data = request.get_json()
        user_id = body_data['user_id']

        # 데이터베이스에서 feedback 목록을 불러옴
        database = Database()
        sql = f"SELECT * FROM feedback;"
        feedback_list = database.execute_all(sql)
        database.close()

        # feedback이 하나도 없을 때의 처리
        if not feedback_list:
            return {'message': '생성된 피드백이 없어요'}, 200
        else:
            for idx, value in enumerate(feedback_list):
                if feedback_list[idx]['is_anony'] == 1:  # 익명처리
                    feedback_list[idx]['user_id'] = 0
                return feedback_list, 200

@feedback.route("/answer/<int:feedback_code>")
@feedback.response(200, 'Post Success',feedbackDTO.post_sucess)
@feedback.response(401, 'Access Denied',feedbackDTO.not_qualified)
@feedback.response(400, 'Invaild Feedback',feedbackDTO.invalid_feedback)
@feedback.response(400, 'No contents',feedbackDTO.no_contents)
@feedback.response(400, 'already answered',feedbackDTO.already_answered)
class FeedbackAnswerAPI(Resource):
    def post(self, feedback_code):
        # Body 데이터 얻어오기
        body_data = request.get_json()
        answer_id = body_data['user_id']
        answer = body_data['answer']

        # 임원이 아닐 경우
        if not answer_id:
            return {'message': '피드백을 볼 수 있는 권한이 없어요'}, 401

        # feedback이 존재하는지 확인
        database = Database()
        sql = f"SELECT * FROM feedback WHERE code = '{feedback_code}';"
        feedback = database.execute_one(sql)
        user_id = feedback['user_id']

        # feedback이 존재하지 않을 때의 처리
        if not feedback:
            database.close()
            return {'message': '존재하지 않는 피드백이에요.'}, 400

        # answer이 존재하는지 확인
        sql = f"SELECT * FROM feedback_answer WHERE code = '{feedback_code}';"
        feedback_answer = database.execute_one(sql)

        # answer이 존재할 때 처리
        if feedback_answer:
            database.close()
            return {'message': '이미 답변된 피드백이에요.'}, 400

        # answer 작성
        else:
            if not answer:
                return {'message': '답변 내용을 작성해주세요'}, 400
            sql = (f"INSERT INTO feedback_answer(code, user_id, answer, answer_id) " \
                   f"VALUES({feedback_code},'{user_id}' ,'{answer}', {answer_id});")
            database.execute(sql)
            # is_answered update
            sql = f"UPDATE feedback SET is_answered = 1 " \
                  f"WHERE code = '{feedback_code}';"
            database.execute(sql)
            database.commit()

            database.close()
            return {'message': '피드백이 성공적으로 작성되었어요'}, 200