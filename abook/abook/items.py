# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AbookItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    category_url= scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    new_chapter = scrapy.Field()
    author = scrapy.Field()
    w_count = scrapy.Field()
    status = scrapy.Field()
    all_chapter = scrapy.Field()
    chapter_add = scrapy.Field()
    content = scrapy.Field()


