# JusBR

API para captura de dados de processos jurídicos nos sistemas públicos
da justiça brasileira.
Os dados são crawleados em tempo de execução e retornados de imediato para quem 
realiza a requisição.

## Pré-requisitos

Certifique-se de ter instalado os seguintes requisitos antes de executar o projeto:

- Docker
- Docker Compose

## Instalação

1. Clone o repositório:

   ```bash
   git clone git@github.com:Augusto94/jusbr.git
   ```

2. Acesse o diretório do projeto:

    ```bash
    cd jusbr
    ```

3. Execute o comando do Docker Compose para construir e iniciar o projeto:

    ```bash
    docker-compose up
    ```
    ou
    ```bash
    make start
    ```

Nesse momento a API estará disponível para consulta de processos.
## Utilização

Acesse a API em seu navegador na url `http://localhost:8000/docs/` e manipule a API de forma fácil através do swagger.
Ou através de ferramentas como o Postman:

 - Endpoint: http://localhost:8000/processo/
 - Método: POST
 - Parâmetros:
    - `{"numero": "0710802-55.2018.8.02.0001"}`: Número do processo de justiça no fomato de NPU. (O tribunal é extraído do número)

Um exemplo de request usando `curl` é:
```curl
curl -X 'POST' \
  'http://localhost:8000/processo' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "numero": "0050091-39.2021.8.06.0027"
}'
```

E um outro exemplo usando `python` seria:
```python
import requests

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

json_data = {
    'numero': '0050091-39.2021.8.06.0027',
}

response = requests.post('http://localhost:8000/processo', headers=headers, json=json_data)
print(response.json())
```

#### *Retorno padrão*
A API FastAPI receberá uma requisição com o número de um processo de justiça. Em seguida, ela disparará o crawler correspondente para obter as informações do processo e retornará as informações como resposta. O processo sempre será buscado tanto no 1º quando no 2º grau.

Exemplo de resposta em JSON:
```json
    {
        "1 Grau": [
            {
                "numero": "0700442-69.2022.8.02.0050",
                "data_distribuicao": "2022-05-12 00:00:00",
                "assuntos": [
                    "Práticas Abusivas"
                ],
                "area": "Cível",
                "valor_acao": 30466.96,
                "juiz": "Lívia Maria Mattos Melo Lima",
                "vara": "1ª Vara de Porto Calvo",
                "foro": "Foro de Porto Calvo",
                "classe": "Procedimento Comum Cível",
                "status": "Em grau de recurso",
                "instancia": "1 Grau",
                "spider": "tjal",
                "fonte": "esaj",
                "estado": "AL",
                "justica": "cível",
                "partes": [
                    {
                        "advogados": [
                            {
                                "nome": "Rafael Matos Gobira"
                            }
                        ],
                        "papel": "Autora",
                        "nome": "Elisângela da Silva Nascimento"
                    },
                    {
                        "advogados": [
                            {
                                "nome": "Rafael Goncalves Rocha"
                            },
                            {
                                "nome": "João Carlos Santos Oliveira"
                            }
                        ],
                        "papel": "Réu",
                        "nome": "BCP CLARO SA"
                    }
                ],
                "andamentos": [
                    {
                        "data": "2023-05-26 00:00:00",
                        "titulo": "Ato Publicado",
                        "texto": "Relação: 0244/2023\nData da Publicação: 29/05/2023\nNúmero do Diário: 3311"
                    },
                    {
                        "data": "2022-12-05 00:00:00",
                        "titulo": "Distribuído por Sorteio"
                    }
                ]
            }
        ],
        "2 Grau": [
            {
                "numero": "0700442-69.2022.8.02.0050",
                "assuntos": [
                    "Perdas e Danos"
                ],
                "area": "Cível",
                "valor_acao": 30466.96,
                "juiz": "DES. OTÁVIO LEÃO PRAXEDES",
                "classe": "Apelação Cível",
                "orgao_julgador": "2ª Câmara Cível",
                "instancia": "2 Grau",
                "spider": "tjal",
                "fonte": "esaj",
                "estado": "AL",
                "justica": "cível",
                "partes": [
                    {
                        "advogados": [
                            {
                                "nome": "Rafael Matos Gobira"
                            }
                        ],
                        "papel": "Apelante",
                        "nome": "Elisângela da Silva Nascimento"
                    },
                    {
                        "advogados": [
                            {
                                "nome": "Rafael Goncalves Rocha"
                            },
                            {
                                "nome": "João Carlos Santos Oliveira"
                            }
                        ],
                        "papel": "Apelado",
                        "nome": "BCP CLARO SA"
                    }
                ],
                "andamentos": [
                    {
                        "data": "2023-05-25 00:00:00",
                        "titulo": "Concluso ao Relator"
                    },
                    {
                        "data": "2023-05-25 00:00:00",
                        "titulo": "Processo Cadastrado"
                    }
                ]
            }
        ]
    }
```

