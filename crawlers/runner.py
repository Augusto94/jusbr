from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings


def run_spider(spider: Spider, numero: str) -> None:
    """Runs a spider to scrape data based on the provided Spider instance.

    Args:
        spider (Spider): The Spider instance to be used for scraping.
        numero (str): The number parameter to be passed to the spider.
        context (Manager): The context object to store the scraped data.

    Returns:
        None
    """
    process = CrawlerProcess(get_project_settings())
    crawler = process.create_crawler(spider)
    process.crawl(crawler, numero=numero)
    process.start(stop_after_crawl=True, install_signal_handlers=False)

    return crawler
