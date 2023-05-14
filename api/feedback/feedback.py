from flask import Flask, request, make_response, jsonify
from flask_restx import Resource, Namespace
from database.database import Database
from datetime import datetime, timedelta

feedback = Namespace('feedback')
'''
table feedback
식별CODE|code       |BIGINT |-prk
회원ID  |user_id    |BIGINT |
익명    |is_anony   |BOOL   | -false
제목    |title      |VARCHAR|
내용    |content    |VARCHAR|
답변여부|is_answered|BOOL    |-false
     |
    ---
     O
     |
    ---
     |
table feedback_answer
식별CODE    |code       |BIGINT |
질문한회원ID|user_id    |BIGINT |
답변        |answer     |VARCHAR|
답변한회원ID|answer_id  |BIGINT |
'''
@feedback.route("/<int:feedback_code>")
class FeedbackGetAPI(Resource): # 임원만(id) 볼 수 있어야함
    def get(self, feedback_code):
        
        # Body 데이터 얻어오기 (user_id)
        body_data = request.get_json()
        user_id = body_data['user_id']
        
        # 데이터베이스에서 feedback 목록을 불러옴
        database = Database()
        sql = f"SELECT * FROM feedback WHERE feedback_code = {feedback_code};"
        feedback = database.execute_all(sql)
        
        # 임원이 아닐 경우
        if not user_id:
            database.close()
            return {'message': '피드백을 볼 수 있는 권한이 없습니다'}, 401
        
        # feedback이 하나도 없을 때의 처리
        if not feedback:
            database.close()
            return [], 200
        else:
            if(feedback['is_anony']==1): # 익명 처리
                feedback['user_id'] = 0
            return feedback, 200
@feedback.route("/list")
class FeedbackListGetAPI(Resource): # 임원만(id) 볼 수 있어야함
    def get(self):
        
        # Body 데이터 얻어오기 (user_id)
        body_data = request.get_json()
        user_id = body_data['user_id']
        
        # 임원이 아닐 경우
        if not user_id:
            return {'message': '피드백을 볼 수 있는 권한이 없습니다'}, 401
        
        # 데이터베이스에서 feedback 목록을 불러옴
        database = Database()
        sql = f"SELECT * FROM feedback;" 
        feedback_list = database.execute_all(sql)
        
        # feedback이 하나도 없을 때의 처리
        if not feedback_list:
            database.close()
            return [], 200
        else:
            for idx, value in enumerate(feedback_list): 
                if(feedback_list[idx]['is_anony'] == 1): # 익명처리
                    feedback_list[idx]['user_id'] = 0
            return feedback_list, 200
               
@feedback.route("/<int:feedback_code>/<bool:is_anony")
class FeedbackPostAPI(Resource):
    def post(self, feedback_code, is_anony):
        
        # Body 데이터 얻어오기
        body_data = request.get_json()
        user_id = body_data['user_id']
        title = body_data['title']
        content = body_data['content']
        
        # feedback이 존재하는지 확인
        database = Database()
        sql = f"SELECT * FROM feedback WHERE code = '{feedback_code}';"
        feedback = database.execute_one(sql)
        
        # feedback이 존재할 때의 처리
        if feedback:
            database.close()
            return {'message': '이미 존재하는 피드백입니다.'}
        # feedback이 존재하지 않을 때 새로 작성
        else:
            sql = f"INSERT INTO feedback(code, user_id, is_anony, title, content, is_answered) "\
                f"VALUES('{feedback_code}', {user_id}, '{title}', '{content}', NULL);"
            database.execute(sql)
            database.commit()
            
            database.close()
            return body_data, 200              
                
@feedback.route("/answer/<int:feedback_code>")
class FeedbackAnswerAPI(Resource):
    def put(self, feedback_code):
        
        # Body 데이터 얻어오기
        body_data = request.get_json()
        answer_id = body_data['user_id']
        answer = body_data['answer']
        
        # 임원이 아닐 경우
        if not answer_id:
            database.close()
            return {'message': '피드백을 볼 수 있는 권한이 없습니다'}, 401
        
        # feedback이 존재하는지 확인
        database = Database()
        sql = f"SELECT * FROM feedback WHERE code = '{feedback_code}';"
        feedback = database.execute_one(sql)
        user_id = feedback['user_id']
        
        # feedback이 존재하지 않을 때의 처리
        if not feedback:
            database.close()
            return {'message': '존재하지 않는 피드백입니다.'}
        
        # answer이 존재하는지 확인
        database = Database()
        sql = f"SELECT * FROM feedback_anwer WHERE code = '{feedback_code}';"
        feedback_answer = database.execute_one(sql)

        # answer이 존재할 때 처리
        if feedback_answer:
            database.close()
            return {'message': '이미 답변된 피드백입니다.'}
        
        # answer 작성
        else:
            sql = f"INSERT INTO feedback_answer(code, user_id, answer, answer_id) "\
                f"VALUES('{feedback_code}',{user_id} ,{answer}, {answer_id});"
            database.execute(sql)
            # is_answered update
            sql = f"UPDATE feedback SET is_answered = 1 "\
                f"WHERE code = '{feedback_code}';"
            database.execute(sql)
            database.commit()
            
            database.close()
            return body_data, 200                         
        
        