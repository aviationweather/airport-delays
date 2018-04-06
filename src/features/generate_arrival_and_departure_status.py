""" Add and fill features to flights table
    - flights.arrival_status
    - flights.departure_status
"""
from sqlalchemy import create_engine
import pandas as pd
import logging
import feature_helpers as helpers


SQL_STATEMENT_ADD_ARRIVAL_STATUS_COLUMN = """
    ALTER TABLE flights
        ADD arrival_status TEXT;
"""


SQL_STATEMENT_ADD_DEPARTURE_STATUS_COLUMN = """
    ALTER TABLE flights
        ADD departure_status TEXT;
"""


def add_arrival_status_column(logger, path_to_db):
    """Adds flights.arrival_status to hold target classification categories"""
    try:
        logger.info("adding column: flights.arrival_status")
        helpers.execute_statement(SQL_STATEMENT_ADD_ARRIVAL_STATUS_COLUMN, path_to_db)
        logger.info("column added: flights.arrival_status")
    except Exception as e:
        if str(e).startswith("(sqlite3.OperationalError) duplicate column name: arrival_status"):
            logger.info("flights.arrival_status already exists, moving to next query")
        else:
            raise e


def add_departure_status_column(logger, path_to_db):
    """Adds flights.departure_status to hold target classification categories"""
    try:
        logger.info("adding column: flights.departure_status")
        helpers.execute_statement(SQL_STATEMENT_ADD_DEPARTURE_STATUS_COLUMN, path_to_db)
        logger.info("column added: flights.departure_status")
    except Exception as e:
        if str(e).startswith("(sqlite3.OperationalError) duplicate column name: departure_status"):
            logger.info("flights.departure_status already exists, moving to next query")
        else:
            raise e

def main():
    """ Executes string of statments to generate target features
          - departure_status
          - arrival_status
    """    
    logger = logging.getLogger(__name__)
    logger.info('Connecting to Database')
    path_to_db = helpers.get_database_connection_string()
    add_arrival_status_column(logger, path_to_db)
    add_departure_status_column(logger, path_to_db)
    logger.info("Script Complete")

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
