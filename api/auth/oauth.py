from lib2to3.pgen2 import token
import requests
from flask import Flask, redirect, request
from flask_restx import Resource, Api, Namespace
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini', encoding='utf-8')

client_id = config['naver_login']['client_id']
client_secret = config['naver_login']['client_secret']

oauth = Namespace('oauth')

@oauth.route("/naver/login")
class NaverLogin(Resource):
    def get(self):
        redirect_uri = "http://p-cube-plus.com/oauth/naver/callback"
        url = f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        return redirect(url)

@oauth.route("/naver/callback")
class NaverLoginCallback(Resource):
    def get(self):
        params = request.args.to_dict()
        code = params.get("code")

        token_request = requests.get(
            f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}")
        token_json = token_request.json()

        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://openapi.naver.com/v1/nid/me", headers={"Authorization": f"Bearer {access_token}"},)
        profile_data = profile_request.json()

        redirect_url = ("p_cube_plus://success?"
                        "access_token=" + token_json.get('access_token') + "&"
                        "refresh_token=" + token_json.get('refresh_token') + "&"
                        "expires_in=" + token_json.get('expires_in'))

        return redirect_url

@oauth.route("/naver/leave", methods=['GET'])
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
