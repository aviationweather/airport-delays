"""
Wrappers for database queries
"""

from datetime import date
import pandas as pd
from sqlalchemy import create_engine


def flight_and_delay_summary_by_airport(start_date=date.min, end_date=date.max,
                                        delay_threshold=15, path_to_db=""):
    """ Return a dataframe flight counts by day of week and year """
    engine = create_engine(path_to_db)
    print("Connecting to Database:", path_to_db)
    with engine.connect() as conn:
        monthly_flights = pd.read_sql(
            """
            SELECT
                a.display_airport_name as airport_name,
                f.origin as airport_code,
                COUNT(f.flights) AS departure_count,
                SUM(
                    CASE WHEN
                        f.departure_delay > :delay_threshold
                    THEN
                        1
                    ELSE
                        0
                    END
                ) AS delayed_count
            FROM
                flights AS f
            JOIN
                airports as a
            ON
                a.airport_seq_id = f.origin_airport_sequence_id
            WHERE
                f.flight_date
            BETWEEN :start_date
                AND :end_date
            GROUP BY
                f.origin
            """,
            conn,
            params={
                'start_date': start_date,
                'end_date': end_date,
                'delay_threshold': delay_threshold
            })
    return monthly_flights
