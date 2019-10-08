# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DarkskyItem(scrapy.Item):
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    timezone = scrapy.Field()
    offset = scrapy.Field()

    # currently block
    time = scrapy.Field()
    icon = scrapy.Field()
    precip_intensity = scrapy.Field()
    precip_probability = scrapy.Field()
    precip_type = scrapy.Field()
    precip_accumulation = scrapy.Field()
    temperature = scrapy.Field()
    apparent_temperature = scrapy.Field()
    dew_point = scrapy.Field()
    humidity = scrapy.Field()
    pressure = scrapy.Field()
    wind_speed = scrapy.Field()
    wind_gust = scrapy.Field()
    wind_bearing = scrapy.Field()
    cloud_cover = scrapy.Field()
    uv_index = scrapy.Field()
    visibility = scrapy.Field()
    ozone = scrapy.Field()
