import pytest

from api.utils import parse_npu


@pytest.mark.parametrize(
    "numero, expected_result",
    [
        (
            "07004426920228020050",
            {
                "sequencial": "0700442",
                "digito": "69",
                "ano": "2022",
                "justica": "8",
                "tribunal": "02",
                "origem": "0050",
            },
        ),
        (
            "12345678901234567890",
            {
                "sequencial": "1234567",
                "digito": "89",
                "ano": "0123",
                "justica": "4",
                "tribunal": "56",
                "origem": "7890",
            },
        ),
    ],
)
def test_parse_npu(numero, expected_result):
    assert parse_npu(numero) == expected_result
