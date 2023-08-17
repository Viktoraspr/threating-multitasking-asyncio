"""
File contains class, which is used for job with DB.
"""

from typing import Type, Sequence
from datetime import datetime

from sqlalchemy import create_engine, Row
from sqlalchemy.engine.result import _TP
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from constants.cities import CITIES
from constants.credentials import URL

from .models import City, Weather


class DBConnection:
    """
    Class uses SQLAlchemy tools for CRUD operation.
    """
    def __init__(self, url=URL):
        self.url = url
        self.engine = create_engine(self.url)

    def write_data_in_cities_table(self, cities: dict = CITIES) -> None:
        """
        Method adds cities to DB
        :param cities: city must be dictionary format: key should be string format and looks like: 'Istanbul,
        Turkey' (city, country), value - iterable (10_241_510, 41.01, 28.95) (population, latitude, longitude),
        :return: None
        """

        values_for_db = []
        for city, value in cities.items():
            c, country = city.split(', ')
            lat, lon = value[1:]

            values_for_db.append(City(
                city=c,
                country=country,
                lon=lat,
                lat=lon,
            ))

        # Adding to DB
        with Session(self.engine) as session:
            session.add_all(values_for_db)
            session.commit()

    def get_cities_from_db(self) -> list[Type[City]]:
        """
        Gets cities and their info from DB
        :return: List of cities
        """
        with Session(self.engine) as session:
            cities = session.query(City).all()
        return cities

    def add_weather_to_db(self, city_id: int, temperature: int, description: str, date: datetime = None):
        """
        Adding data to weather table in database
        :param city_id: city id (as in table cities)
        :param temperature: current temperature in the city
        :param description: weather description
        :param date: date
        :return: None
        """
        weather = Weather(
            city_id=city_id,
            temperature=temperature,
            description=description,
            date=date
        )
        with Session(self.engine) as session:
            session.add(weather)
            session.commit()

    def get_data_with_sql_query(self, sql_query: str) -> Sequence[Row[_TP]]:
        """
        Returns data from database
        :param sql_query: sql query
        :return: data
        """
        with self.engine.connect() as conn:
            data = conn.execute(text(sql_query))
        return data.fetchall()
