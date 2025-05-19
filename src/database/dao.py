from sqlalchemy import and_, insert, select
from sqlalchemy.exc import SQLAlchemyError
from typing import Generic, TypeVar

from constants import WEATHER_ICONS_PATH
from src.config import settings
from src.database.db import session_maker
from src.database.models import Base, Favorites

from cachetools import cached, TTLCache


favorites_cache = TTLCache(maxsize=100, ttl=120)
ModelType = TypeVar("ModelType", bound=Base)


class BaseDAO(Generic[ModelType]):

    model = None

    @classmethod
    def create(
        cls,
        data: dict,
    ) -> ModelType:
        with session_maker() as session:
            try:
                query = insert(cls.model).values(**data)
                object = session.execute(query)
                session.commit()
            except (SQLAlchemyError, Exception) as error:
                session.rollback()
                if isinstance(error, SQLAlchemyError):
                    message = "Database Exception"
                elif isinstance(error, Exception):
                    message = "Unknown Exception"
                message += ": Не удается добавить данные."
                print(message + str(error))

    @classmethod
    def delete_object(cls, **kwargs):
        with session_maker() as session:
            try:
                query = select(cls.model).filter_by(**kwargs)
                result = session.execute(query)
                result = result.scalar()
                object_to_delete = result
                if not result:
                    raise None
                session.delete(result)
                session.commit()
                print("SUCCES DELETE")
                return True
            except:
                print("DELETE ERROR")
                return None

    @classmethod
    def get_multi(cls):
        with session_maker() as session:
            db_objs = session.execute(select(cls.model))
            return db_objs.scalars().all()

    @classmethod
    @cached(cache=favorites_cache)
    def get_favorites_by_page(cls, page: int = 1, page_size: int = 6):
        """
        Returns a tuple (items, total_count, has_prev, has_next) for pagination.

        Args:
            page (int): The page number (1-based).
            page_size (int): The number of items per page.

        Returns:
            tuple: (items: list[Favorites], total_count: int, has_prev: bool, has_next: bool)
        """
        with session_maker() as session:
            total_count = session.query(cls.model).count()
            items = (
                session.query(cls.model)
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all()
            )
            return items, total_count


class FavoritesDAO(BaseDAO):
    model = Favorites

    @classmethod
    def get_fav_city(
        cls,
        name: str,
        lat: float,
        lon: float,
    ):
        with session_maker() as session:
            db_objs = session.execute(
                select(cls.model).filter(
                    cls.model.name == name,
                    cls.model.lat == lat,
                    cls.model.lon == lon,
                )
            )
            return db_objs.scalars().first()
