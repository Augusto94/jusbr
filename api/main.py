from multiprocessing.context import Process

from fastapi import FastAPI, HTTPException, status

from api.constants import TRIBUNAL2SPIDER
from api.schema import ProcessoInputDTO
from api.utils import get_processo_mongo, parse_npu
from crawlers.runner import run_spider
from crawlers.utils import format_npu

app = FastAPI()


@app.get("/")
async def health_check() -> dict:
    return {"status": "healthy"}


@app.post("/crawl")
def crawl_processo(processo: ProcessoInputDTO) -> dict:
    """Initiate the execution of a crawler to gather information about a process.

    Initiates the execution of a specific crawler to gather information about a process based on its number.
    The crawler runs in a separate process and collects the data, which will be available at the /processo/{numero} endpoint.

    Args:
        processo (ProcessoInputDTO): The process information, including the process number.

    Returns:
        dict: A dictionary containing a message indicating that the data collection has started.

    Raises:
        HTTPException: If no crawler is available to collect the information for the given process number.

    Examples:
        >>> processo = ProcessoInputDTO(numero='07004426920228020050')
        >>> crawl_processo(processo)
        {'message': 'The process data collection for number 07004426920228020050 has started. Once completed, the data will be available at the /processo/07004426920228020050 endpoint.'}

        >>> processo = ProcessoInputDTO(numero='1234567890')
        >>> crawl_processo(processo)
        HTTPException: 400 BAD REQUEST - No crawler is available to collect the information for the given number 1234567890.

    Note:
        - This endpoint assumes the availability of specific spiders defined in the `TRIBUNAL2SPIDER` mapping.
        - The `format_npu` function is used to format the process number into a specific pattern.
        - The `parse_npu` function is used to parse the components of the process number.
        - The `run_spider` function is responsible for starting the crawler and collecting the data.
        - The collected data will be available at the `/processo/{numero}` endpoint once the process is completed.
    """
    numero = processo.numero
    npu = format_npu(numero)
    npu_parsed = parse_npu(numero)

    spider = TRIBUNAL2SPIDER.get(npu_parsed.get("tribunal"))
    if not spider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nenhum crawler disponível para o coletar as informações do número {numero}.",
        )

    # Create, start and wait for the crawler to run in a separate process
    process = Process(target=run_spider, args=(spider, npu))
    process.start()

    return {
        "detail": f"A captura dos dados do processo {numero} foi iniciada. Ao finalizar os dados estarão disponíveis no endpoint /processo/{numero}."
    }


@app.get("/processo/{numero}")
def get_processo(numero: str) -> list:
    """Get information about a process based on its number.

    Retrieves information about a process from the MongoDB database based on the provided process number.

    Args:
        numero (str): The number of the process to retrieve.

    Returns:
        list: A list containing information about the process.

    Raises:
        HTTPException: If the requested process does not exist in the database.

    Note:
        This endpoint assumes the availability of a MongoDB database containing process information.
        The `get_processo_mongo` function is responsible for querying the MongoDB database.
    """
    processo_list = get_processo_mongo(numero)
    if not processo_list:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"O processo {numero} ainda não existe em nossa base de dados.",
        )

    return processo_list
