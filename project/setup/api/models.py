from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия')
})

director: Model = api.model('Режиссер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Егор Жуков')
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Егор'),
    'description': fields.String(required=True, example='Егор Жуков'),
    'trailer': fields.String(required=True, example='Егор Жуков'),
    'year': fields.Integer(required=True, example=1),
    'rating': fields.String(required=True, example=1),
    'genre_id': fields.String(required=True, example=1),
    'director_id': fields.String(required=True, example=1)
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=100, example='Егор'),
    'password': fields.String(required=True, example='Егор'),
    'name': fields.String(required=False, max_length=100, example='Егор'),
    'surname': fields.String(required=False, max_length=100, example='Егор'),
    'favorite_genre': fields.String(required=False, max_length=100, example='Егор')
})
