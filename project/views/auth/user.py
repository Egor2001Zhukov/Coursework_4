from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user, movie
from project.tools.user_inspected import auth_required

api = Namespace('user')


@api.route('/')
class UserView(Resource):
    @api.marshal_with(user, code=200, description='OK')
    @auth_required
    def get(self):
        return user_service.get_profile()

    @auth_required
    def patch(self, email):
        user_d = request.json
        user_service.update(email, user_d)
        return "", 200


@api.route('/password/')
class ChangePassword(Resource):
    def put(self):
        user_d = request.json
        user_service.update_password(user_d)
        return "", 200


@api.route('/favorites/movies/')
class GetFM(Resource):
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    @auth_required
    def get(self):
        return user_service.get_favorite_movie(), 200


@api.route('/favorites/movies/<int:movie_id>/')
class AddDeleteFM(Resource):

    @auth_required
    def post(self, movie_id):
        return user_service.add_favorite_movie(movie_id), 200

    @auth_required
    def delete(self, movie_id):
        user_service.delete_favorite_movie(movie_id)
        return "", 200
