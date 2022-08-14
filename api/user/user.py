import requests
from flask import Flask, redirect, request
from flask_restx import Resource, Api, Namespace

user = Namespace('user')

@user.route("/profile")
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

@user.route("/notification")
class UserNotification(Resource):
    def get(self):
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