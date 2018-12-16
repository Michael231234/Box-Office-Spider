# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoxofficeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie = scrapy.Field()
    box_office = scrapy.Field()
    year = scrapy.Field()
    distributor = scrapy.Field()
    pass
