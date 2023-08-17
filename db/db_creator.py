"""
This file contains function, which creates DB.

File should be run only once - when you need to create DB.
"""


from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists, create_database, drop_database

from constants.credentials import URL


def create_db(url=URL):
    engine = create_engine(url)

    if database_exists(engine.url):
        drop_database(engine.url)

    if not database_exists(engine.url):
        create_database(engine.url)

create_db()
