
import pandas as pd

from data_model import WeatherDataModel, WeatherStatsDataModel


weather_data_model = WeatherDataModel()
weather_stats_data_model = WeatherStatsDataModel()
import numpy as np


def generate_report():
   
    weather_data = weather_data_model.get_data()

    
    weather_data['Year'] = weather_data['Date'].str[:4]

    
    weather_data = weather_data[
        (weather_data['Date'] != -9999) & (weather_data['MaxTemp'] != -9999) & (weather_data['MinTemp'] != -9999) & (
                    weather_data['Precipitation'] != -9999)]

    report = weather_data.groupby([ 'StationID','Year']).agg(
        {'MaxTemp': np.mean, 'MinTemp': np.mean, 'Precipitation': sum}).reset_index()
    
    report[['MaxTemp','MinTemp']] = round(report[['MaxTemp','MinTemp']]/10,2)
    
    report[['Precipitation']] = round(report[['Precipitation']]/100,2)

   
    for index, record in report.iterrows():
        print(weather_stats_data_model.add_entry(tuple(record)))


if __name__ == '__main__':
    generate_report()
