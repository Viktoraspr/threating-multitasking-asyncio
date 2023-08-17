"""
File contains function to generate fake weather data.

Result format looks similar as in from https://openweathermap.org/api/one-call-3.
"""
import random
import time

from constants.constants import WEATHER_MAIN


def get_weather_fake(lon: float, lat: float) -> dict:
    """
    Function generates fake current weather
    :param lon: lon - longitude  of planet
    :param lat: - latitude of planet
    :return: Current weather in dictionary format. The dict sample is from https://openweathermap.org/api/one-call-3.
    """
    # Time sleep is used for imitation time for API request
    # time.sleep(1)
    result = {
          "coord": {
            "lon": lon,
            "lat": lat,
          },
          "weather": [
            {
              "id": 501,
              "main": random.choice(WEATHER_MAIN),
              "description": "moderate rain",
              "icon": "10d"
            }
          ],
          "base": "stations",
          "main": {
            "temp": random.randint(-5, 40),
            "feels_like": 298.74,
            "temp_min": 297.56,
            "temp_max": 300.05,
            "pressure": 1015,
            "humidity": 64,
            "sea_level": 1015,
            "grnd_level": 933
          },
          "visibility": 10000,
          "wind": {
            "speed": 0.62,
            "deg": 349,
            "gust": 1.18
          },
          "rain": {
            "1h": 3.16
          },
          "clouds": {
            "all": 100
          },
          "dt": 1661870592,
          "sys": {
            "type": 2,
            "id": 2075663,
            "country": "IT",
            "sunrise": 1661834187,
            "sunset": 1661882248
          },
          "timezone": 7200,
          "id": 3163858,
          "name": "Zocca",
          "cod": 200
        }

    return result
