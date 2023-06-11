from scrapy.http import FormRequest, Request

from crawlers.loaders import AndamentoLoader, ParteLoader, ProcessoLoader
from crawlers.spiders import JusbrSpiderBase
from crawlers.spiders.esaj.constants import (
    CONSULTA_KEY,
    DEFAULT_FORMDATA,
    XPATHS_ANDAMENTOS,
    XPATHS_PARTES,
    XPATHS_PROCESSO,
)


class EsajSpiderBase(JusbrSpiderBase):
    fonte = "esaj"
    justica = "cível"
    custom_settings = {
        "COOKIES_ENABLED": True,
    }

    def __init__(self, numero=None, *args, **kwargs):
        super(EsajSpiderBase, self).__init__(*args, **kwargs)
        self.numero = numero
        self.initial_step = self.consultar_processo

    def consultar_processo(self, response):
        instancia = "1 Grau" if "cpopg" in response.url else "2 Grau"

        formdata = DEFAULT_FORMDATA[instancia].copy()
        formdata[CONSULTA_KEY[instancia]] = self.numero

        yield FormRequest(
            url=response.urljoin("search.do"),
            formdata=formdata,
            callback=self.verificar_consulta,
            cb_kwargs={"instancia": instancia},
        )

    def verificar_consulta(self, response, instancia):
        numero_processo = response.xpath(XPATHS_PROCESSO["numero"]).get()
        if numero_processo and numero_processo.strip():
            yield from self.extrair_processo(response, instancia)
        elif response.xpath(XPATHS_PROCESSO["_lista_processos"]):
            for processo_id in response.xpath(XPATHS_PROCESSO["_lista_processos"]).getall():
                yield Request(
                    url=response.urljoin(f"show.do?processo.codigo={processo_id}"),
                    callback=self.verificar_consulta,
                    method="GET",
                    cb_kwargs={"instancia": instancia},
                )
        elif response.xpath(XPATHS_PROCESSO["_lista_relacionados"]):
            for url_relacionado in response.xpath(XPATHS_PROCESSO["_lista_relacionados"]).getall():
                yield Request(
                    url=response.urljoin(url_relacionado),
                    callback=self.verificar_consulta,
                    method="GET",
                    cb_kwargs={"instancia": instancia},
                )
        elif response.xpath(XPATHS_PROCESSO["_popup_senha"]):
            self.segredo_justica = True

    def extrair_processo(self, response, instancia):
        processo = response.xpath(XPATHS_PROCESSO["_processo"])
        loader = ProcessoLoader(selector=processo)
        loader.add_xpaths(XPATHS_PROCESSO)
        loader.add_value("instancia", instancia)

        self.add_default_values(loader)

        item = loader.load_item()
        item_processo = dict(item)

        self.extrair_partes(response, item_processo)
        self.extrair_andamentos(response, item_processo)

        self.dados_processo.setdefault(instancia, []).append(item_processo)

        yield item_processo

    def extrair_partes(self, response, item):
        partes = response.xpath(XPATHS_PARTES["_tabela_completa"])
        if not partes:
            partes = response.xpath(XPATHS_PARTES["_tabela_parcial"])

        for parte in partes:
            loader = ParteLoader(selector=parte)
            raw_advogados = parte.xpath(XPATHS_PARTES["_advogados"]).extract()
            if raw_advogados:
                advogados = [advogado.strip() for advogado in raw_advogados if advogado.strip()]
                advogados_final = [{"nome": advogado} for advogado in advogados]
                loader.add_value("advogados", advogados_final)

            loader.add_xpaths(XPATHS_PARTES)
            item_parte = loader.load_item()
            item.setdefault("partes", []).append(dict(item_parte))

    def extrair_andamentos(self, response, item):
        andamentos = response.xpath(XPATHS_ANDAMENTOS["_tabela_completa"])
        if not andamentos:
            andamentos = response.xpath(XPATHS_ANDAMENTOS["_tabela_parcial"])

        for andamento in andamentos:
            loader = AndamentoLoader(selector=andamento)
            loader.add_xpaths(XPATHS_ANDAMENTOS)

            item_andamento = loader.load_item()
            item.setdefault("andamentos", []).append(dict(item_andamento))
