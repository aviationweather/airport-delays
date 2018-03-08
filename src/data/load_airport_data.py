"""
Loads the airport CSV into sqlite database
"""
import sys
import pandas as pd
import glob
from sqlalchemy import create_engine
import logging
import random
from collections import namedtuple


def get_airport_features():
    """ Return a dictionary of columns and target data types.

        Asserting str type is chosen for many types that contain numeric data,
        primarily because no numeric operation is expected to be taken.
    """
    Feature = namedtuple('Feature', ['raw_name', 'storage_name', 'dtype'])
    return [
        Feature('AIRPORT_SEQ_ID', 'airport_seq_id', str),
        Feature('AIRPORT_ID', 'airport_id', str),
        Feature('AIRPORT', 'airport', str),
        Feature('DISPLAY_AIRPORT_NAME', 'display_airport_name', str),
        Feature('DISPLAY_AIRPORT_CITY_NAME_FULL',
                'display_airport_city_name_full', str),
        Feature('AIRPORT_WAC_SEQ_ID2', 'airport_wac_seq_id2', str),
        Feature('AIRPORT_WAC', 'airport_wac', int),
        Feature('AIRPORT_COUNTRY_NAME', 'airport_country_name', str),
        Feature('AIRPORT_COUNTRY_CODE_ISO', 'airport_country_code_iso', str),
        Feature('AIRPORT_STATE_NAME', 'airport_state_name', str),
        Feature('AIRPORT_STATE_CODE', 'airport_state_code', str),
        Feature('AIRPORT_STATE_FIPS', 'airport_state_fips', int),
        Feature('CITY_MARKET_SEQ_ID', 'city_market_seq_id', int),
        Feature('CITY_MARKET_ID', 'city_market_id', int),
        Feature('DISPLAY_CITY_MARKET_NAME_FULL',
                'display_city_market_full_name', str),
        Feature('CITY_MARKET_WAC_SEQ_ID2', 'city_market_wac_seq_id2', int),
        Feature('CITY_MARKET_WAC', 'city_market_wac', int),
        # Latitude
        Feature('LAT_DEGREES', 'lat_degrees', int),
        Feature('LAT_HEMISPHERE', 'lat_hemisphere', str),
        Feature('LAT_MINUTES', 'lat_minutes', int),
        Feature('LAT_SECONDS', 'lat_seconds', int),
        Feature('LATITUDE', 'latitude', float),
        # Longitude
        Feature('LON_DEGREES', 'lon_degrees', int),
        Feature('LON_HEMISPHERE', 'lon_hemisphere', str),
        Feature('LON_MINUTES', 'lon_minutes', int),
        Feature('LON_SECONDS', 'lon_seconds', int),
        Feature('LONGITUDE', 'longitude', float),
        # Time features
        Feature('UTC_LOCAL_TIME_VARIATION', 'utc_local_time_variation', str),
        Feature('AIRPORT_START_DATE', 'airport_start_date', str),
        Feature('AIRPORT_THRU_DATE', 'airport_thru_date', str),
        Feature('AIRPORT_IS_CLOSED', 'airport_is_closed', bool),
        Feature('AIRPORT_IS_LATEST', 'airport_is_latest', bool)
    ]


def read_airport_data_from_csv(file_name, as_iterator=False, chunksize=10000):
    """ Read the contents of a provided csv into a dataframe or iterator """
    features = get_airport_features()
    raw_features = [f.raw_name for f in features]

    if as_iterator:
        return pd.read_csv(file_name, encoding='latin-1', header=0,
                           delimiter=',', low_memory=False,
                           usecols=raw_features,
                           iterator=as_iterator, dtype=str,
                           chunksize=chunksize)

    return pd.read_csv(file_name, encoding='latin-1', header=0,
                       delimiter=',', low_memory=False,
                       usecols=raw_features,
                       iterator=as_iterator, dtype=str)


def transform_ariport_data(data):
    """Conduct inital data type tranformations for airport data"""
    # ensure all column names are stripped of blank spaces
    data = data.rename(columns={c: c.replace(' ', '') for c in data.columns})
    # convert all column names to lower camel case
    data.columns = [x.lower() for x in data.columns]

    features = get_airport_features()
    for f in features:
        if f.dtype == int:
            data[f.storage_name] = data[f.storage_name].fillna(0).astype(int)
        if f.dtype == float:
            data[f.storage_name] = data[f.storage_name].fillna(0).astype(float)

    # datetime conversion from string
    data['airport_start_date'] = \
        pd.to_datetime(data['airport_start_date'], format='%Y-%m-%d')
    data['airport_thru_date'] = \
        pd.to_datetime(data['airport_thru_date'], format='%Y-%m-%d')

    # fuzzy match on lat and long
    data['int_latitude'] = data['latitude'] * 10
    data['int_latitude'] = data['int_latitude'].astype(int)
    data['int_longitude'] = data['longitude'] * 10
    data['int_longitude'] = data['int_longitude'].astype(int)
    return data


def load_csv_into_database(file_name, path_to_database, logger):
    db_engine = create_engine(path_to_database)
    chunksize = 10000
    i, j = 0, 1
    logger.info(f"Uploading File: {file_name}")
    with db_engine.connect() as connection:
        reader = read_airport_data_from_csv(file_name, chunksize=chunksize,
                                            as_iterator=True)
        for chunk in reader:
            chunk = transform_ariport_data(chunk)
            chunk.index += j
            i += 1
            chunk.to_sql('airports', connection,
                         chunksize=chunksize, if_exists='append')
            j = chunk.index[-1] + 1

    logger.info(f"Upload Complete: {file_name}")


def get_airport_files():
    """Return list of csv files with airport data"""
    return glob.glob("data/raw/airports/*MASTER_CORD_All_All.csv")


def load_airport_data(path_to_database):
    logger = logging.getLogger(__name__)
    files = get_airport_files()
    for f in files:
        load_csv_into_database(f, path_to_database, logger)


def main():
    f = random.choice(get_airport_files())
    data = read_airport_data_from_csv(f)
    data = transform_ariport_data(data)
    print(data.head)
    print(data.info)


if __name__ == '__main__':
    sys.exit(main())
