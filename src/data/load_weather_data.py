"""
Loads the weather data into sqlite database
"""
from collections import namedtuple
import datetime as datetime
import glob
import logging
import pandas as pd
from sqlalchemy import create_engine
import sys


def identify_weather_features():
    """ Returns a list of named tuples for selected of the features  """
    Feature = namedtuple('Feature', ['raw_name', 'storage_name', 'dtype'])
    return [
        Feature('STATION', 'station', str),
        Feature('STATION_NAME', 'station_name', str),
        Feature('ELEVATION', 'elevation', float),
        Feature('LATITUDE', 'latitude', float),
        Feature('LONGITUDE', 'longitude', float),
        Feature('DATE', 'date', datetime.datetime),
        Feature('HOURLYVISIBILITY', 'hourly_visibility', int),
        Feature('HOURLYDRYBULBTEMPF', 'hourly_dry_bulb_temp_f', float),
        Feature('HOURLYWETBULBTEMPF', 'hourly_wet_bulb_temp_f', float),
        Feature('HOURLYDewPointTempF', 'hourly_dew_point_temp_f', float),
        Feature('HOURLYRelativeHumidity', 'hourly_relative_humidity', int),
        Feature('HOURLYPrecip', 'hourly_precipitation', float),
        Feature('HOURLYWindSpeed', 'hourly_wind_speed', int),
        Feature('HOURLYWindDirection', 'hourly_wind_direction', int),
        Feature('HOURLYWindGustSpeed', 'hourly_wind_gust_speed', int),
        Feature('HOURLYStationPressure', 'hourly_station_pressure', float)
    ]


def parse_weather_data(file_name):
    """Convert a given weather csv into a dataframe for storage"""
    features = identify_weather_features()
    raw_feature_names = [f.raw_name for f in features]
    data = pd.read_csv(file_name, usecols=raw_feature_names, low_memory=False)

    # Rename all features to storage name with snake_case
    for f in features:
        data.rename(columns={f.raw_name: f.storage_name}, inplace=True)

    # Precipitation of 'T' indicates trace amount, set to 0.001 rather than 0
    data['hourly_precipitation'].replace(to_replace='T', value=0.001,
                                         inplace=True)

    # Handle conversion for features to specificed data types
    for f in features:
        # if an element cannot be converted to numeric, set to NA
        if f.dtype in [int, float]:
            data[f.storage_name] = \
                pd.to_numeric(data[f.storage_name], errors='coerce')

        # convert datetime features
        elif f.dtype == datetime.datetime:
            data[f.storage_name] = \
              pd.to_datetime(data[f.storage_name], infer_datetime_format=True)
        # handle string types
        else:
            data[f.storage_name] = data[f.storage_name].astype(f.dtype)

    # for missing wind gusts, assume zero
    data['hourly_wind_gust_speed'] = \
        data['hourly_wind_gust_speed'].fillna(0)
    # for missing precipitation, forward fill at most two records
    data['hourly_precipitation'] = \
        data['hourly_precipitation'].fillna(method='ffill', limit=2)
    data['hourly_precipitation'] = \
        data['hourly_precipitation'].fillna(0)
    # forward fill remainder of missing data
    data = data.fillna(method='ffill')

    # fuzzy match on lat and long
    data['int_latitude'] = data['latitude'] * 10
    data['int_latitude'] = data['int_latitude'].astype(int)
    data['int_longitude'] = data['longitude'] * 10
    data['int_longitude'] = data['int_longitude'].astype(int)

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
