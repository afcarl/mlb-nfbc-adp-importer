# -*- coding: utf-8 -*-
import re
import urlparse

import scrapy
from scrapy.exceptions import CloseSpider

from ..items import Loader, Ranking


POS_LIST = (
    'C', '1B', '2B', 'SS', '3B', 'OF',
    'SP', 'RP',
    'DH',
)

PAGE_URL = 'http://hosted.stats.com/mlb/adp.asp?pos=all&page={}'
POS_URL = 'http://hosted.stats.com/mlb/adp.asp?pos={}'

class ADPSpider(scrapy.Spider):
    """
    Scrapes NFBC ADP tables.

    Scraping can happen one of two ways:
    
    1. Collect all players in a user-defined page range,
        via `-a page_count` crawler CLI option
    2. Collect all players by position pages (default)

    Warning:
        STATS's paginated data tables have a pagination problem.
        As of this commit, page 15 stops nearly half-way through
        the player list, and does not offer a link to page 16.
        Thus, players 724-749 are missing. By-position pages
        also only include players 1-723.

        Until this is fixed, it's recommended to use the brute force
        pagination method, as it collects the most data.
    """

    name = 'nfbcadp'
    allowed_domains = ['stats.com']

    def __init__(self, page_count=None, *a, **kw):
        super(ADPSpider, self).__init__(*a, **kw)

        # generate a range of pages from 1 through `page_count`
        if page_count is not None:
            page_count = int(page_count)

            if page_count <= 1:
                page_count = 2

            self.start_urls = [
                PAGE_URL.format(n)
                for n in range(1, page_count + 1)
            ]

            self.logger.info('Selecting all from pages 1-{}'.format(
                             page_count))
        else:
            # generate a list of position url
            self.start_urls = [
                ''.format(pos)
                for pos in POS_LIST
            ]
            self.logger.info('Selecting all by position')

    def parse(self, response):
        rows = response.css(
            'div#shsMLBADP'
            ' table.shsTable.shsBorderTable'
            '  tr:not(.shsTableTtlRow)'
        )

        self.logger.debug('{} - Found {} rows'.format(
                          response.url, len(rows)))

        for row in rows:
            # extract single-player ranking from row
            loader = Loader(Ranking(), row)

            # extract player information
            player = row.css('td:nth-of-type(2) a')
            player_url = player.css('::attr(href)').extract_first()
            player_url = urlparse.urljoin(response.url, player_url)
            url_bits = urlparse.urlparse(player_url)

            loader.add_value('player_url', player_url)
            loader.add_value('player_name',
                             player.css('::text').extract_first())
            loader.add_value('player_id',
                             urlparse.parse_qs(url_bits.query)['id'][0])

            loader.add_css('team_name', 'td:nth-of-type(3)::text')
            loader.add_css('pos', 'td:nth-of-type(4)::text')
            loader.add_css('avg_pick', 'td:nth-of-type(5)::text')
            loader.add_css('min_pick', 'td:nth-of-type(6)::text')
            loader.add_css('max_pick', 'td:nth-of-type(7)::text')

            yield loader.load_item()
