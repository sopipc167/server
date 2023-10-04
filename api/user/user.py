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
        
        # 동아리에 가입되어 있는 여부를 Boolean 값으로 변경
        user_data['is_signed'] = True if user_data['is_signed'] else False

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
            project_data['start_date'] = project_data['start_date'].strftime('%Y-%m-%d')
            project_data['end_date'] = project_data['end_date'].strftime('%Y-%m-%d')

            # 플랫폼 정보를 List<String>의 형식으로 변환
            platform_list = project_data['platform'].split(',')
            project_data['platform'] = platform_list

            # 팀원 모집 여부와 문의 가능 여부를 Boolean 값으로 변경
            project_data['is_finding_member'] = True if project_data['is_finding_member'] else False
            project_data['is_able_inquiry'] = True if project_data['is_able_inquiry'] else False

            # PM 초기화
            project_data['pm'] = None

            # 소속된 프로젝트(들)의 멤버 식별자 목록 조회
            sql = f"SELECT * FROM project_members where project_id = {id};"
            project_members = database.execute_all(sql)
            
            # 프로젝트 팀원 별 상세 정보를 불러오고 members와 pm에 각각 할당
            members = []
            for member in project_members:
                # 유저 상세 정보 조회
                id = member['user_id']
                sql = f"SELECT * FROM users where id = {id};"
                member_data = database.execute_one(sql)

                # 동아리에 가입되어 있는 여부를 Boolean 값으로 변경
                member_data['is_signed'] = True if member_data['is_signed'] else False

                # PM이면 pm에 따로 추가, PM이 아니면 members에 추가
                if member['is_pm']:
                    project_data['pm'] = member_data
                else:
                    members.append(member_data)
            project_data['members'] = members
            
            # 얻은 프로젝트 정보를 리스트에 추가
            project_data_list.append(project_data)
        
        user_data['projects'] = project_data_list
        database.close()

        return user_data, 200

@user.route("/notification/<string:id>")
class UserNotification(Resource):
    def get(self):
        database = Database()
        sql1 = f"select level from users where id={id}"
        lev = database.execute_one(sql1)
        if lev ==1:
            sql2 = f"select n.time, n.message, n.memo from notification as n where id = 0 or id = 1;"
        elif lev ==2 or lev==4:
            sql2 = f"select n.time, n.message, n.memo from notification as n where id = 0 or id = 2;"
        else:
            sql2 = f""
        data =  database.execute_all(sql2)
        return data
