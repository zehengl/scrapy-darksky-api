# scrapy-darksky-api

![coding_style](https://img.shields.io/badge/code%20style-black-000000.svg)
[![time tracker](https://wakatime.com/badge/github/zehengl/scrapy-darksky-api.svg)](https://wakatime.com/badge/github/zehengl/scrapy-darksky-api)

A scrapy app to crawl weather data from Dark Sky Api

## Envrionment

- Python 3.6

## Install

1. create virtualenv
2. activate virtualenv
3. update pip and setuptools
4. install deps

Use `pip install -r requirements-dev.txt` for development.
It will install `pylint` and `black` to enable linting and auto-formatting.

## Usage

1. set envrionment variables for darksky secret key, latitude, longitude, year, and hour for crawling
2. run scrapy to crawl the forcast data and save in json

This scrapy app would crawl the temperatures in all days witin {year} at {hour} o'clock.

Keep in mind that [Dark Sky Api](https://darksky.net/dev) only allows 1000 requests for free tier.

## Example

( _51.0447° N_, _114.0719° W_ ) is Calgary's coordinates.

### Windows

```powershell
python -m venv venv
.\venv\Scripts\activate
python -m pip install -U pip setuptools
pip install -r requirements-scrapy.txt
$Env:darksky_secret_key="xxx"
$Env:darksky_latitude="51.05011"
$Env:darksky_longitude="-114.08529"
$Env:darksky_year="2013"
$Env:darksky_hour="6"
scrapy crawl forcast -o data\forcast_$Env:darksky_year`_$Env:darksky_hour.json
```

### Linux

```bash
python -m venv venv
source venv/bin/activate
python -m pip install -U pip setuptools
pip install -r requirements-scrapy.txt
export darksky_secret_key="xxx"
export darksky_latitude="51.05011"
export darksky_longitude="-114.08529"
export darksky_year="2013"
export darksky_hour="6"
scrapy crawl forcast -o data/forcast_$darksky_year\_$darksky_hour.json
```

## Demo

See the demo app at [https://scrapy-darksky-api.herokuapp.com/](https://scrapy-darksky-api.herokuapp.com/) for some crawled weather data

## Credits

- [Icon](https://www.iconfinder.com/icons/667368/celcius_clouds_farenheit_sunshine_temerature_thermometer_weather_icon) by [The Pictographers](https://www.iconfinder.com/bluewolfski)
