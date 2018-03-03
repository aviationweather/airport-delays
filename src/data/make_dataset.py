# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import load_airport_data as airports
import load_flight_data as flights
import load_weather_data as weather

def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    
    path_to_db = 'sqlite:///data/processed/airlines.db'

    logger.info('loading airport data')
    #airports.load_airport_data(path_to_db)
    logger.info('loading flight data')
    #flights.load_flight_data(path_to_db)
    logger.info('handling weather data')
    weather.load_weather_data(path_to_db)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
