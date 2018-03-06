"""
Loads the airport CSV into sqlite database
"""
import sys
import pandas as pd
import glob
import random
import numpy as np
from sqlalchemy import create_engine
import logging

def get_column_dictionary():
    """ Return a dictionary of columns and target data types. 
    
        Asserting str type is chosen for many types that contain numeric data, primarily because no numeric operation is expected to be taken.

        See zip code example:
        https://stackoverflow.com/questions/893454/is-it-a-good-idea-to-use-an-integer-column-for-storing-us-zip-codes-in-a-databas
    """
    return {
        'AIRPORT_SEQ_ID':str, 'AIRPORT_ID':str, 'AIRPORT':str, 'DISPLAY_AIRPORT_NAME':str, 'DISPLAY_AIRPORT_CITY_NAME_FULL':str,
        'AIRPORT_WAC_SEQ_ID2':int, 'AIRPORT_WAC':int, 'AIRPORT_COUNTRY_NAME':str, 'AIRPORT_WAC':str, 'AIRPORT_COUNTRY_NAME':str,
        'AIRPORT_COUNTRY_CODE_ISO': str, 'AIRPORT_STATE_NAME':str, 'AIRPORT_STATE_CODE':str, 'AIRPORT_STATE_FIPS':int,
        'CITY_MARKET_SEQ_ID':int, 'CITY_MARKET_ID':int, 'DISPLAY_CITY_MARKET_NAME_FULL':str, 'CITY_MARKET_WAC_SEQ_ID2':int,
        'CITY_MARKET_WAC':int, 'CITY_MARKET_WAC': int, 'LAT_DEGREES':int, 'LAT_HEMISPHERE': str, 'LAT_MINUTES':int,
        'LAT_SECONDS':int, 'LATITUDE':float, 'LON_DEGREES':int, 'LON_HEMISPHERE':str, 'LON_MINUTES':int, 'LON_SECONDS':int, 
        'LONGITUDE':float, 'UTC_LOCAL_TIME_VARIATION':str, 'AIRPORT_START_DATE':str, 'AIRPORT_THRU_DATE':str,
        'AIRPORT_IS_CLOSED':bool, 'AIRPORT_IS_LATEST':bool 
    }

def load_csv_into_database(file_name, path_to_database, logger):
    db_engine = create_engine(path_to_database)
    column_type_dict = get_column_dictionary()
    chunksize = 10000
    i, j = 0, 1
    logger.info(f"Uploading File: {file_name}")
    with db_engine.connect() as connection:
        for df in pd.read_csv(file_name, encoding='latin-1', usecols=column_type_dict.keys(), header=0, 
                              delimiter=',', chunksize=chunksize, iterator=True, dtype=str):
            df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
            for column_name, data_type in column_type_dict.items():
                if data_type == int:
                    df[column_name] = df[column_name].fillna(0).astype(data_type)
                if data_type == float:
                    df[column_name] = df[column_name].fillna(0).astype(data_type)
                if column_name == 'AIRPORT_START_DATE':
                    df[column_name] = pd.to_datetime(df[column_name], format='%Y-%m-%d')
                if column_name == 'AIRPORT_THRU_DATE':
                    df[column_name] = pd.to_datetime(df[column_name], format='%Y-%m-%d')

            # fuzzy match on weather measurements within the same 0.1 degrees lat and long
            df['int_latitude'] = df['LATITUDE'] * 10
            df['int_latitude'] = df['int_latitude'].astype(int)
            df['int_longitude'] = df['LONGITUDE'] * 10
            df['int_longitude'] = df['int_longitude'].astype(int)
            
            df.index += j
            i+=1
            # set all columns to lower case
            df.columns = map(str.lower, df.columns)
            df.to_sql('airports', connection, chunksize=chunksize, if_exists='append', index=False)
            j = df.index[-1] + 1
    logger.info(f"Upload Complete: {file_name}")

def load_airport_data(path_to_database):
    logger = logging.getLogger(__name__)
    files = glob.glob("data/raw/airports/*MASTER_CORD_All_All.csv")
    for f in files:
        load_csv_into_database(f, path_to_database, logger)

