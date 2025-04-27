from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, declared_attr


# from src.database.db import Base
class PreBase:
    """Родительский класс для базового."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Возвращает имя для таблицы в нижнем регистре."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class Base(DeclarativeBase, PreBase):
    pass


class WeatherKeys(Base):

    key = Column(Integer, primary_key=True)
    image_name = Column(String)


class Favorites(Base):
    """Favorites city db model."""

    name = Column(String, nullable=False)
    api_id = Column(Integer, nullable=False)
