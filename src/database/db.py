from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker


from src.database.models import Base

sqlite_database = "sqlite:///app_db.db"

engine = create_engine(sqlite_database, echo=True)
session_maker = sessionmaker(engine)


def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)
