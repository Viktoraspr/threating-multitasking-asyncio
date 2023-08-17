"""
This file contains class for extracting data from DB.
"""

from datetime import date, timedelta, datetime

from db.DB_management import DBConnection


class DataAnalysis(DBConnection):
    """
    Class contains different methods to extract data from DB.
    """
    def __init__(self):
        super().__init__()
        self.today = date.today()

    def get_max_min_st_dev_values(self) -> dict:
        """
        Method returns maximum, minimum, and standard deviation of temperatures per country and city for today,
        yesterday, current week, and last seven days.
        :return: dictionary format, where key is period, values: list(country, city, minimum, maximum,
        standard deviation). If city is None, then it's country's data.
        """
        monday = self.today - timedelta(days=self.today.weekday())

        dates = {
            'today': (self.today, self.today + timedelta(1)),
            'yesterday': (self.today-timedelta(1), self.today),
            'current_week': (monday, self.today + timedelta(1)),
            'last_7_days': (self.today-timedelta(6), self.today),
        }

        result = {}
        for key, value in dates.items():
            sql_query = f"""
            select cities.country, cities.city, min(weather.temperature), 
            max(weather.temperature), round(stddev(weather.temperature), 2) 
                from weather
                join cities ON cities.city_id = weather.city_id
                where date >= '{value[0]} 00:00:00' 
                and  date <  '{value[1]} 00:00:00'
                group by rollup(cities.country, cities.city)
                order by cities.country;
            """
            result[key] = self.get_data_with_sql_query(sql_query=sql_query)
        return result

    def indicate_cities_with_highest_lowest_temperature_per_hour(self, start_period: datetime = date.today(),
                                                                 end_period: datetime = date.today()) -> dict:
        """
        Returns dictionary, where keys are 'min_temperature' and 'max_temperature', result list of tuples,
        the tuple contains city, date(year, month, day, hour) and temperature.
        :param start_period: date (datetime format) without hours.
        :param end_period: date (datetime format) without hours.
        :return: dictionary with minimum and maximum temperature, city and hour.
        """

        min_temp_sql = f"""
        select cities.city, minimum.hours, minimum.temper
        from (select min(temperature) as temper, date_trunc('hour', date) as hours, city_id,
        rank() over (partition by date_trunc('hour', date) order by min(temperature)) rank_rank
        from weather
        where date >= '{start_period} 00:00:00' and  date <  '{end_period + timedelta(1)} 00:00:00'
        group by hours, city_id) minimum
        join cities on cities.city_id = minimum.city_id
        where minimum.rank_rank = 1;
        """

        max_temp_sql = f"""
        select cities.city, maximum.hours, maximum.temper
                from (select max(temperature) as temper, date_trunc('hour', date) as hours, city_id,
        rank() over (partition by date_trunc('hour', date) order by max(temperature) desc) rank_rank
        from weather
        where date >= '{start_period} 00:00:00' and  date <  '{end_period + timedelta(1)} 00:00:00'
        group by hours, city_id) maximum
                join cities on cities.city_id = maximum.city_id
                where maximum.rank_rank = 1;
        """

        result = {
            'min_temperature': self.get_data_with_sql_query(sql_query=min_temp_sql),
            'max_temperature': self.get_data_with_sql_query(sql_query=max_temp_sql),
        }
        return result

    def indicate_cities_with_highest_lowest_temperature_per_day(self, start_period: datetime = date.today(),
                                                                end_period: datetime = date.today()) -> dict:
        """
        Returns dictionary, where keys are 'min_temperature' and 'max_temperature', result list of tuples,
        the tuple contains city, date(year, month, day) and temperature.
        :param start_period: date (datetime format) without hours.
        :param end_period: date (datetime format) without hours.
        :return: dictionary with minimum and maximum temperature, city and day.
        """
        max_temp_sql = f"""
        select cities.city, maximum.days, maximum.temper
        from (select max(temperature) as temper, CAST(weather.date AS DATE) as days, city_id,
            rank() over (partition by CAST(weather.date AS DATE) order by max(temperature) desc) rank_rank
            from weather
            where date >= '{start_period} 00:00:00' and  date <  '{end_period+timedelta(1)} 00:00:00'
        group by days, city_id) maximum
        join cities on cities.city_id = maximum.city_id
        where maximum.rank_rank = 1
        order by maximum.days desc;
        """

        min_temp_sql = f"""
        select cities.city, minimum.days, minimum.temper
        from (select min(temperature) as temper, CAST(weather.date AS DATE) as days, city_id,
            rank() over (partition by CAST(weather.date AS DATE) order by min(temperature)) rank_rank
            from weather
            where date >= '{start_period} 00:00:00' and  date <  '{end_period+timedelta(1)} 00:00:00'
            group by days, city_id) minimum
        join cities on cities.city_id = minimum.city_id
        where minimum.rank_rank = 1
        order by minimum.days desc;
        """

        result = {
            'min_temperature': self.get_data_with_sql_query(sql_query=min_temp_sql),
            'max_temperature': self.get_data_with_sql_query(sql_query=max_temp_sql),
        }
        return result

    def indicate_cities_with_highest_lowest_temperature_per_week(self, start_week: int = date.today().isocalendar()[1],
                                                                 end_week: int = date.today().isocalendar()[1]) -> dict:
        """
        Returns dictionary, where keys are 'min_temperature' and 'max_temperature', result list of tuples,
        the tuple contains city, week number and temperature
        :param start_week: date (datetime format) without hours.
        :param end_week: date (datetime format) without hours.
        :return: dictionary with minimum and maximum temperature, city and week number.
        """
        max_temp_sql = f"""
        select cities.city, maximum.week, maximum.temper
                from (select max(temperature) as temper, DATE_PART('week', weather.date) as week, city_id,
        rank() over (partition by DATE_PART('week', weather.date) order by max(temperature) desc) rank_rank
        from weather
        where DATE_PART('week', weather.date) >= 32 and DATE_PART('week', weather.date) < 33
        group by week, city_id) maximum
                join cities on cities.city_id = maximum.city_id
                where maximum.rank_rank = 1
        order by maximum.week desc;
        """

        min_temp_sql = f"""
        select cities.city, minimum.week, minimum.temper
        from (select min(temperature) as temper, DATE_PART('week', weather.date) as week, city_id,
            rank() over (partition by DATE_PART('week', weather.date) order by min(temperature)) rank_rank
            from weather
            where DATE_PART('week', weather.date) >= {start_week} and DATE_PART('week', weather.date) < {end_week + 1}
            group by week, city_id) minimum
        join cities on cities.city_id = minimum.city_id
        where minimum.rank_rank = 1
        order by minimum.week desc;
        """

        result = {
            'min_temperature': self.get_data_with_sql_query(sql_query=min_temp_sql),
            'max_temperature': self.get_data_with_sql_query(sql_query=max_temp_sql),
        }
        return result

    def get_number_hours_of_description(self, description: str = 'Rain', city: str = None) -> dict:
        """
        returns number of hours. Default description - 'Rain'.  It can return one city or all cities.
        :param description: weather description. Default - "Rain'
        :param city: city, default - None.
        :return: dictionary with two keys: 'last_day', 'last_week'. Value - counted hours.
        """
        city_sql = ''
        if city:
            city_sql = f"cities.city like '{city}' and "

        # The number of times (hours) it rained in the last day and week.
        sql_last_day = f"""
        select count(*)
        from (select date_trunc('hour', date) as hours
        from weather
        join cities on cities.city_id = weather.city_id 
        where {city_sql}weather.description like '{description}' 
        and date >= '{self.today - timedelta(1)} 00:00:00' and date < '{self.today} 00:00:00') weath;
        """

        first_week_day = self.today - timedelta(days=self.today.weekday(), weeks=1)
        last_week_day = self.today - timedelta(days=self.today.weekday(), weeks=0)

        sql_last_week = f"""
                select count(*)
                from (select date_trunc('hour', date) as hours
                from weather
                join cities on cities.city_id = weather.city_id 
                where {city_sql}weather.description like '{description}' 
                and date >= '{first_week_day} 00:00:00' and date < '{last_week_day} 00:00:00') weath;
                """

        result = {
            'last_day': self.get_data_with_sql_query(sql_query=sql_last_day)[0][0],
            'last_week': self.get_data_with_sql_query(sql_query=sql_last_week)[0][0],
        }

        return result
