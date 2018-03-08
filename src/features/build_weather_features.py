""" Functions to build features for flight data
"""
import sys
import pandas as pd
from datetime import date
from sqlalchemy import create_engine
import feature_helpers as helpers


def get_weather_data(start_date=None, end_date=None,
                     airport_code=None, path_to_db=None):
    """ Query weather features at selected airport """
    if start_date is None:
        start_date = date(2017, 1, 1)
    if end_date is None:
        end_date = date(2017, 12, 31)
    if airport_code is None:
        airport_code = 'MDT'

    engine = create_engine(path_to_db)
    with engine.connect() as conn:
        weather = pd.read_sql(
            """
            SELECT
                a.airport,
                w.date,
                w.hourly_visibility,
                w.hourly_dry_bulb_temp_f,
                w.hourly_precipitation,
                w.hourly_wind_speed,
                w.hourly_wind_gust_speed,
                w.hourly_station_pressure
            FROM
                weather AS w
            JOIN
                airports as a
            ON a.int_latitude = w.int_latitude
            AND a.int_longitude = w.int_longitude
            WHERE
                a.airport = :airport_code
            AND
                a.airport_is_latest == 1
            AND
                w.date
            BETWEEN :start_date
                AND :end_date
            """,
            conn,
            params={
                'start_date': start_date,
                'end_date': end_date,
                'airport_code': airport_code
            })
    return weather


def build_weather_features(weather):
    """ Conduct transformations to build weather feature-set """
    weather['date'] = weather['date'].apply(helpers.extract_datetime)
    weather['measurement_hour'] = weather['date'].apply(helpers.round_to_hour)
    weather = weather.drop('date', axis=1)
    return weather


def get_weather_features(start_date=None, end_date=None,
                         airport_code=None, path_to_db=None):
    """ Retrieve weather data and build weather features """
    weather = get_weather_data(start_date, end_date, airport_code, path_to_db)
    return build_weather_features(weather)


def main():
    """ Build featureset for departing flights, print to console"""
    start_date = date(2017, 1, 1)
    end_date = date(2017, 12, 31)
    airport_code = 'MDT'
    path_to_db = helpers.get_database_connection_string()

    features = get_weather_features(start_date, end_date,
                                    airport_code, path_to_db)

    print(features.head())
    print(features.info())


if __name__ == '__main__':
        sys.exit(main())
