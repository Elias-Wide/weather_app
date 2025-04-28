from datetime import datetime
from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import and_, insert, select
from sqlalchemy.exc import SQLAlchemyError

from src.database.db import session_maker
from src.database.models import Base


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
                query = (
                    insert(cls.model).values(**data).returning(cls.model.id)
                )
                object = session.execute(query)
                session.commit()
                return object.mappings().first()
            except (SQLAlchemyError, Exception) as error:
                session.rollback()
                if isinstance(error, SQLAlchemyError):
                    message = "Database Exception"
                elif isinstance(error, Exception):
                    message = "Unknown Exception"
                message += ": Не удается добавить данные."
                print(message)

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
