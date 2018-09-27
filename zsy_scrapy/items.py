# -*- coding: utf-8 -*-

from scrapy.loader.processors import MapCompose, TakeFirst, Join
import scrapy
from scrapy.loader import ItemLoader


class ZsyScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def repl(value):
    return value.replace("显示标题（细览页）", "")


class ActicleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ArticleItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field(
        input_processor=MapCompose(repl),
        output_processor=TakeFirst()
    )
    content = scrapy.Field(
        output_processor=Join("")
    )
    source = scrapy.Field()
    create_time = scrapy.Field()
    visits = scrapy.Field()
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    md5_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    state = scrapy.Field()
