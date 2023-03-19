from project.dao.main import UserDAO
from project.tools.security import generate_password_hash


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_by_email(self, email):
        return self.dao.get_by_email(email)

    def get_profile(self):
        return self.dao.get_profile()

    def update(self, user_d):
        self.dao.update_user(user_d)

    def update_password(self, user_d):
        user_d["password"] = generate_password_hash(user_d["password"])
        self.dao.update_password(user_d)

    def delete_user(self, uid):
        self.dao.delete_user(uid)

    def add_favorite_movie(self, movie_id):
        return self.dao.add_favorite_movie(movie_id)

    def delete_favorite_movie(self, movie_id):
        return self.dao.delete_favorite_movie(movie_id)

    def get_favorite_movie(self):
        return self.dao.get_favorite_movies()