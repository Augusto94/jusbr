import re


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
