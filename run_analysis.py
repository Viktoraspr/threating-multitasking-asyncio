"""
This file for analysis demonstration
"""

from management.data_analysis import DataAnalysis

data_analysis = DataAnalysis()
print(data_analysis.get_max_min_st_dev_values())
print(data_analysis.indicate_cities_with_highest_lowest_temperature_per_hour())
print(data_analysis.indicate_cities_with_highest_lowest_temperature_per_day())
print(data_analysis.indicate_cities_with_highest_lowest_temperature_per_week())
print(data_analysis.get_number_hours_of_description(city='Rome'))
print(data_analysis.get_number_hours_of_description())
