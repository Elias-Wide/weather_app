from src.database.db import create_db_and_tables
from src.parse_api import (
    get_conditions_from_api,
    insert_weather_conditions_data,
)


create_db_and_tables()
insert_weather_conditions_data(get_conditions_from_api())
