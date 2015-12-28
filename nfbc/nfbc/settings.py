# -*- coding: utf-8 -*-

BOT_NAME = 'nfbc'

SPIDER_MODULES = ['nfbc.spiders']
NEWSPIDER_MODULE = 'nfbc.spiders'

USER_AGENT = 'nfbc-adp-spider (+http://www.github.com/mattdennewitz/nfbc-adp-spider)'

CONCURRENT_REQUESTS = 2

FEED_EXPORT_FIELDS = [
    'player_id', 'player_url', 'player_name',
    'team_name', 'pos', 'avg_pick', 'min_pick', 'max_pick'
]
