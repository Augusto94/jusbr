from crawlers.spiders import JusbrSpiderBase


class TjceSpider(JusbrSpiderBase):
    name = "tjce"
    allowed_domains = ["esaj.tjce.jus.br"]
    start_urls = [
        "https://esaj.tjce.jus.br/cpopg/open.do",
        "https://esaj.tjce.jus.br/cposg5/open.do",
    ]

    def __init__(self, numero=None, *args, **kwargs):
        super(TjceSpider, self).__init__(*args, **kwargs)
        self.numero = numero
        self.initial_step = self.consultar_processo

    def consultar_processo(self, response):
        yield
