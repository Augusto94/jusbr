from crawlers.spiders.esaj.esaj import EsajSpiderBase


class TjceSpider(EsajSpiderBase):
    name = "tjce"
    estado = "CE"
    allowed_domains = ["esaj.tjce.jus.br"]
    start_urls = [
        "https://esaj.tjce.jus.br/cpopg/open.do",
        "https://esaj.tjce.jus.br/cposg5/open.do",
    ]
