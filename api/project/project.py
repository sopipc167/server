from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database

project = Namespace('project')

@project.route("/list")
class ProjectListAPI(Resource):
    def get(self):
        # 데이터베이스에서 프로젝트 목록을 불러옴
        database = Database()
        sql = f"SELECT * FROM projects;"
        project_list = database.execute_all(sql)
        
        if not project_list:    # 프로젝트가 하나도 없을 때의 처리
            database.close()
            return [], 200
        else:
            for idx, value in enumerate(project_list):
                # 날짜를 문자열 날짜로 변경
                project_list[idx]['start_date'] = value['start_date'].strftime('%Y-%m-%d')
                project_list[idx]['end_date'] = value['end_date'].strftime('%Y-%m-%d')
                
                # 플랫폼 정보를 List<String>의 형식으로 변환
                platform_list = project_list[idx]['platform'].split(',')
                project_list[idx]['platform'] = platform_list

                # 팀원 모집 여부와 문의 가능 여부를 Boolean 값으로 변경
                project_list[idx]['is_finding_member'] = True if value['is_finding_member'] else False
                project_list[idx]['is_able_inquiry'] = True if value['is_able_inquiry'] else False

                # PM 초기화
                project_list[idx]['pm'] = None

                # 프로젝트 팀원 목록 불러오기
                sql = f"SELECT * FROM project_members WHERE project_id = {project_list[idx]['id']};"
                project_members = database.execute_all(sql)
                
                # 프로젝트 팀원 별 상세 정보를 불러오고 members와 pm에 각각 할당
                member_list = []
                for member in project_members:
                    sql = f"SELECT * FROM users WHERE id = {member['user_id']};"
                    user_data = database.execute_one(sql)
                    # 동아리에 가입되어 있는 여부를 Boolean 값으로 변경
                    user_data['is_signed'] = True if user_data['is_signed'] else False

                    # PM이면 pm에 따로 추가, PM이 아니면 members에 추가
                    if member['is_pm']:
                        project_list[idx]['pm'] = user_data
                    else:
                        member_list.append(user_data)
                project_list[idx]['members'] = member_list
                
            return project_list, 200

@project.route('/<int:project_id>')
class ProjectDetailAPI(Resource):
    def get(self, project_id):
        # 데이터베이스에서 id 값에 맞는 프로젝트 상세 내역을 불러옴
        database = Database()
        sql = f"SELECT * FROM projects where id = {project_id};"
        project = database.execute_one(sql)
        
        if not project:
            database.close()
            return { 'message': '프로젝트 식별자가 올바르지 않아요 :(' }, 400
        else:
            # 날짜를 문자열 날짜로 변경
            project['start_date'] = project['start_date'].strftime('%Y/%m/%d')
            project['end_date'] = project['end_date'].strftime('%Y/%m/%d')
                
            # 팀원 모집 여부와 문의 가능 여부를 Boolean 값으로 변경
            project['is_finding_member'] = True if project['is_finding_member'] else False
            project['is_able_inquiry'] = True if project['is_able_inquiry'] else False
            
            # 프로젝트 팀원 목록의 id 조회
            sql = f"SELECT user_id from project_members where project_id = {project['id']};"
            user_id_list = database.execute_all(sql)
            user_list = []
            # 프로젝트에 속하는 팀원들의 상세 정보를 구하여 리스트에 추가
            for id_value in user_id_list:
                user_id = id_value['user_id']
                sql = f"SELECT * from users where id = {user_id};"
                row = database.execute_one(sql)
                user_list.append(row)
            
            # 프로젝트 팀원 목록 추가
            project['members'] = user_list
            database.close()
            
            return project, 200

@project.route('/<int:project_id>/modify')
class ProjectEditAPI(Resource):
    def put(self, project_id):
        # Body 데이터 얻어오기
        body_data = request.get_json()
        user_id = body_data['user_id']
        is_finding_member = body_data['is_finding_member']
        is_able_inquiry = body_data['is_able_inquiry']
        
        # 프로젝트가 존재하는 지 확인
        database = Database()
        sql = f"SELECT * FROM projects where id = {project_id};"
        project_list = database.execute_one(sql)
        
        # 프로젝트가 조회되지 않을 때의 처리
        if not project_list:
            database.close()
            return { 'message': '프로젝트가 조회되지 않아요 :(\n지속적으로 발생하면 문의해주세요!' }, 400
        
        # 요청한 유저가 프로젝트의 PM인지 조회
        sql = f"SELECT is_pm FROM project_members where project_id = {project_id} and user_id = {user_id};"
        row = database.execute_one(sql)

        if not row:
            # 조회되지 않을 때의 예외처리
            database.close()
            return { 'message': '프로젝트 정보나 유저 정보가 없어요 :(' }, 400
        elif row['is_pm']:
            # 요청한 프로젝트의 PM이 맞을 때의 처리
            sql = f"UPDATE projects SET is_finding_member = {is_finding_member}," \
                f"is_able_inquiry = {is_able_inquiry} WHERE id = {project_id};"
            database.execute(sql)
            database.commit()
            database.close()
            return { 'message': '프로젝트 정보를 변경했습니다 :)' }, 200
        else:
            # 요청한 프로젝트의 PM이 아닐 떄의 처리
            database.close()
            return { 'message': '프로젝트의 PM만 수정할 수 있어요 :(' }, 400