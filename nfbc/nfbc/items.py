# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


__all__ = ('Loader', 'Ranking', )

class Loader(ItemLoader):
    default_output_processor = TakeFirst()


class Ranking(scrapy.Item):
    player_id = scrapy.Field()
    player_name = scrapy.Field()
    player_url = scrapy.Field()
    team_name = scrapy.Field()
    pos = scrapy.Field()
    avg_pick = scrapy.Field()
    min_pick = scrapy.Field()
    max_pick = scrapy.Field()
