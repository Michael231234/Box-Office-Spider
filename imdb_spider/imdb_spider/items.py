# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie = scrapy.Field()
    genre = scrapy.Field()
    rate = scrapy.Field()
    country = scrapy.Field()
    review = scrapy.Field()
    movie_url = scrapy.Field()
    cast = scrapy.Field()
    year = scrapy.Field()
    RatePeople = scrapy.Field()
    Production = scrapy.Field()
    runTime = scrapy.Field()
    pass
