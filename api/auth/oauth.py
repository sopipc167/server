import requests
from flask import Flask, redirect, request
from flask_restx import Resource, Api, Namespace
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini', encoding='utf-8')

client_id = config['naver_login']['client_id']
client_secret = config['naver_login']['client_secret']

oauth = Namespace('oauth')
'''
@oauth.route("/naver/login")
class NaverLogin(Resource):
    def get():
        redirect_uri = "http://p-cube-plus.com/oauth/naver/callback"
        url = f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        return redirect(url)

@oauth.route("/naver/callback")
def get():
    params = request.args.to_dict()
    code = params.get("code")

    token_request = requests.get(
        f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}")
    token_json = token_request.json()

    access_token = token_json.get("access_token")
    profile_request = requests.get(
        "https://openapi.naver.com/v1/nid/me", headers={"Authorization": f"Bearer {access_token}"},)
    profile_data = profile_request.json()

    return {'profile_data': profile_data, 'token_data': token_json}


@app.route("/auth/naver/leave", methods=['GET'])
def leave():

    headers = request.headers
    if headers.get('Authorization') is None:
        return {'message': 'Unauthorized'}, 401

    access_token = headers.get('Authorization')
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'access_token': access_token,
        'grant_type': 'delete',
        'service_provider': 'NAVER'
    }

    leave_request = requests.post(
        "https://nid.naver.com/oauth2.0/token", params=params)
    leave_data = leave_request.json()

    return leave_data
'''

@oauth.route("/user/profile", methods=['GET'])
class UserProfile(Resource):
    def get(self):
        data = {
            "id": 1,
            "level": "수습회원",
            "name": "김판큐",
            "part_index": 1,
            "profile_image": "url",
            "projects": [
                {
                    "id": 1,
                    "type": 0,
                    "name": "PCube+",
                    "is_end": False,
                    "start_date": "2022-05-27 00:00:00.000Z",
                    "end_date": "2022-05-27 00:00:00.000Z",
                    "tags": [
                        "2D",
                        "etc",
                        "etc",
                    ],
                    "members": [
                        {
                            "id": 1,
                            "name": "오창한",
                            "part_index": 1
                        },
                        {
                            "id": 2,
                            "name": "조승빈",
                            "part_index": 1
                        },
                    ],
                    "platform": [
                        "Android",
                        "iOS",
                        "Web"
                    ],
                    "pm": {
                        "id": 1,
                        "name": "오창한",
                        "part_index": 1
                    }
                },
                {
                    "id": 1,
                    "type": 0,
                    "name": "PCube+",
                    "is_end": False,
                    "start_date": "2022-05-27 00:00:00.000Z",
                    "end_date": "2022-05-27 00:00:00.000Z",
                    "tags": [
                        "2D",
                        "etc",
                        "etc",
                    ],
                    "members": [
                        {
                            "id": 1,
                            "name": "오창한",
                            "part_index": 1
                        },
                        {
                            "id": 2,
                            "name": "조승빈",
                            "part_index": 1
                        },
                    ],
                    "platform": [
                        "Android",
                        "iOS",
                        "Web"
                    ],
                    "pm": {
                        "id": 1,
                        "name": "오창한",
                        "part_index": 1
                    }
                }
            ],
            "promotion_progress": {
                "semester": False,
                "curriculum": {
                    "completed": False,
                    "current_curriculum": "커리큘럼 이름",
                    "start_date": "2022-05-27 00:00:00.000Z",
                    "end_date": "2022-05-27 00:00:00.000Z",
                },
                "progress": 0.5,
                "project": {
                    "attended": False,
                    "type": 0
                },
                "workshop": {
                    "count": 1,
                    "complete": False
                },
                "vote": False,
            },
            "recent_seminar": [
                {
                    "id": 1,
                    "type": 0,
                    "date": "2020-05-27 00:00:00.000",
                    "description": "",
                },
                {
                    "id": 1,
                    "type": 0,
                    "date": "2020-05-27 00:00:00.000",
                    "description": "",
                },
            ],
            "caution_list": [
                {
                    "id": 1,
                    "type": 0,
                    "warning_amount": 1.0,
                    "description": "A 사유 어쩌고 저쩌고",
                    "date": "2022-05-27 00:00:00.000"
                },
                {
                    "id": 1,
                    "type": 0,
                    "warning_amount": 1.0,
                    "description": "A 사유 어쩌고 저쩌고",
                    "date": "2022-05-27 00:00:00.000"
                }
            ],
        }

        return data


@oauth.route("/user/notification", methods=['GET'])
class UserNotification(Resource):
    def user_notification(self):
        data = {
            "notification_list": [
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
        }

        return data
