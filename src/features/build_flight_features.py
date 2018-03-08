""" Functions to build features for flight data
"""

import sys
import pandas as pd
from datetime import date
from sqlalchemy import create_engine
import feature_helpers as helpers


def build_features_for_departing_flights(start_date=None, end_date=None,
                                         airport_code=None, path_to_db=None):
    """ Retreive features for flights departing from a selected airport """
    if start_date is None:
        start_date = date(2017, 1, 1)
    if end_date is None:
        end_date = date(2017, 12, 31)
    if airport_code is None:
        airport_code = 'MDT'

    engine = create_engine(path_to_db)
    with engine.connect() as conn:
        flights = pd.read_sql(
            """
            SELECT
                f.departure_was_delayed_15,
                f.origin,
                f.dest,
                f.carrier,
                f.departure_time_scheduled,
                f.distance,
                f.elapsed_time_scheduled
            FROM
                flights AS f
            WHERE
                f.Origin = :airport_code
            AND
                f.flight_date
            BETWEEN :start_date
                AND :end_date
            """,
            conn,
            params={
                'start_date': start_date,
                'end_date': end_date,
                'airport_code': airport_code
            })

    flights['departure_time'] = \
        flights['departure_time_scheduled'].apply(helpers.extract_datetime)
    flights['departure_month'] = flights['departure_time'].dt.month
    flights['departure_date'] = flights['departure_time'].dt.day
    flights['departure_dow'] = flights['departure_time'].dt.dayofweek
    flights['departure_hod'] = flights['departure_time'].dt.hour
    return flights


def main():
    start_date = date(2017, 1, 1)
    end_date = date(2017, 12, 31)
    airport_code = 'MDT'
    path_to_db = helpers.get_database_connection_string()

    features = build_features_for_departing_flights(start_date,
                                                    end_date,
                                                    airport_code,
                                                    path_to_db)
    print(features.head())
    print(features.info())


if __name__ == '__main__':
        sys.exit(main())
