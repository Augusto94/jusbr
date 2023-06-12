import os
import re

import pymongo

from crawlers.utils import format_npu


def parse_npu(numero: str) -> dict:
    """Parses the given NPU number into its components.

    Args:
        numero (str): The NPU number to be parsed.

    Returns:
        dict: A dictionary containing the parsed components of the NPU number:
            - 'sequencial': The sequential part of the NPU number.
            - 'digito': The digit part of the NPU number.
            - 'ano': The year part of the NPU number.
            - 'justica': The justice part of the NPU number.
            - 'tribunal': The court part of the NPU number.
            - 'origem': The origin part of the NPU number.

    Examples:
        >>> parse_npu('07004426920228020050')
        {
            'sequencial': '0700442',
            'digito': '69',
            'ano': '2022',
            'justica': '8',
            'tribunal': '02',
            'origem': '0050'
        }
    """
    numero = "".join(re.findall(r"\d+", numero))
    numero = numero.zfill(20)
    return {
        "sequencial": numero[0:7],
        "digito": numero[7:9],
        "ano": numero[9:13],
        "justica": numero[13:14],
        "tribunal": numero[14:16],
        "origem": numero[16:20],
    }


def get_processo_mongo(numero: str) -> list:
    """Retrieve process data from MongoDB based on the process number.

    Retrieves the process data from MongoDB by querying the database using the formatted NPU number.
    The NPU number is obtained by formatting the process number using the `format_npu` function.

    Args:
        numero: The process number.

    Returns:
        A list of process data documents retrieved from MongoDB.

    Note:
        - The function assumes the availability of a MongoDB server and the required environment variables.
    """
    npu = format_npu(numero)

    mongo_client = pymongo.MongoClient(os.getenv("MONGO_URL"))
    collection = mongo_client[os.getenv("MONGO_DB")][os.getenv("MONGO_COLLECTION")]

    processos = collection.find({"termo_consulta": npu}, {"_id": 0})

    return [processo for processo in processos]
