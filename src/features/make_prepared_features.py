""" Get a number of prepared records for analysis, store in local db
"""
import build_features as build_features
from feature_helpers import get_database_connection_string
from datetime import date
from pandas.io import sql
from sqlalchemy import create_engine
import logging
import sys

def drop_feature_table(path_to_db, table):
    engine = create_engine(path_to_db)
    sql.execute('DROP TABLE IF EXISTS %s'%table, engine)
    sql.execute('VACUUM', engine)

def main():
    """ Build featureset for departing flights, print to console"""
    logger = logging.getLogger(__name__)

    start_date = date(2017, 1, 1)
    end_date = date(2017, 12, 31)
    path_to_db = get_database_connection_string()
    drop_feature_table(path_to_db, 'features')

    for airport_code in ['MDT', 'ATL', 'LAX']:
        logger.info(f'Generating Feature Set For {airport_code}')
        features = build_features.get_features_for_delay_classification(
            start_date=start_date, 
            end_date=end_date,
            airport_code=airport_code, 
            path_to_db=path_to_db
        )
        logger.info(f'Storing Generated Features For {airport_code}')
        with create_engine(path_to_db).connect() as connection:
            features.to_sql('features', connection,if_exists='append')
        logger.info(f'Storage Complete For {airport_code}')

    logger.info('Feature Generation Complete')

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
