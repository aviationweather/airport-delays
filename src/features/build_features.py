""" Return aggregated feature sets for analysis
"""

import sys
import pandas as pd
from datetime import date
from datetime import timedelta
import build_flight_features as flight_builder
import build_weather_features as weather_builder
from feature_helpers import get_database_connection_string


def merge_departure_weather_data(weather, flights, hour_shift=3):
    """ Combine weather and flights features for a departing airport """
    weather['m_hour_shifted'] = \
        weather['measurement_hour'].apply(
            lambda x: x + timedelta(hours=hour_shift)
        )

    return pd.merge(left=flights, right=weather,
                    left_on=['origin', 'departure_time'],
                    right_on=['airport', 'm_hour_shifted'])


def get_features_for_delay_classification(start_date=None, end_date=None,
                                          airport_code=None, path_to_db=None):
    if path_to_db is None:
        path_to_db = get_database_connection_string()

    weather = weather_builder.get_weather_features(
        start_date=start_date,
        end_date=end_date,
        airport_code=airport_code,
        path_to_db=path_to_db
    )

    flights = flight_builder.build_features_for_departing_flights(
        start_date=start_date,
        end_date=end_date,
        airport_code=airport_code,
        path_to_db=path_to_db
    )

    return merge_departure_weather_data(weather, flights, 3)


def main():
    """Return a fixed dataset, print to console"""

    start_date = date(2017, 1, 1)
    end_date = date(2017, 12, 31)
    airport_code = 'MDT'
    path_to_db = get_database_connection_string()

    features = get_features_for_delay_classification(
        start_date=start_date,
        end_date=end_date,
        airport_code=airport_code,
        path_to_db=path_to_db
    )

    print(features.info())
    print("-----------")
    print(features.head())


if __name__ == '__main__':
        sys.exit(main())
