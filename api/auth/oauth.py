import configparser
import requests
import hashlib
import re
from flask import Flask, request
from flask_restx import Resource, Namespace
from flask_jwt_extended import (
    create_access_token, create_refresh_token
)
from database.database import Database

config = configparser.ConfigParser()
config.read('config/config.ini', encoding='utf-8')

client_id = config['naver_login']['client_id']
client_secret = config['naver_login']['client_secret']

oauth = Namespace('oauth')

@oauth.route("/naver/login")
class NaverLogin(Resource):
    def get(self):
        # 네이버 토큰 검증
        naver_token = request.args.get('refresh_token')
        params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': naver_token,
            'grant_type': 'refresh_token',
            'service_provider': 'NAVER'
        }
        naver_request = requests.post(
            "https://nid.naver.com/oauth2.0/token", params=params)
        naver_data = naver_request.json()
        if 'access_token' not in naver_data.keys():
            return { 'message': '네이버 로그인에 실패했어요 :(' }, 401
        
        # 필요한 데이터 검증
        naver_identifier = request.args.get('identifier')
        if naver_identifier is None or naver_identifier == '':
            return { 'message': '네이버 로그인에 실패했어요 :(' }, 401
        name = request.args.get('name')
        if name is None or name == '':
            return { 'message': '네이버 로그인에 실패했어요 :(' }, 401
        phone_number = request.args.get('phone_number')
        if phone_number is None or phone_number == '':
            return { 'message': '네이버 로그인에 실패했어요 :(' }, 401
        phone_number = re.sub(r'\D', '', phone_number)
        phone_number = re.sub(r'(\d{3})(\d{4})(\d{4})', r'\1-\2-\3', phone_number)

        # 데이터로 유저 정보 조회
        user_id = hashlib.sha256(name.encode('utf-8') + phone_number.encode('utf-8')).hexdigest()
        database = Database()
        sql = f"SELECT is_signed FROM users WHERE id = '{user_id}';"
        is_signed = database.execute_one(sql)
        if is_signed is None:
            database.close()
            return { 'message': '판도라큐브 회원 정보가 없어요 :(' }, 401
        
        # 토큰 생성
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        token = { 'access_token': access_token, 'refresh_token': refresh_token }
        
        # 판도라큐브 회원인 경우에 대한 처리
        is_signed = is_signed['is_signed']
        if is_signed:
            # 이미 PCube+에 가입한 경우에는 로그인으로 처리
            database.close()
            return token, 200
        
        # 처음 가입하는 경우
        sql = f"INSERT INTO identifier VALUES('{naver_identifier}', '{user_id}', 0);"
        database.execute(sql)
        sql = f"UPDATE users SET is_signed = 1 WHERE id = '{user_id}';"
        database.execute(sql)
        database.commit()
        database.close()
        
        return token, 200

@oauth.route("/naver/leave")
class NaverLoginLeave(Resource):
    def post(self):
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
