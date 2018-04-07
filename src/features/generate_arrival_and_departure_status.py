""" Add and fill features to flights table
    - flights.arrival_status
    - flights.departure_status
"""
from sqlalchemy import create_engine
import pandas as pd
import logging
import feature_helpers as helpers


ADD_ARRIVAL_STATUS_COLUMN = """
    ALTER TABLE flights
        ADD arrival_status TEXT;
"""

ADD_DEPARTURE_STATUS_COLUMN = """
    ALTER TABLE flights
        ADD departure_status TEXT;
"""

SET_DEPARTURE_STATUS = """
    UPDATE flights 
    SET 
    departure_status = 
        CASE
            WHEN flights.cancelled = 1 THEN 'CANCELLED'
            WHEN flights.departure_delay < -15 THEN 'EARLY'
            WHEN flights.departure_delay < 15 THEN 'ON_TIME'
            WHEN flights.departure_delay < 31 THEN 'DELAYED_15_TO_30'
            WHEN flights.departure_delay < 61 THEN 'DELAYED_31_TO_60'
            WHEN flights.departure_delay < 120 THEN 'DELAYED_61_TO_120'
            WHEN flights.departure_delay > 120 THEN 'DELAYED_120_PLUS'
            ELSE 'ON_TIME'
        END 
    """

SET_ARRIVAL_STATUS = """
    UPDATE flights 
    SET 
    arrival_status = 
        CASE
            WHEN flights.cancelled = 1 THEN 'CANCELLED'
            WHEN flights.arrival_delay < -15 THEN 'EARLY'
            WHEN flights.arrival_delay < 15 THEN 'ON_TIME'
            WHEN flights.arrival_delay < 31 THEN 'DELAYED_15_TO_30'
            WHEN flights.arrival_delay < 61 THEN 'DELAYED_31_TO_60'
            WHEN flights.arrival_delay < 120 THEN 'DELAYED_61_TO_120'
            WHEN flights.arrival_delay > 120 THEN 'DELAYED_120_PLUS'
            ELSE 'ON_TIME'
        END 
    """

def add_arrival_status_column(logger, path_to_db):
    """Adds flights.arrival_status to hold target classification categories"""
    try:
        logger.info("adding column: flights.arrival_status")
        helpers.execute_statement(ADD_ARRIVAL_STATUS_COLUMN, path_to_db)
        logger.info("column added: flights.arrival_status")
    except Exception as e:
        if str(e).startswith("(sqlite3.OperationalError) duplicate column name: arrival_status"):
            logger.info("flights.arrival_status already exists, moving to next query")
        else:
            raise e


def add_departure_status_column(logger, path_to_db):
    """ Builds arrival_status, and departure status for all flights
    """
    try:
        logger.info("adding column: flights.departure_status")
        helpers.execute_statement(ADD_DEPARTURE_STATUS_COLUMN, path_to_db)
        logger.info("column added: flights.departure_status")
    except Exception as e:
        if str(e).startswith("(sqlite3.OperationalError) duplicate column name: departure_status"):
            logger.info("flights.departure_status already exists, moving to next query")
        else:
            raise e


def assign_departure_status(logger, path_to_db):
    """ Determine values for flights.departure_status"""
    try:
        logger.info("Setting Values: flights.departure_status")
        helpers.execute_statement(SET_DEPARTURE_STATUS, path_to_db)
        logger.info("update complete: flights.departure_status")
    except Exception as e:
        raise e


def assign_arrival_status(logger, path_to_db):
    """ Determine values for flights.arrival_status"""
    try:
        logger.info("Setting Values: flights.arrival_status")
        helpers.execute_statement(SET_ARRIVAL_STATUS, path_to_db)
        logger.info("update complete: flights.arrival_status")
    except Exception as e:
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
    assign_departure_status(logger, path_to_db)
    assign_arrival_status(logger, path_to_db)
    logger.info("Script Complete")


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
