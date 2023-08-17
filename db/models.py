"""
File contains information about tables in database
"""

from datetime import datetime

from sqlalchemy import String, Float, DateTime
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


from constants.credentials import URL

engine = create_engine(URL)

class Base(DeclarativeBase):
    pass


class City(Base):
    """
    Class describe table 'cities' in database
    """
    __tablename__ = "cities"
    city_id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(30))
    country: Mapped[str] = mapped_column(String(60))
    lon: Mapped[float] = mapped_column(Float(decimal_return_scale=2))
    lat: Mapped[float] = mapped_column(Float(decimal_return_scale=2))
    weathers = relationship("Weather", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f'City (id={self.city_id!r}, name={self.city!r})'


class Weather(Base):
    """
       Class describe table 'weather' in database
    """
    __tablename__ = "weather"
    id: Mapped[int] = mapped_column(primary_key=True)
    temperature: Mapped[int]
    description: Mapped[str]
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.city_id'))
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f"Weather(id={self.id!r}, city_id={self.city_id!r})"


Base.metadata.create_all(engine)
