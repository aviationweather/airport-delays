"""
Loads the flights data into sqlite database
"""
import sys
import pandas as pd
import glob
import random
import datetime as datetime
from sqlalchemy import create_engine
from tqdm import tqdm
import logging

def get_column_dictionary():
    """ Return a dictionary of columns and target data types. """
    return {
        'Year':int, 'Month':int, 'DayofMonth':int, 'DayOfWeek':int, 'FlightDate':datetime.date, 'UniqueCarrier':str,
        'AirlineID':str, 'Carrier':str, 'TailNum':str, 'FlightNum':str, 
        'OriginAirportID':str, 'OriginAirportSeqID':str,
        'OriginCityMarketID':str, 'Origin':str, 'OriginCityName':str, 'OriginState':str, 'OriginStateFips':int,
        'OriginStateName':str, 'OriginWac':int, 
        'DestAirportID':str, 'DestAirportSeqID':str, 'DestCityMarketID':str,
        'Dest':str, 'DestCityName':str, 'DestState':str, 'DestStateFips':int, 'DestStateName': str, 'DestWac':int,
        'CRSDepTime':datetime.time, 'DepTime':datetime.time, 'DepDelay':float, 'DepDelayMinutes':float, 'DepDel15':bool,
        'DepartureDelayGroups':int, 'DepTimeBlk':str, 'TaxiOut':float, 'WheelsOff':datetime.time, 'WheelsOn':datetime.time,
        'TaxiIn':float, 'CRSArrTime':datetime.time, 'ArrTime':datetime.time, 'ArrDelay':float, 'ArrDelayMinutes':float,
        'ArrDel15':bool, 'ArrivalDelayGroups':int, 'ArrTimeBlk':bool, 
        'Cancelled':bool, 'CancellationCode':str, 'Diverted':bool, 
        'CRSElapsedTime':float, 'ActualElapsedTime':float, 'AirTime':float, 
        'Flights':float, 'Distance':float, 'DistanceGroup':int,
        'CarrierDelay':float, 'WeatherDelay':float, 'NASDelay':float, 'SecurityDelay':float, 'LateAircraftDelay':float
     }

def load_csv_into_database(file_name, path_to_database):
    db_engine = create_engine(path_to_database)
    column_dict = get_column_dictionary()
    chunksize = 10000
    i, j = 0, 1
    with db_engine.connect() as connection:
        reader = pd.read_csv(file_name, encoding='latin-1', usecols=column_dict.keys(), header=0, delimiter=',', chunksize=chunksize, iterator=True, dtype='str')
        for df in tqdm(reader):
            df = df.rename(columns={c: c.replace(' ', '') for c in df.columns}) 
            for column_name, data_type in column_dict.items():
                if data_type == int:
                    df[column_name] = df[column_name].fillna(0).astype(data_type)
                if data_type == float:
                    df[column_name] = df[column_name].fillna(0).astype(data_type)
                if data_type == datetime.date:
                    df[column_name] = pd.to_datetime(df[column_name], format='%Y-%m-%d')
                if data_type == datetime.time:
                    df[column_name] = df[column_name].fillna(0).astype(str)

            df.index += j
            i+=1
            df.to_sql('flights', connection, chunksize=chunksize, if_exists='append')
            j = df.index[-1] + 1

def load_flight_data(path_to_database):
    logger = logging.getLogger(__name__)
     # Reverse sort to load most recent years first
    files = sorted(glob.glob("data/raw/flights/On_Time_On_Time*.csv"), reverse=True)

    for f in files:
        logger.info(f'Loading {f} into database')
        load_csv_into_database(f, path_to_database)
        logger.info('Complete...loading next file')