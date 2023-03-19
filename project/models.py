from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import backref, relationship

from project.setup.db import models, db


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    __tablename__ = 'directors'

    name = Column(String(100), unique=True, nullable=False)


class Movie(models.Base):
    __tablename__ = 'movies'

    title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    trailer = Column(String(100), nullable=False)
    year = Column(Integer(), nullable=False)
    rating = Column(Integer(), nullable=False)
    genre_id = Column(Integer(), nullable=False)
    director_id = Column(Integer(), nullable=False)

#
# class UserMovie(db.Model):
#     __tablename__ = 'user_movie'
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     movie_id = Column(Integer, ForeignKey('movie.id'))
#     user = relationship('User', backref=backref('favorite_movies', cascade='all'))
#     movie = relationship('Movie')
#

class User(models.Base):
    __tablename__ = 'users'

    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(), unique=True, nullable=False)
    name = Column(String(100))
    surname = Column(String(100))
    favorite_movies = relationship('Movie', secondary='user_movie', cascade='all')



user_movie = db.Table('user_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