Quando existir alguma dado encontrado para o processo, o retorno sempre ter 2 chaves: `1 Grau` e `2 Grau` com uma lista de objectos processo.
Isso acontece porque em alguns casos, pricipalmente no 2º grau, a consulta de um número pode retornar mais de uma ocorrência do processo. Por isso 
necessidade do retorno ser uma lista para cada instância.

Os campos possível que podem para o objeto processo são:

| Field Name  |  Type |
|:---|:---:|
| numero | **String** |
| data_distribuicao | **String** |
| assuntos | **List** |
| classe | **String** |
| instancia | **String** |
| valor_acao | **Float** |
| area | **String** |
| status | **String** |
| juiz | **String** |
| vara | **String** |
| foro | **String** |
| orgao_julgador | **String** |
| spider | **String** |
| fonte | **String** |
| estado | **String** |
| justica | **String** |
| partes | **List of dict** |
| andamentos |  **List of dict** |

> **Lembrando que alguns campos existem apenas para processos do 1º grau e outros somente para processos do 2º grau.**

#### *Detalhando o objeto **parte***
As partes de um processo são retornadas como uma lista de objetos ou lista de dicionácios python.  
Cada objeto parte tem os campos: `nome (string)`, `papel (string)` e `advogados (list of dict)`.  
O objeto advogado, por sua vez, possui o campo `nome (string)`. Essa estrutura foi adotada porque outros sistemas podem ter mais
informações além do nome do advogado e sendo assim o item já esta preparado para esses casos.  
Então, uma parte de um processo é composta pelo `nome`, `papel` e a `lista de advogados`.
Um exemplo de parte é:
```json
{
    "papel": "Apelado",
    "nome": "BCP CLARO SA",
    "advogados": [
        {
            "nome": "Rafael Goncalves Rocha"
        },
        {
            "nome": "João Carlos Santos Oliveira"
        }
    ]
}
```

#### *Detalhando o objeto **andamento***
Os andamentos de um processo são retornados como uma lista de objetos ou lista de dicionácios python.  
Cada andamento é composto pelos campos: `data (string)`, `titulo (string)` e `texto (string)`.
Um exemplo de andamento é:
```json
{
    "data": "2021-05-28 00:00:00",
    "titulo": "Processo apensado",
    "texto": "Apensado ao processo 0050049-24.2020.8.06.0027 - Classe: Execução Fiscal - Assunto principal: Dívida Ativa"
}
```

#### *Processo em segredo de justiça*
Quando o processo consultado se encontra em segredo de justiça a seguinte responta em JSON é retornada:

```json
{
    "detail": "O processo <numero> se encontra em segredo de justiça e não pôde ter suas informações capturadas."
}
```

#### *Processo não encontrado*
Quando o processo é consultado mas não é encontrada nenhuma informação no tribunal, a seguinte responta em JSON é retornada:

```json
{
    "detail": "Nenhuma informação foi encontrada para o número <numero>."
}
```

#### *Crawler não implementado*
Como o projeto ainda esta no início nem todos os tribunais estão disponíveis ainda.
Somente o `TJAL` e o `TJCE`' estão disponíveis por enquanto, então, seo usuário tentar
buscar informações de processos que não pertencem à esses tribunais, a seguinte responta em JSON é retornada:

```json
{
    "detail": "Nenhum crawler disponível para o coletar as informações do número {<numero>."
}
```

#### *Erro ao buscar informações do processo*
Por fim, algum pode pode ocorrer durante a captura dos dados do processo.
Instabilidadeou mudança do sistema do tribunal ou algum bug no crawler pode gerar um erro.
Nesses casos a seguinte responta em JSON é retornada:

```json
{
    "detail": "Houve um problema durante a execução do crawler e as informações do processo não foram capturadas."
}
```

## Testes

Para executar os testes automatizados, utilize o seguinte comando:
```bash
docker-compose run --rm app pytest --cov --cov-report term-missing --cov-fail-under 90 --disable-pytest-warnings
```
ou simplesmente:
```bash
make test
```

