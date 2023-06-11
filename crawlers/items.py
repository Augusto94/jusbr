from scrapy.item import Field, Item


class ProcessoItem(Item):
    numero = Field()  # String
    data_distribuicao = Field()  # String
    assuntos = Field()  # String List
    classe = Field()  # String
    instancia = Field()  # String
    valor_acao = Field()  # Float
    area = Field()  # String
    status = Field()  # String
    juiz = Field()  # String
    vara = Field()  # String
    foro = Field()  # String
    orgao_julgador = Field()  # String
    spider = Field()  # String
    fonte = Field()  # String
    estado = Field()  # String
    justica = Field()  # String


class Parte(Item):
    nome = Field()  # String
    papel = Field()  # String
    advogados = Field()  # Dict List
    documento = Field()  # String


class Andamento(Item):
    titulo = Field()  # String
    data = Field()  # String
    texto = Field()  # String
