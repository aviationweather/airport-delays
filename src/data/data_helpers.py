""" Shared helpers for data scripts
"""
import os
from datetime import timedelta

def round_to_hour(ts):
    """Revert a timestamp to the last full hour, for use with pd.apply()"""
    return ts.replace(microsecond=0, second=0, minute=0)

def find(name, path):
    """ Walks selected path to find a given file"""
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def shift_back_hours(ts, hours=3):
    """Return a timestamp a set number of hours in past"""
    return ts - timedelta(hours=hours)

def get_database_connection_string():
    """Returns the sqlite connection string"""
    return "sqlite:///" + find('airlines.db', '.')
