from multiprocessing import Manager
from multiprocessing.context import Process

from fastapi import FastAPI, HTTPException, status

from api.constants import TRIBUNAL2SPIDER
from api.schema import ProcessoInputDTO
from api.utils import parse_npu
from crawlers.runner import run_spider

app = FastAPI()


@app.get("/")
async def health_check() -> dict:
    return {"status": "healthy"}


@app.post("/processo")
def crawl_processo(processo: ProcessoInputDTO) -> dict:
    numero = processo.numero
    npu_parsed = parse_npu(numero)
    spider = TRIBUNAL2SPIDER.get(npu_parsed.get("tribunal"))
    if not spider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nenhum crawler disponível para o coletar as informações do número {numero}.",
        )

    # Create, start and wait for the crawler to run in a separate process
    manager = Manager()
    context = manager.dict()

    process = Process(target=run_spider, args=(spider, numero, context))
    process.start()
    process.join()

    if context["failure"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Houve um problema durante a execução do crawler e as informações do processo não foram capturadas.",
        )
    elif context["segredo_justica"]:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"O processo {numero} se encontra em segredo de justiça e não pôde ter suas informações capturadas.",
        )
    elif context["data"].get("1 Grau", []) or context["data"].get("2 Grau", []):
        return context["data"]
    else:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"Nenhuma informação foi encontrada para o número {numero}.",
        )
