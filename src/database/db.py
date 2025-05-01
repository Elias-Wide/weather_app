from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from src.config import settings
from src.database.models import Base

sqlite_database = f"sqlite:///{settings.db_name}.db"

engine = create_engine(sqlite_database, echo=True)
session_maker = sessionmaker(engine)


def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)
