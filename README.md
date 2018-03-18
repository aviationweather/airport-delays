# Analysis of Delays in US Airports

## Overview

Airport delays are costly.  Delays are costly to consumers who would prefer to spend that lost time working, vacationing or otherwise deriving economic value.  The same delays are costly to airlines in fuel, workforce, equipment, reputation, and other opportunity costs.  Finally, the airports themselves may incur lost revenues from consistent delays as passengers and airlines alike seek regional alternatives.  With that in mind, understanding the magnitude, frequency and growth of such delays across the system can help all stakeholders make more informed decisions about where to fly, land, and invest in the hopes of making the air travel a more consumer-friendly experience, encouraging consumers to travel more.

## Objective

The objective of this analysis is to examine the relationships between flight delays, weather, and the size of airports across the United States. The analysis consists of some sub-components:

- Comparison and contrast of domestic airports along high-level performance metrics
- Prediction of airport delays at a selected regional airport

The aggregation of these components is intended to provide consumers an opportunity to understand how domestic airports are performing relative to one another, and reducing travel discomfort by proactively identifying flights that are likely to be delayed or canceled. Initially, my focus will be on 2017 flights departing from LAX, ATL, and MDT.

## Data

The primary data required to conduct the analysis include information on domestic airports and the flights between them.  The [United States Department Of Transportation - Bureau of Transportation Statistics](https://www.bts.gov/) collects detailed information for both categories.  Weather data, aggregated by the [National Oceanic and Atmospheric Administration](http://www.noaa.gov/), is available for various locations and time frames.

### Dataset: Airport Data

Data used to identify each airport includes name, latitude, longitude, city, state, and current operational status.  This information is made available by the Bureau of Transportation Statistics in the [Aviation Support Tables: Master Coordinate Table](https://www.transtats.bts.gov/tables.asp?DB_ID=595&DB_Name=&DB_Short_Name=#).  The data is available for download as single, zipped CSV file.  The linked [dictionary file](references/airports/DICTIONARY.md) provides an overview of the expected contents of this file.

### Dataset: Flight Data

Attributes of individual flights are available from the Bureau of Transportation Statistics in the [Data Profile: Airline On-Time Performance Data Table](https://www.transtats.bts.gov/DatabaseInfo.asp?DB_ID=120&Link=0).  The information is downloadable as a series of zipped CSV files that include monthly listings of all flights from major US Domestic carriers.  The data includes information identifying the departing airport, arrival airport, airline, original schedule, as well as the actual schedule with specific delays quantified in minutes.  Additional details regarding the expected contents of are available in the following linked [dictionary file](references/flights/DICTIONARY.md).

### Dataset: Weather Data

Hourly weather measurements were pulled from the [Local Climatological Data (LCD)](https://www.ncdc.noaa.gov/cdo-web/datatools/lcd).  This data includes measured wind speed, precipitation, temperature and air pressure.  An overview of the file contents is available in the following [documentation](references/weather/lcd_weather_documentation.pdf).

## Current Approach

The development of this analysis required the following high-level steps:

### Configuration and Environment

This project leverages the [Cookie Cutter Data Science Project Template](https://drivendata.github.io/cookiecutter-data-science/).  Installing the project requirements can be completed with:

```shell
make requirements
```

### Data Acquisition

After download raw csv's should be placed in the corresponding location.

- Airports: `/data/raw/airports/`
- Flights:  `/data/raw/flights/`
- Weather:  `/data/raw/weather/`

### Data Storage

Assuming the successful configuration of the aws-cli, syncing the contents of the `\data\` directory can be achieved with the following commands:

```shell
# Upload
make sync_data_to_s3
# Download
make sync_data_from_s3
```

For storage in your s3 bucket, the following line in the `MAKEFILE` needs to be updated.

```makefile
BUCKET = put-your-custom-bucket-name-here
```

### Data Wrangling

After download, the raw CSV files were processed by a series of scripts aggregated in the script `make_dataset.py`.  The processing results in an aggregation of the data into an SQLite database `/data/processed/airlines.db`.  This process can be run with the command:

```shell
make data
```

### Exploratory Data Analysis

Notebooks outlining the initial data analysis can be found in the `./notebooks/eda/` directory.

### Feature Generation

After data is loaded into the local repository, a set of prepared data features for modeling can be generated with the following command.  The generated features will be stored in `./data/processed/airlines.db`.

```shell
make features
```

### Outputs

The following short posts are based on this project:

- Exploratory Data Analysis: Does it matter when I fly?
  - [https://bcbeidel.github.io/2018/03/17/does-it-matter-when-i-fly/](https://bcbeidel.github.io/2018/03/17/does-it-matter-when-i-fly/)
- Classification with Scikit-learn: Predicting Flight Delays
  - [https://bcbeidel.github.io/2018/03/18/predicting-flight-delays/](https://bcbeidel.github.io/2018/03/18/predicting-flight-delays/)

## Project Organization

------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results-oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
