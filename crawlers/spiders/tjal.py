from crawlers.spiders import JusbrSpiderBase


class TjalSpider(JusbrSpiderBase):
    name = "tjal"
    allowed_domains = ["www2.tjal.jus.br"]
    start_urls = [
        "https://www2.tjal.jus.br/cpopg/open.do",
        "https://www2.tjal.jus.br/cposg5/open.do",
    ]

    def __init__(self, numero=None, *args, **kwargs):
        super(TjalSpider, self).__init__(*args, **kwargs)
        self.numero = numero
        self.initial_step = self.consultar_processo

    def consultar_processo(self, response):
        yield
