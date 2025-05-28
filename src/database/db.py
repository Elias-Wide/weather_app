from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from config import settings
from database.models import Base

sqlite_database = f"sqlite:///{settings.db_name}.sqlite"

engine = create_engine(sqlite_database)
session_maker = sessionmaker(engine)


def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)
