import requests
from flask import Flask, redirect, request
from flask_restx import Resource, Api, Namespace
from database.database import Database
from datetime import datetime

user = Namespace('user')

@user.route("/profile")
class UserProfile(Resource):
    def get(self):
        database = Database()
        # 유저 테이블에서 해당 유저에 대한 정보 조회
        # 추후에는 토큰 등을 받아서 어떤 사용자인지 인식하고, 해당 사용자에 대한 정보를 뿌려줄 예정
        sql = f"SELECT * FROM users where id = {1};"    # 추후에는 1이 아닌 각 유저에 대한 식별자가 들어갈 예정
        user_data = database.execute_one(sql)

        if not user_data:
            database.close()
            return { 'message': '회원 정보를 찾지 못했어요 :(' }, 400

        # 소속된 프로젝트(들)의 식별자 목록 조회
        sql = f"SELECT project_id FROM project_members where user_id = {user_data['id']};"
        project_id_list = database.execute_all(sql)

        # 소속된 프로젝트(들)의 상세 정보 조회
        project_data_list = []
        for data in project_id_list:
            id = data['project_id']
            sql = f"SELECT * FROM projects where id = {id};"
            project_data = database.execute_one(sql)

            # Date를 String으로 형 변환함
            project_data['start_date'] = datetime.strftime(project_data['start_date'])
            project_data['end_date'] = datetime.strftime(project_data['end_date'])

            # 소속된 프로젝트(들)의 멤버 식별자 목록 조회
            sql = f"SELECT * FROM project_members where project_id = {id};"
            project_member_id_list = database.execute_all(sql)
            
            # 멤버 식별자 목록을 이용하여 각 멤버별 상세 정보 조회
            members = []
            for member_id in project_member_id_list:
                id = member_id['user_id']
                sql = f"SELECT * FROM users where id = {id};"
                member_data = database.execute_one(sql)
                members.append(member_data)
            project_data['members'] = members
            
            project_data_list.append(project_data)
        
        user_data['projects'] = project_data_list
        database.close()

        return user_data, 200

@user.route("/notification")
class UserNotification(Resource):
    def get(self):
        data = [
            {
                "id": 1,
                "type": 0,
                "date": "2023-01-01 10:00:00",
                "description": "당일 10시에 청소가 시작됩니다.",
                "name": "청소 알림",
            },
            {
                "id": 2,
                "type": 0,
                "date": "2023-01-01 10:00:00",
                "description": "당일 10시에 청소가 시작됩니다.",
                "name": "청소 알림",
            },
            {
                "id": 1,
                "type": 0,
                "date": "2023-01-01 10:00:00",
                "description": "당일 10시에 청소가 시작됩니다.",
                "name": "청소 알림",
            },
            {
                "id": 1,
                "type": 0,
                "date": "2023-01-01 10:00:00",
                "description": "당일 10시에 청소가 시작됩니다.",
                "name": "청소 알림",
            }
        ]

        return data
