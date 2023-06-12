import pytest

from crawlers import utils


@pytest.mark.parametrize(
    "text, expected_result",
    [
        ("abc123xyz456", "123456"),
        ("Hello, @World!", ""),
        ("", None),
        (None, None),
    ],
)
def test_string_digits_only(text, expected_result):
    assert utils.string_digits_only(text) == expected_result


@pytest.mark.parametrize(
    "numero_npu, expected_result",
    [
        ("07004426920228020050", "0700442-69.2022.8.02.0050"),
        ("12345678901234567890", "1234567-89.0123.4.56.7890"),
    ],
)
def test_format_npu(numero_npu, expected_result):
    assert utils.format_npu(numero_npu) == expected_result


@pytest.mark.parametrize(
    "pattern, string, sep, flags, expected_result",
    [
        (r"\d+", "la12la21", "", 0, "1221"),
        (r"\w+", "abcd#$", "", 0, "abcd"),
        (r"\d", "!@#$", "", 0, ""),
    ],
)
def test_filter_by_regex(pattern, string, sep, flags, expected_result):
    assert utils.filter_by_regex(pattern, string, sep, flags) == expected_result


@pytest.mark.parametrize(
    "string, expected_result",
    [
        ("      jusbr \n  lalala", "jusbr\nlalala"),
        (" jus br ", "jus br"),
        (" ", ""),
        ("", ""),
        (None, ""),
    ],
)
def test_normalize_spaces(string, expected_result):
    assert utils.normalize_spaces(string) == expected_result


@pytest.mark.parametrize(
    "value, expected_result",
    [
        ("<p>Hello, <b>World!</b></p>", "Hello, World!"),
        ("   Hello   World   ", "Hello World"),
        (None, None),
    ],
)
def test_clear_value(value, expected_result):
    assert utils.clear_value(value) == expected_result


@pytest.mark.parametrize(
    "raw_date, expected_result",
    [
        ("2023-06-09", "2023-06-09 00:00:00"),
        ("Invalid date", None),
        ("", ""),
    ],
)
def test_parse_date(raw_date, expected_result):
    assert utils.parse_date(raw_date) == expected_result


@pytest.mark.parametrize(
    "text, expected_result",
    [
        ("USD 100.50", 100.5),
        ("Invalid input", None),
        ("", None),
    ],
)
def test_parse_money(text, expected_result):
    assert utils.parse_money(text) == expected_result


@pytest.mark.parametrize(
    "text, expected_result",
    [
        ("Hello, @World!", "Hello World"),
        ("JusBR Project", "JusBR Project"),
        ("", None),
    ],
)
def test_no_special_characters(text, expected_result):
    assert utils.no_special_characters(text) == expected_result


@pytest.mark.parametrize(
    "text, expected_result",
    [
        ("-JusBr:", "JusBr"),
        ("@JusBR Project", "JusBR Project"),
        ("Apelante:", "Apelante"),
        ("", None),
    ],
)
def test_alpha_characters_only(text, expected_result):
    assert utils.alpha_characters_only(text) == expected_result
