# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy


class JusbrSpiderBase(scrapy.Spider):
    def parse(self, response):
        yield from self.initial_step(response)
