"""
Loads the flights data into sqlite database
"""
import sys
from collections import namedtuple
import pandas as pd
import glob
import random
import datetime as datetime
from sqlalchemy import create_engine
import logging
import time
import data_helpers as helpers


def identify_flight_features():
    """ Return a dictionary of features for use from csv. """
    Feature = namedtuple('Feature', ['raw_name', 'storage_name', 'dtype'])
    return [
        Feature('Year', 'year', int),
        Feature('Month', 'month', int),
        Feature('DayofMonth', 'day_of_month', int),
        Feature('DayOfWeek', 'day_of_week', int),
        Feature('FlightDate', 'flight_date', datetime.date),
        Feature('UniqueCarrier', 'carrier', str),
        Feature('AirlineID', 'airline_id', str),
        Feature('TailNum', 'tail_number', str),
        Feature('Origin', 'origin', str),
        Feature('OriginAirportID', 'origin_airport_id', str),
        Feature('OriginAirportSeqID', 'origin_airport_sequence_id', str),
        Feature('Dest', 'dest', str),
        Feature('DestAirportID', 'dest_airport_id', str),
        Feature('CRSDepTime', 'departure_time_scheduled', 'time'),
        Feature('DepTimeBlk', 'departure_time_block', str),
        Feature('DepTime', 'departure_time_actual', 'time'),
        Feature('DepDelay', 'departure_delay', int),
        Feature('DepDel15', 'departure_was_delayed_15', bool),
        Feature('CRSArrTime', 'arrival_time_scheduled', 'time'),
        Feature('ArrTimeBlk', 'arrival_time_block', str),
        Feature('ArrTime', 'arrival_time_actual', 'time'),
        Feature('ArrDelay', 'arrival_delay', int),
        Feature('ArrDel15', 'arrival_was_delayed_15', bool),
        Feature('Cancelled', 'cancelled', bool),
        Feature('CancellationCode', 'cancelled_code', str),
        Feature('Diverted', 'diverted', bool),
        Feature('CRSElapsedTime', 'elapsed_time_scheduled', int),
        Feature('ActualElapsedTime', 'elapsed_time_acutal', int),
        Feature('Distance', 'distance', int),
        Feature('Flights', 'flights', int)
    ]


def read_flight_data_from_csv(file_name, as_iterator=False, chunksize=None):
    """ Read the contents of a provided csv into a dataframe or iterator """
    if as_iterator:
        return pd.read_csv(file_name, encoding='latin-1', header=0,
                           delimiter=',', low_memory=False, iterator=True)

    return pd.read_csv(file_name, encoding='latin-1', low_memory=False,
                       header=0, delimiter=',', iterator=False)


def infer_time(time_num):
    """Generates a time delta based on int value"""
    try:
        time_str = str(int(time_num))
    except Exception:
        time_str = "0000"

    if time_str == '2400':
        time_str = '2359'
    if time_str == '0':
        time_str = '0001'

    out_time = time.strptime('0000', '%H%M')
    try:
        out_time = time.strptime(time_str, '%H%M')
    except ValueError:
        if time_str is not '00':
            out_time = time.strptime(time_str, '%M')
    except Exception:
        out_time = time.strptime('0000', '%H%M')

    time_delta = datetime.timedelta(hours=out_time.tm_hour,
                                    minutes=out_time.tm_min)
    return time_delta


def handle_flight_features(data):
    """Transform raw data frame for storage or inspection"""
    features = identify_flight_features()
    selected_raw_features = [f.raw_name for f in features]
    # downselect to subset of selected features
    data = data.loc[:, selected_raw_features]

    # rename all field in dataframe to appropriate 'storage_name' type
    for f in features:
        data.rename(columns={f.raw_name: f.storage_name}, inplace=True)

    for f in features:
        if f.dtype is int:
            data.loc[:, f.storage_name] = \
                data[f.storage_name].fillna(0).astype(int)
        if f.dtype is float:
            data.loc[:, f.storage_name] = \
                data[f.storage_name].fillna(0).astype(float)
        if f.dtype is bool:
            data.loc[:, f.storage_name] = \
                data[f.storage_name].fillna(0).astype(bool)
        if f.dtype is datetime.date:
            data.loc[:, f.storage_name] = \
                pd.to_datetime(data[f.storage_name],
                               infer_datetime_format=True)

    # Only handle time after flight_date is successfully converted
    for f in features:
        if f.dtype is 'time':
            time_deltas = data[f.storage_name].apply(infer_time)

            data.loc[:, f.storage_name] = \
                data.loc[:, 'flight_date'] + time_deltas

    # Append a 'scheduled_departure_hour' to dataframe
    data['departure_hour_scheduled'] = \
        data['departure_time_scheduled'].apply(helpers.round_to_hour)
    data['arrival_hour_scheduled'] = \
        data['arrival_time_scheduled'].apply(helpers.round_to_hour)
    return data


def load_csv_into_database(file_name, path_to_database):
    """Load a specified flight data file into local database, chunkwise"""
    db_engine = create_engine(path_to_database)
    chunksize = 10000
    i, j = 0, 1
    with db_engine.connect() as connection:
        reader = read_flight_data_from_csv(file_name, as_iterator=True,
                                           chunksize=chunksize)
        for chunk in reader:
            chunk = handle_flight_features(chunk)
            chunk.index += j
            i += 1
            chunk.to_sql('flights', connection,
                         chunksize=chunksize, if_exists='append')
            j = chunk.index[-1] + 1


def load_flight_data(path_to_database):
    logger = logging.getLogger(__name__)
    # Reverse sort to load most recent years first
    files = sorted(glob.glob("data/raw/flights/On_Time_On_Time*.csv"),
                   reverse=True)

    for f in files:
        logger.info(f'Loading {f} into database')
        load_csv_into_database(f, path_to_database)
        logger.info('Complete...loading next file')


def main():
    """ Parse first file, ensure parse occurs without error"""
    f = random.choice(glob.glob("data/raw/flights/*.csv"))
    data = read_flight_data_from_csv(f)
    data = handle_flight_features(data)
    print(data.info())
    print(data.head())
    print(data[['flight_date', \
                'departure_time_scheduled', 'departure_hour_scheduled', \
                'arrival_time_scheduled', 'arrival_hour_scheduled']])


if __name__ == '__main__':
    sys.exit(main())
