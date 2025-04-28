from datetime import datetime
from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import and_, insert, select
from sqlalchemy.exc import SQLAlchemyError

from src.database.db import session_maker
from src.database.models import Base, Favorites, WeatherConditions


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
                return object_to_delete
            except:
                return None

    @classmethod
    def get_multi(cls):
        with session_maker() as session:
            db_objs = session.execute(select(cls.model))
            return db_objs.scalars().all()


class FavoritesDAO(BaseDAO):
    model = Favorites

    @classmethod
    def get_favorites_city(cls, name: str, api_id: int):
        with session_maker() as session:
            db_objs = session.execute(
                select(cls.model).filter(
                    cls.model.name == name, cls.model.api_id == api_id
                )
            )
            return db_objs.scalars().first()


class WeatherConditionsDAO(BaseDAO):
    model = WeatherConditions
