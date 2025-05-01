from sqlalchemy import Column, Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, declared_attr


class PreBase:
    """
    Prebase class.
    Creating tablename and column ID (primary key).
    """

    @declared_attr
    def __tablename__(cls) -> str:
        """Returning tablename in lowercase."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)


class Base(DeclarativeBase, PreBase):
    pass


class WeatherConditions(Base):

    code = Column(Integer, unique=True)
    day = Column(String, nullable=False)
    night = Column(String, nullable=False)


class Favorites(Base):
    """Favorites city db model."""

    region = Column(String, nullable=False)
    country = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "region", "country", "lat", "lon", name="unique_favorites"
        ),
    )
