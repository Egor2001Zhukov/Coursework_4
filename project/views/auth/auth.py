import calendar
import datetime

import jwt
from flask import current_app, request
from flask_restx import Namespace, abort, Resource

from project.container import auth_service

api = Namespace('auth')


@api.route('/login/')
class AuthView(Resource):
    def post(self):
        auth_data = request.json
        email = auth_data.get("email")
        password = auth_data.get("password")

        if None in [email, password]:
            return "", 400

        tokens = auth_service.generate_tokens(email, password)
        return tokens

    def put(self):
        auth_data = request.json
        token = auth_data.get("refresh_token")
        tokens = auth_service.approve_refresh_token(token)
        return tokens


@api.route('/register/')
class AuthView(Resource):
    def post(self):
        auth_data = request.json
        email = auth_data.get("email")
        password = auth_data.get("password")

        if None in [email, password]:
            return "", 400

        auth_service.create_user(auth_data)
        return "", 201