Executando esse comando o esperado é que os testes unitários do projeto sejam executados e ao final um relatório de cobertura 
é exibido. Como definido no comando, os testes só são considerados sucesso caso a cobertura esteja acima de 90%.

#### *Observação*
```
Os testes das spiders estão executando de fato as spiders ,fazendo as requests e etc. Um possível problema é que ao adicoionar
várias spiders ao projeto o tempo para rodar os testes pode ficar inviável. Uma solução seria fixar responses de exemplo e os
testes rodar baseado nesses exemplos. Perderia cobertura pois não rodaria o projeto por completo mas ganha escalabilidade e performance.
```

## Contribuição
Contribuições são bem-vindas! Se você quiser colaborar com o projeto, siga as etapas abaixo:

1. Faça um fork do repositório
2. Crie uma branch com sua feature (git checkout -b feature/MinhaFeature)
3. Faça commit das suas alterações (git commit -am 'Adiciona minha feature')
4. Faça push para a branch (git push origin feature/MinhaFeature)
5. Abra um Pull Request

## Observações e análise do projeto

#### *Stask das principais tecnologias utilizadas*
 - FastAPI
 - Scrapy
 - Docker
 - Docker Compose
 - Pytest

#### *Detalhes dos crawlers*
Como os dois tribunai implementados (`TJAL` e `TJCE`) pertecem ao mesmo sistema que é o `esaj` foi criada uma spider base do esaj
que implementa todo o fluxo de extração dos dados dos processos. Assim as spiders do `tjal` e `tjce` herdam dessa spider base e 
assim conseguimos evitar repetição de código e facilitar a manutenção.  
Essa decisão também facilita a criação de novos crawlers de tribunais que são do sistema `esaj`.  

Também foi criada uma spider base do projeto que adiciona métodos e atributos que são gerais a todos os crawlers, independente de for do `esaj` ou não.  

Por questão de organização cada spider possui uma pasta no projeto. Arquivos de constants, utils e etc que são espeíficos para cada spider devem ficar dentro
da pasta da spider.  
Como o nome sugere, no arquivo `constants.py` devem ficar todas as constantes das spiders, como `xpaths, urls, formulários de requests, etc`. Isso deixa o código
mais `clean` e fácil de manter.  
Ainda na pasta das spiders tem um arquivo chamado `arguments.yml` que contém exemplos de números de processos para facilitar os testes no ambiente de desenvolvimento. 

Para simplificar a lógica de extração, limpeza e transformação de dados foi feito o uso da ferramenta ItemLoader do scrapy. Com ele, entre outras coisas,
conseguimos padronizar o formato de saída dos campos e adicionar uma série de tratamentos permitindo que as spiders foquem mais na lógica de extração em si e
menos na manipulação detalhada dos dados extraídos.

#### *Possíveis problemas e soluções*

 - Como a API faz o disparo dos crawlers e fica aguardando o final da execução para retornar a response para o cliente,
em alguns casos, por diversos motivos, o crawler pode levar muito tempo para finalizar sua execução e isso pode gerar uma
experiência ruim para que esta requisitando os dados.  
Dependendo da necessidade de que requisita os dados, o que poderia ser feito para contornar esse problema seria a 
API disparar a execução do crawler e retornar de imediato a response informando o inicio do crawleamento.  
Após a spider finalizar poderia ser enviado para um serviço de mensageria os dados crawleados e a aplicação que requisitou poderia
consumir.

 - Seguindo nesse pensamento, uma outra melhoria seria separar a API e os crawlers em diferentes microserviços.  
Como os crawlers são uma parte crítica da aplicação, teria sua própria API para receber solicitações de crawling e retornar os resultados.  
A API principal faria chamadas para esse microserviço sempre que necessário. Essa abordagem oferece uma separação clara de responsabilidades e escalabilidade.

 - Para conseguir processar uma grande quantidade de solicitações será necessário utilizar uma fila de tarefas.  
Utilizar uma fila de tarefas, como o Celery, é uma opção eficiente para lidar com tarefas em segundo plano.  
Pode ser configurada uma fila onde cada mensagem na fila representa uma tarefa de crawling. A API adiciona uma 
tarefa na fila quando recebe uma solicitação e um worker processa as tarefas na fila, executando os crawlers conforme necessário.  
Dessa forma, a API pode retornar rapidamente, e o crawling é tratado em segundo plano e em um outro microserviço.  

## Contato

`email`: **augustoarl@gmail.com**
`redes sociais`: **@augustoarl**
