from numbers import Real
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


class Favorites(Base):
    """Favorites city db model."""

    name = Column(String, nullable=False)
    lat = Column(String, nullable=False)
    lon = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("name", "lat", "lon", name="unique_favorites"),
    )
