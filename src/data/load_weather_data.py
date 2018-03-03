"""
Loads the weather data into sqlite database
"""
import sys
import pandas as pd
import glob
import random
import datetime as datetime
from sqlalchemy import create_engine
from tqdm import tqdm
import logging
import data_helper as helper
from collections import namedtuple
import re

def identify_weather_features():
    """ Returns a list of named tuples for each of the features in the dataframe """
    Feature = namedtuple('Feature', ['raw_name', 'storage_name', 'dtype'])
    return [
        Feature(raw_name='STATION', storage_name='station', dtype=str),
        Feature(raw_name='STATION_NAME', storage_name='station_name', dtype=str),
        Feature(raw_name='ELEVATION', storage_name='elevation', dtype=str),
        Feature(raw_name='LATITUDE', storage_name='latitude', dtype=float),
        Feature(raw_name='LONGITUDE', storage_name='longitude', dtype=float),
        Feature(raw_name='DATE', storage_name='date', dtype=datetime.datetime),
        Feature(raw_name='HOURLYVISIBILITY', storage_name='hourly_visibility', dtype=int),
        Feature(raw_name='HOURLYDRYBULBTEMPF', storage_name='hourly_dry_bulb_temp_f', dtype=float),
        Feature(raw_name='HOURLYWETBULBTEMPF', storage_name='hourly_wet_bulb_temp_f', dtype=float),
        Feature(raw_name='HOURLYDewPointTempF', storage_name='hourly_dew_point_temp_f', dtype=float),
        Feature(raw_name='HOURLYRelativeHumidity', storage_name='hourly_relative_humidity', dtype=int),
        Feature(raw_name='HOURLYWindSpeed', storage_name='hourly_wind_speed', dtype=int),
        Feature(raw_name='HOURLYWindDirection', storage_name='hourly_wind_direction', dtype=int),
        Feature(raw_name='HOURLYWindGustSpeed', storage_name='hourly_wind_gust_speed', dtype=int),
        Feature(raw_name='HOURLYStationPressure', storage_name='hourly_station_pressure', dtype=float)
    ]

def parse_weather_data(file_name):
    """Convert a given weather csv into a dataframe for storage"""

    features = identify_weather_features()
    raw_feature_names = [f.raw_name for f in features]
    data = pd.read_csv(file_name, usecols=raw_feature_names)

    for feature in features:
        data.rename(columns={feature.raw_name:feature.storage_name}, inplace=True)
        if feature.dtype in [int, float]:
            data[feature.storage_name] = pd.to_numeric(data[feature.storage_name], errors='coerce') 
        elif feature.dtype == datetime.datetime:
            data[feature.storage_name] = pd.to_datetime(data[feature.storage_name], infer_datetime_format=True)
        else:
            data[feature.storage_name].astype(feature.dtype, copy=False)
   
    data['hourly_wind_gust_speed'] =  data['hourly_wind_gust_speed'].fillna(0)
    data = data.fillna(method='ffill')
    return data

def load_csv_into_database(file_name, path_to_database):
    db_engine = create_engine(path_to_database)

    with db_engine.connect() as connection:
        data = parse_weather_data(file_name)
        data.to_sql('weather', connection, if_exists='append')

def load_weather_data(path_to_database):
    logger = logging.getLogger(__name__)
     # Reverse sort to load most recent years first
    files = sorted(glob.glob("data/raw/weather/*.csv"))

    for f in files:
        logger.info(f'Loading {f} into database')
        load_csv_into_database(f, path_to_database)
        logger.info('Complete...loading next file')

def main():
    """ Parse first file, ensure parse occurs without error"""
    f = sorted(glob.glob("data/raw/weather/*.csv"))[0]
    data = parse_weather_data(f)
    print(data.info())
    print(data.head())

if __name__ == '__main__':
    sys.exit(main())