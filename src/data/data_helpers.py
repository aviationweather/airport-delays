""" Shared helpers for data scripts
"""
import os

def round_to_hour(ts):
    """Revert a timestamp to the last full hour, for use with pd.apply()"""
    return ts.replace(microsecond=0, second=0, minute=0)

def find(name, path):
    """ Walks selected path to find a given file"""
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def get_database_connection_string():
    """Returns the sqlite connection string"""
    return "sqlite:///" + find('airlines.db', '.')
