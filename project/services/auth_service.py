import calendar
import datetime

import jwt
from flask import current_app, abort

from project.dao.main import UserDAO
from project.tools.security import compare_passwords, generate_password_hash


class AuthService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def generate_tokens(self, email, password, is_refresh=False):
        user = self.dao.get_by_email(email)
        if user is None:
            abort(404)

        if not is_refresh:
            if not compare_passwords(user.password, password):
                abort(400)

        data = {'email': user.email}

        # access token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, current_app.config["JWT_SECRET"], current_app.config["JWT_ALGORITHM"])
        # refresh token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, current_app.config["JWT_SECRET"], current_app.config["JWT_ALGORITHM"])

        return {"access_token": access_token, "refresh_token": refresh_token}

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(refresh_token, current_app.config["JWT_SECRET"],
                          current_app.config["JWT_ALGORITHM"])
        email = data.get("email")

        return self.generate_tokens(email, None, is_refresh=True)

    def create_user(self, user_d):
        user_d["password"] = generate_password_hash(user_d["password"])
        return self.dao.create_user(user_d)
