DEFAULT_FORMDATA = {
    "1 Grau": {
        "cbPesquisa": "NUMPROC",
        "dadosConsulta.tipoNuProcesso": "UNIFICADO",
    },
    "2 Grau": {
        "cbPesquisa": "NUMPROC",
        "tipoNuProcesso": "UNIFICADO",
    },
}

CONSULTA_KEY = {
    "1 Grau": "dadosConsulta.valorConsultaNuUnificado",
    "2 Grau": "dePesquisaNuUnificado",
}

XPATH_PROCESSO_BASE = (
    ".//span[contains(.,  '{field}')]//following-sibling::div//span//text() | .//span[contains(.,  '{field}')]//following-sibling::div/text()"
).format

XPATHS_PROCESSO = {
    "_processo": "//div[@class='unj-entity-header']",
    "_classe_cnj": XPATH_PROCESSO_BASE(field="Classe"),
    "_recurso": XPATH_PROCESSO_BASE(field="Recurso"),
    "_popup_senha": "//input[contains(@name, 'senhaProcesso')]",
    "_lista_processos": "//section[contains(@class, 'lista-processos')]//input/@value",
    "_lista_relacionados": "//ul[contains(@class, 'unj-list-row')]/li//a/@href",
    "numero": ".//span[contains(@class, 'unj-larger')]//text()",
    "data_distribuicao": XPATH_PROCESSO_BASE(field="Distribui"),
    "assuntos": XPATH_PROCESSO_BASE(field="ssunto"),
    "area": XPATH_PROCESSO_BASE(field="rea"),
    "valor_acao": XPATH_PROCESSO_BASE(field="Valor"),
    "juiz": f'{XPATH_PROCESSO_BASE(field="Juiz")} | {XPATH_PROCESSO_BASE(field="Relator")} | {XPATH_PROCESSO_BASE(field="Revisor")}',
    "vara": XPATH_PROCESSO_BASE(field="Vara"),
    "foro": XPATH_PROCESSO_BASE(field="Foro"),
    "classe": XPATH_PROCESSO_BASE(field="Classe"),
    "status": "//span[contains(@class, 'unj-tag')]/text()",
    "orgao_julgador": XPATH_PROCESSO_BASE(field="Julgador"),
}

XPATHS_PARTES = {
    "_tabela_completa": "//table[@id='tableTodasPartes']//tr",
    "_tabela_parcial": "//table[@id='tablePartesPrincipais']//tr",
    "papel": ".//td[1]//span//text()",
    "nome": ".//td[2]/text()[1]",
    "_advogados": ".//td[2]//span[@class='mensagemExibindo'] \
                  //following-sibling::text()",
}

XPATHS_ANDAMENTOS = {
    "_tabela_completa": "//tbody[@id='tabelaTodasMovimentacoes']//tr",
    "_tabela_parcial": "//tbody[@id='tabelaUltimasMovimentacoes']//tr",
    "data": ".//td[1]//text()",
    "titulo": ".//td[3]//text()",
    "texto": ".//td[3]/span/text()",
}
