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


class ForcastSpider(scrapy.Spider):
    name = "forcast"
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
        forcast = json.loads(response.text)

        yield DarkskyItem(
            latitude=forcast["latitude"],
            longitude=forcast["longitude"],
            timezone=forcast["timezone"],
            offset=forcast["offset"],
            # currently block
            time=forcast["currently"].get("time", None),
            icon=forcast["currently"].get("icon", None),
            precip_intensity=forcast["currently"].get("precipIntensity", None),
            precip_probability=forcast["currently"].get("precipProbability", None),
            precip_type=forcast["currently"].get("precipType", None),
            precip_accumulation=forcast["currently"].get("precipAccumulation", None),
            temperature=forcast["currently"].get("temperature", None),
            apparent_temperature=forcast["currently"].get("apparentTemperature", None),
            dew_point=forcast["currently"].get("dewPoint", None),
            humidity=forcast["currently"].get("humidity", None),
            pressure=forcast["currently"].get("pressure", None),
            wind_speed=forcast["currently"].get("windSpeed", None),
            wind_gust=forcast["currently"].get("windGust", None),
            wind_bearing=forcast["currently"].get("windBearing", None),
            cloud_cover=forcast["currently"].get("cloudCover", None),
            uv_index=forcast["currently"].get("uvIndex", None),
            visibility=forcast["currently"].get("visibility", None),
            ozone=forcast["currently"].get("ozone", None),
        )
