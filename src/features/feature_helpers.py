""" Shared Helpers methods for features namespace
"""
import os
import numpy as np
import pandas as pd
from datetime import timedelta
from sqlalchemy import create_engine


def find(name, path):
    """ Walks selected path to find a given file"""
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def get_database_connection_string():
    """Returns the sqlite connection string"""
    return "sqlite:///" + find('airlines.db', '.')


def extract_datetime(dt_string):
    """Convert string to datetime, for use with pd.apply()"""
    return pd.to_datetime(dt_string, infer_datetime_format=True)


def round_to_hour(ts):
    """Revert a timestamp to the last full hour, for use with pd.apply()"""
    return ts.replace(microsecond=0, second=0, minute=0)


def shift_back_hours(ts, hours=3):
    """Return a timestamp a set number of hours in past"""
    return ts - timedelta(hours=hours)


def exclude_datetime_features(data):
    return data.select_dtypes(exclude=[np.datetime64])


def execute_statement(statement, path_to_db):
    engine = create_engine(path_to_db)
    with engine.connect() as conn:
        result = conn.execute(statement)
    return result
