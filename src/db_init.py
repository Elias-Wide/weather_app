import os
from posixpath import abspath, dirname
import sys
from src.database.db import create_db_and_tables, sqlite_database
from src.config import settings


def is_local_db_exists(db_path: str) -> bool:
    """
    Checks if the local database file exists.

    Args:
        db_path (str): The path to the database file.

    Returns:
        bool: True if the database file exists, False otherwise.
    """
    return os.path.exists(os.path.abspath(".") + f"/{settings.db_name}.db")


def init_database(db_path: str = sqlite_database) -> None:
    if is_local_db_exists(db_path):
        print("Local database exists.")
        return
    else:
        create_db_and_tables()
        print("Local database does not exist." "creating DB...")
