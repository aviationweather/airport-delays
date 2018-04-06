from sqlalchemy import create_engine
import pandas as pd
import logging
import feature_helpers as helpers


DROP_ARRIVAL_FEATURES_TABLE = """
    DROP TABLE IF EXISTS arrival_features;
"""

CREATE_ARRIVAL_FEATURES_TABLE = """
    CREATE TABLE arrival_features (
        arrival_airport_id INTEGER NOT NULL,
        scheduled_arrival_hour DATETIME NOT NULL,
        scheduled_arrivals INTEGER NOT NULL,
        fraction_cancelled_arrivals DOUBLE NOT NULL,
        fraction_delayed_arrivals DOUBLE NOT NULL,
        average_delay_arrivals INTEGER NOT NULL
    );
"""

GENERATE_ARRIVAL_FEATURES = """
    INSERT INTO arrival_features 
    SELECT 
        f.dest_airport_id AS arrival_airport_id,
        f.arrival_hour_scheduled AS scheduled_arrival_hour,
        SUM(f.flights) AS scheduled_arrivals,
        SUM(f.cancelled) / SUM(f.flights) AS fraction_cancelled_arrivals,
        SUM(f.arrival_was_delayed_15) / SUM(f.flights) AS fraction_delayed_arrivals,
        CASE 
            WHEN SUM(f.arrival_was_delayed_15) > 0 
                THEN SUM(f.arrival_delay) / SUM(f.arrival_was_delayed_15) 
            ELSE 0
        END AS average_delay_arrivals
    FROM 
        flights AS f
    GROUP BY
        f.dest_airport_id,
        f.arrival_hour_scheduled
"""

DROP_DEPARTURE_FEATURES_TABLE = """
    DROP TABLE IF EXISTS departure_features;
"""

CREATE_DEPARTURE_FEATURES_TABLE = """
    CREATE TABLE departure_features (
        departure_airport_id INTEGER NOT NULL,
        scheduled_departure_hour DATETIME NOT NULL,
        scheduled_departures INTEGER NOT NULL,
        fraction_cancelled_departures DOUBLE NOT NULL,
        fraction_departures_delayed DOUBLE NOT NULL,
        average_delay_departures INTEGER NOT NULL
    );
"""

GENERATE_DEPARTURE_FEATURES = """
    INSERT INTO departure_features 
    SELECT 
        f.origin_airport_id as departure_airport_id,
        f.departure_hour_scheduled as scheduled_departure_hour,
        SUM(f.flights) as scheduled_departures,
        SUM(f.cancelled) / SUM(f.flights) as fraction_cancelled_departures,
        SUM(f.departure_was_delayed_15) / SUM(f.flights) as fraction_departures_delayed,
        CASE 
            WHEN SUM(f.departure_was_delayed_15) > 0 
                THEN SUM(f.departure_delay) / SUM(f.departure_was_delayed_15) 
            ELSE 0
        END AS average_delay_departures
    FROM 
        flights AS f
    GROUP BY
        f.origin_airport_id,
        f.departure_hour_scheduled
"""

def execute_statement(statment, path_to_db):
    engine = create_engine(path_to_db)
    with engine.connect() as conn:
        result = conn.execute(statment)
    return result

def generate_arrival_congestion(logger, path_to_db):
    logger.info("Arrival Features: Discarding Existing Table")
    execute_statement(DROP_ARRIVAL_FEATURES_TABLE, path_to_db)
    logger.info("Arrival Features: Creating New Table")
    execute_statement(CREATE_ARRIVAL_FEATURES_TABLE, path_to_db)
    logger.info("Arrival Features: Generating Table Contents")
    execute_statement(GENERATE_ARRIVAL_FEATURES, path_to_db)

def generate_departure_congestion(logger, path_to_db):
    logger.info("Departure Features: Discarding Existing Table")
    execute_statement(DROP_DEPARTURE_FEATURES_TABLE, path_to_db)
    logger.info("Departure Features: Creating New Table")
    execute_statement(CREATE_DEPARTURE_FEATURES_TABLE, path_to_db)
    logger.info("Departure Features: Generating Table Contents")
    execute_statement(GENERATE_DEPARTURE_FEATURES, path_to_db)

def main():
    """ Executes string of queries to generate congestion related features
    """    
    logger = logging.getLogger(__name__)
    logger.info('Connecting to Database')
    path_to_db = helpers.get_database_connection_string()

    try:
        logger.info("Arrival Features: Generation Started")
        generate_arrival_congestion(logger, path_to_db)
        logger.info("Arrival Features: Generation Complete")
    except Exception as e:
        logger.error("An error occured generating arrival features.")
        logger.error(str(e))

    try:
        logger.info("Departure Features: Generation Started")
        generate_departure_congestion(logger, path_to_db)
        logger.info("Departure Features: Generation Complete")
    except Exception as e:
        logger.error("An error occured generating departure features.")
        logger.error(str(e))

    logger.info("Script Complete")

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
