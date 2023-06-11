from crawlers.spiders.esaj.esaj import EsajSpiderBase


class TjalSpider(EsajSpiderBase):
    name = "tjal"
    estado = "AL"
    allowed_domains = ["www2.tjal.jus.br"]
    start_urls = [
        "https://www2.tjal.jus.br/cpopg/open.do",
        "https://www2.tjal.jus.br/cposg5/open.do",
    ]
