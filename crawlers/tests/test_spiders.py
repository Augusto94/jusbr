from crawlers.runner import run_spider
from crawlers.spiders.tjal.tjal import TjalSpider


def test_spider():
    # Testa captura de processo com ocorrência no 1º e 2º grau
    numero = "0710802-55.2018.8.02.0001"
    crawler = run_spider(spider=TjalSpider, numero=numero)
    items = crawler.spider.items

    assert len(items) == 3
    assert [item["numero"] == numero for item in items]
