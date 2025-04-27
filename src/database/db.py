from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker

from src.database.models import Base, Favorites, WeatherKeys

# строка подключения
sqlite_database = "sqlite:///app_db.db"

# создаем движок SqlAlchemy
engine = create_engine(sqlite_database, echo=True)
Session = sessionmaker(engine)


class PreBase:
    """Родительский класс для базового."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Возвращает имя для таблицы в нижнем регистре."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)


create_db_and_tables()
print("База данных и таблица созданы")
