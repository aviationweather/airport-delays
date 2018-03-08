""" Shared helpers for data scripts
"""
import os


def find(name, path):
    """ Walks selected path to find a given file"""
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def get_database_connection_string():
    """Returns the sqlite connection string"""
    return "sqlite:///" + find('airlines.db', '.')
