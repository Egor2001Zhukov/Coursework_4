from typing import Dict

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import scoped_session

from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie, User, user_movie
from project.tools.user_inspected import user_inspected


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorDAO(BaseDAO[Director]):
    __model__ = Director


class MovieDAO(BaseDAO[Movie]):
    __model__ = Movie


class UserDAO:

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).one()

    def get_profile(self):
        email = user_inspected()
        return self.get_by_email(email)

    def create_user(self, user_d: Dict):
        user = User(**user_d)
        self._db_session.add(user)
        self._db_session.commit()
        return '', 401

    def update_user(self, user_d):
        email = user_inspected()
        user = self.get_by_email(email)
        if "name" in user_d:
            user.name = user_d.get("name")
        if "surname" in user_d:
            user.surname = user_d.get("surname")
        self._db_session.add(user)
        self._db_session.commit()

    def update_password(self, user_d):
        user_email = user_inspected()
        user = self.get_by_email(user_email)
        user.password = user_d.get("password")
        self._db_session.add(user)
        self._db_session.commit()

    def delete_user(self, email):
        user = self.get_by_email(email)
        self._db_session.add(user)
        self._db_session.commit()

    def add_favorite_movie(self, movie_id):
        user_email = user_inspected()
        user = self.get_by_email(user_email)
        movie = self._db_session.query(Movie).filter(Movie.id == movie_id).one()
        result = self._db_session.query(user_movie).filter_by(movie_id=movie.id, user_id=user.id).first()
        if result:
            return f'Movie is already to add to favorites movies'
        else:
            try:
                query = user_movie.insert().values(movie_id=movie.id, user_id=user.id)
                self._db_session.execute(query)
                self._db_session.commit()
                return f'Movie added to favorites movies'
            except Exception:
                return f'No movie with id = {movie_id}'

    def get_favorite_movies(self):
        user_email = user_inspected()
        user = self.get_by_email(user_email)
        query = user_movie.select().where(user_movie.c.user_id == user.id)
        result = self._db_session.execute(query)
        list_of_favorites_movie =[]
        for movie_id in result:
            movie = self._db_session.query(Movie).filter(Movie.id == movie_id[0]).one()
            list_of_favorites_movie.append(movie)
        return list_of_favorites_movie

    def delete_favorite_movie(self, movie_id):
        user_email = user_inspected()
        user = self.get_by_email(user_email)
        movie = self._db_session.query(Movie).filter(Movie.id == movie_id).one()
        query = user_movie.delete().where(user_movie.c.movie_id == movie.id).where(user_movie.c.user_id == user.id)
        self._db_session.execute(query)
        self._db_session.commit()
