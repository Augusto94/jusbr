# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from datetime import datetime

import scrapy

from crawlers.utils import format_npu


class JusbrSpiderBase(scrapy.Spider):
    items = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(JusbrSpiderBase, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_error, signal=scrapy.signals.spider_error)
        return spider

    def spider_error(self, spider, failure):
        spider.failure = failure

    def parse(self, response):
        yield from self.initial_step(response)

    def add_default_values(self, loader):
        loader.add_values(
            {
                "spider": self.name,
                "fonte": self.fonte,
                "estado": self.estado,
                "justica": self.justica,
                "termo_consulta": format_npu(self.numero),
                "last_crawled": datetime.now(),
            }
        )
