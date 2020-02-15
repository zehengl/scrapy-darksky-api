# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
from calendar import isleap
import json

import scrapy

from darksky.items import DarkskyItem

key = os.getenv("darksky_secret_key", None)
lat = os.getenv("darksky_latitude", None)
long = os.getenv("darksky_longitude", None)
year = os.getenv("darksky_year", None)
hour = os.getenv("darksky_hour", None)

assert key, "[darksy] secret key not set"
assert lat, "[darksky] latitude not set"
assert long, "[darksky] longitude not set"
assert year, "[darksky] year not set"
assert hour, "[darksky] hour not set"

year = int(year)
hour = int(hour)


class ForecastSpider(scrapy.Spider):
    name = "forecast"
    excludes = ",".join(["flags", "alerts", "minutely", "hourly", "daily"])
    allowed_domains = [f"https://api.darksky.net/forecast/{key}"]
    days = 366 if isleap(year) else 365
    timestamps = [
        int((datetime(year, 1, 1, hour) + timedelta(days=d)).timestamp())
        for d in range(days)
    ]

    start_urls = [
        f"https://api.darksky.net/forecast/{key}/{lat},{long},{time}?units=si&exclude=flags,alerts,minutely,hourly,daily"
        for time in timestamps
    ]

    def parse(self, response):
        forecast = json.loads(response.text)

        yield DarkskyItem(
            latitude=forecast["latitude"],
            longitude=forecast["longitude"],
            timezone=forecast["timezone"],
            offset=forecast["offset"],
            # currently block
            time=forecast["currently"].get("time", None),
            icon=forecast["currently"].get("icon", None),
            precip_intensity=forecast["currently"].get("precipIntensity", None),
            precip_probability=forecast["currently"].get("precipProbability", None),
            precip_type=forecast["currently"].get("precipType", None),
            precip_accumulation=forecast["currently"].get("precipAccumulation", None),
            temperature=forecast["currently"].get("temperature", None),
            apparent_temperature=forecast["currently"].get("apparentTemperature", None),
            dew_point=forecast["currently"].get("dewPoint", None),
            humidity=forecast["currently"].get("humidity", None),
            pressure=forecast["currently"].get("pressure", None),
            wind_speed=forecast["currently"].get("windSpeed", None),
            wind_gust=forecast["currently"].get("windGust", None),
            wind_bearing=forecast["currently"].get("windBearing", None),
            cloud_cover=forecast["currently"].get("cloudCover", None),
            uv_index=forecast["currently"].get("uvIndex", None),
            visibility=forecast["currently"].get("visibility", None),
            ozone=forecast["currently"].get("ozone", None),
        )
