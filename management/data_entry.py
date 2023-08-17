"""This file contains one class, for getting data from the source and adding data to DB"""

import asyncio
import multiprocessing
import threading
from datetime import datetime
from constants.constants import WEATHER_MAIN
from db.models import City
from db.DB_management import DBConnection
from weather.fake_weather import get_weather_fake


class DataCreator:
    """
    Class have three different ways to do the same task: threads, processes, and asyncio coroutines.
    """
    db_connection = DBConnection()

    def __init__(self):
        self.cities = self.db_connection.get_cities_from_db()

    @staticmethod
    def __get_weather_on_city(city: City) -> dict:
        """
        Gets data from the source
        :param city: City, which weather should be generated.
        :return: current weather
        """
        return get_weather_fake(city.lon, city.lat)

    def __add_data_to_db(self, city_id: int, temperature: int, description: str, date: datetime = None) -> None:
        """
        Prepares and send a data to the DB management class
        :param city_id: city_id from DB cities table
        :param temperature: temperature, which needs to add to DB
        :param description: weather description
        :return: None
        """
        if description not in WEATHER_MAIN:
            raise 'Not correct weather value'
        if not -60 <= temperature <= 60:
            raise 'Not correct temperature'
        self.db_connection.add_weather_to_db(city_id=city_id, temperature=temperature,
                                             description=description, date=date)

    def get_and_add_weather_to_db(self, city: City, date: datetime = None) -> None:
        """
        Getting a weather and sending a data to DB
        :param city: city
        :param date: date
        :return: None
        """
        weather = self.__get_weather_on_city(city)
        temperature = weather['main']['temp']
        description = weather['weather'][0]['main']
        self.__add_data_to_db(city_id=city.city_id, temperature=temperature, description=description, date=date)

    async def get_and_add_async_weather_to_db(self, city: City) -> int:
        """
        Creates a thread object
        :param city: city
        :return: async thread number
        """
        return await asyncio.to_thread(self.get_and_add_weather_to_db, city)

    def run_threading(self, date: datetime = None) -> None:
        """
        Running a process using threads
        :return: None
        """
        threads = []

        city: City
        for city in self.cities:
            t = threading.Thread(target=self.get_and_add_weather_to_db, args=(city, date))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

    def run_multiprocessing(self):
        """
        Running a process using processes
        :return: None
        """
        processes = []

        city: City
        for city in self.cities:
            process = multiprocessing.Process(target=self.get_and_add_weather_to_db, args=(city,))
            process.start()
            processes.append(process)

        for p in processes:
            p.join()

    async def run_concurrency(self):
        """
        Running a process using coroutines
        :return: None
        """
        cities = self.db_connection.get_cities_from_db()
        city: City
        await asyncio.gather(*[self.get_and_add_async_weather_to_db(city) for city in cities])
