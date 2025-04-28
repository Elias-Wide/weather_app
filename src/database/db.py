from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker

from src.database.models import Base, Favorites, WeatherKeys

sqlite_database = "sqlite:///app_db.db"

engine = create_engine(sqlite_database, echo=True)
session_maker = sessionmaker(engine)


class PreBase:
    """
    Prebase class.
    Creating tablename and column ID (primary key).
    """

    @declared_attr
    def __tablename__(cls) -> str:
        """Returning tablename in lowercase."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)
