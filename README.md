# vipranc-DE2.2

# Introduction

With this project, you can create DB, retrieve data using API to DB, and also there are several functions for analytic information requiring. 

It requires Python >=3.9

# Development

## Writing source code

Consider follow:
* [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## Installation

Create a virtual environment:

    python -m venv .venv

Install package:

    pip install -r requirements.txt

# Project structure


constants/credentials.py - need to add credentials of Postgres DB. 
db/db_creator.py - creates DB if it does not exist.
db/models.py- creates tables in db.


Several runs files:
run_fake_data_injection_in_db.py - inject fake data for 30 days in DB.
run_threading.py - multiple threads concurrently.
run_analysis.py - demonstration analysis methods.
run_all_retrieval_methods.py - run coroutines, threads, and processes methods.
