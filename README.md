# scrapy-darksky-api

## Envrionment

- Python 3.6
- Windows 10

## Coding Style

![coding_style](https://img.shields.io/badge/code%20style-black-000000.svg)

## Install

    python -m venv venv
    .\venv\Scripts\activate
    python -m pip install -U pip setuptools
    pip install -r requirements.txt

Use `pip install -r requirements-dev.txt` for development.
It will install `pylint` and `black` to enable linting and auto-formatting.

## Usage

Fist, set envrionment variables for darksky secret key, latitude, longitude, year, and hour for crawling.
This scrapy app would crawl the temperatures in all days witin {year} at {hour} o'clock.

    $Env:darksky_secret_key="xxx"
    $Env:darksky_latitude="51.05011"
    $Env:darksky_longitude="-114.08529"
    $Env:darksky_year="2013"
    $Env:darksky_hour="6"
    # for example, (51.0447° N, 114.0719° W) is Calgary's coordinates

Then, crawl the forcast data

    scrapy crawl forcast -o forcast_$Env:darksky_year`_$Env:darksky_hour.json
