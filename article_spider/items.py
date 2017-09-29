# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
import re


def add_jobbole(value):
    return value+"-jobbole"


def get_date(value):
    re_match = re.match("([0-9/]*).*?", value.strip())
    if re_match:
        create_date = re_match.group(1)
    else:
        create_date = " "
    return create_date


def get_comment_num(value):
    re_match = re.match(".*?(\d+).*", value)
    if re_match:
        comment_num = re_match.group(1)
    else:
        comment_num = 0
    return comment_num


def get_fav_num(value):
    re_match = re.match(".*?(\d+).*", value)
    if re_match:
        fav_num = re_match.group(1)
    else:
        fav_num = 0
    return fav_num


class ArticleSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    webpage_image_url = scrapy.item.Field()
    title = scrapy.item.Field(
        output_processor=TakeFirst()
    )
    create_date = scrapy.item.Field(
        input_processor=MapCompose(get_date),
        output_processor=TakeFirst()
    )
    article_type = scrapy.item.Field(
        output_processor=TakeFirst()
    )
    praise_num = scrapy.item.Field(
        output_processor=TakeFirst()
    )
    fav_num = scrapy.item.Field(
        input_processor=MapCompose(get_fav_num),
        output_processor=TakeFirst()
    )
    comment_num = scrapy.item.Field(
        input_processor=MapCompose(get_comment_num),
        output_processor=TakeFirst()
    )
    pass
