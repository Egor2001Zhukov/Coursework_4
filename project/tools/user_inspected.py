import jwt
from flask import request, abort, current_app


def user_inspected():
    data = request.headers['Authorization']
    token = data.split('Bearer ')[-1]
    user = jwt.decode(token, current_app.config["JWT_SECRET"], current_app.config["JWT_ALGORITHM"])
    return user.get('email', 'user')


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        try:
            jwt.decode(token, current_app.config["JWT_SECRET"], current_app.config["JWT_ALGORITHM"])
            return func(*args, **kwargs)
        except jwt.exceptions.DecodeError:
            print('Error JWT DECODE')
            abort(401)



    return wrapper
