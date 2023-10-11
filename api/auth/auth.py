from flask_restx import Resource
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from flask_restx import Resource, Namespace
from flask import request

auth = Namespace('auth')

@auth.route('/token/refresh')
@auth.response(401, 'Unauthorized')
class TokenAPI(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, args, kwargs)

    @jwt_required(refresh=True)
    @auth.doc(security='apiKey')
    def get(self):
        # refresh token으로 갱신
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        token = { 'access_token': access_token, 'refresh_token': refresh_token }
        return token, 200

@auth.route('token/test')
class TokenTestAPI(Resource):
    @auth.expect(auth.parser().add_argument('user_id', type=str, help='유저 ID'), validate=True)
    def get(self):
        user_id = request.args['user_id']
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        token = { 'access_token': access_token, 'refresh_token': refresh_token }
        return token, 200