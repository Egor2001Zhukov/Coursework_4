from typing import Generic, List, Optional, TypeVar

from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound
from project.setup.db.models import Base

T = TypeVar('T', bound=Base)

# сюда мы подаем класс MovieDAO
class BaseDAO(Generic[T]):
    # модель ставит по умолчанию модель Base
    __model__ = Base
    # принимает начало сессии базы данных
    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    def get_by_id(self, pk: int) -> Optional[T]:
        return self._db_session.query(self.__model__).get(pk)

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__)
        try:
            if page:
                if status =="new":
                    stmt = stmt.order_by(desc(self.__model__.year))
                return stmt.paginate(page, self._items_per_page).items
            elif status =="new":
                return stmt.order_by(desc(self.__model__.year)).all()
            else:
                return stmt.all()
        except NotFound:
            return []
    #
    # def create(self, data: dict) -> None:
    #     base_object: Base = self.__model__(**data)
    #     self._db_session.add(base_object)
    #     self._db_session.commit()
    #
    # def delete(self, pk: int) -> None:
    #     base_object: Optional[T] = self.get_by_id(pk)
    #     self._db_session.delete(base_object)
    #     self._db_session.commit()

