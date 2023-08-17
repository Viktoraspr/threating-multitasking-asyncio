"""
Checks received data
"""

from datetime import datetime, timedelta

from management.data_entry import DataCreator

data = DataCreator()

today = datetime.today()

for days in range(30, -1, -1):
    day = datetime.today() - timedelta(days)
    for hour in range(24):
        data_date = datetime(year=day.year, month=day.month, day=day.day, hour=hour, minute=1)
        data.run_threading(date=data_date)
