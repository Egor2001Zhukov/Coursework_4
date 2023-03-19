from project.dao import GenresDAO
from project.dao.main import DirectorDAO, MovieDAO, UserDAO

from project.services import GenresService, AuthService
from project.services.directors_service import DirectorsService
from project.services.movies_service import MoviesService
from project.services.user_service import UserService
from project.setup.db import db

# DAO
user_dao = UserDAO(db.session)
genre_dao = GenresDAO(db.session)
director_dao = DirectorDAO(db.session)
movie_dao = MovieDAO(db.session)

# Services
user_service = UserService(user_dao)
auth_service = AuthService(dao=user_dao)
genre_service = GenresService(dao=genre_dao)
director_service = DirectorsService(dao=director_dao)
movie_service = MoviesService(dao=movie_dao)
