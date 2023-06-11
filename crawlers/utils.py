import re
import unicodedata

from dateparser.search import search_dates
from w3lib.html import remove_tags


def string_digits_only(text: str) -> str or None:
    """Extracts and returns a string containing only the digits from the input text.

    Args:
        text: The input text from which to extract the digits.

    Returns:
        A string containing only the digits found in the input text. If the input text is empty or None,
        None is returned.

    Example:
        >>> string_digits_only("abc123xyz456")
        '123456'

    Note:
        The function uses regular expressions to find and extract digits from the input text.
    """
    if not text:
        return None
    return "".join(re.findall(r"\d+", text))


def format_npu(numero_npu):
    """Formats the given NPU number into a specific pattern.

    Args:
        numero_npu (str): The NPU number to be formatted.

    Returns:
        str: The formatted NPU number in the pattern "{0}-{1}.{2}.{3}.{4}.{5}".

    Examples:
        >>> format_npu('07004426920228020050')
        '0700442-69.2022.8.02.0050'
    """
    numero = string_digits_only(numero_npu).zfill(20)
    npu = "{0}-{1}.{2}.{3}.{4}.{5}"
    return npu.format(
        numero[:7], numero[7:9], numero[9:13], numero[13], numero[14:16], numero[16:20]
    )


def filter_by_regex(pattern: str, string: str, sep: str = "", flags: int = 0) -> str:
    """Filter a string based on the input regex.

    Filters and returns a string based on your regex, after that a `join` is done using the `sep`
    that is received as an argument.

    Args:
        pattern: String with filter regex.
        string: String that will be applied to the regex.
        sep: Separator for string.

    Returns:
        String filtered by regex.

    Examples:
        >>> filter_by_regex(r'\d+', 'la12la21')
        '1221'
        >>> filter_by_regex(r'\w+', 'abcd#$')
        'abcd'
        >>> filter_by_regex(r'\d', '!@#$')
        ''
    """
    return sep.join(re.findall(pattern=pattern, string=string, flags=flags))


def normalize_spaces(string: str) -> str:
    """Normalize spaces in the string.

    Receives a string and removes unnecessary spaces through regex, keeping the line break.

    Args:
        string: String that will be normalized.

    Returns:
        Normalized string.

    Examples:
        >>> normalize_spaces('      jusbr \\n  lalala')
        'jusbr\\nlalala'
        >>> normalize_spaces(' jus br ')
        'jus br'
        >>> normalize_spaces(' ')
        ''
    """
    if not string or type(string) != str:
        return ""

    re_norm = re.compile(r"(?:\s*\n\s*)+", flags=re.UNICODE)
    cleared_value = filter_by_regex(r"[^\s]+|\n", string, " ", re.UNICODE)

    return re_norm.sub("\n", cleared_value).strip()


def clear_value(value: str) -> str:
    """Clears a string value by removing HTML tags and normalizing spaces.

    Args:
        value: The string value to be cleared.

    Returns:
        Cleared string value.

    Examples:
        >>> clear_value('<p>Hello, <b>World!</b></p>')
        'Hello, World!'
        >>> clear_value('   Hello   World   ')
        'Hello World'
        >>> clear_value(None)
        None
    """
    if isinstance(value, str):
        try:
            cleared_value = str(remove_tags(value))
            return normalize_spaces(cleared_value)
        except Exception:
            return value
    else:
        return value


def string_digits_only(text: str) -> str:
    """Extracts and returns a string containing only the digits from the input text.

    Args:
        text: The input text from which to extract the digits.

    Returns:
        A string containing only the digits found in the input text. If the input text is empty or None,
        None is returned.

    Examples:
        >>> string_digits_only("abc123xyz456")
        '123456'
    """
    if not text:
        return None
    return "".join(re.findall(r"\d+", text))


def parse_date(raw_date: str) -> str:
    """Parses a date string and returns it in a specific format.

    Args:
        date: The date string to be parsed.

    Returns:
        The parsed date string in the format "%Y-%m-%d %H:%M:%S" if successful, otherwise None.

    Examples:
        >>> parse_date("2023-06-09")
        '2023-06-09 00:00:00'
        >>> parse_date("Invalid date")
        None
    """
    if not raw_date:
        return raw_date

    date_search = search_dates(raw_date)
    date_parsed = date_search[0][1] if date_search else None

    return date_parsed.strftime("%Y-%m-%d %H:%M:%S") if date_parsed else None


def parse_money(text: str) -> float or None:
    """Parses a money string and returns the corresponding floating-point value.

    Args:
        text: The money string to be parsed.

    Returns:
        The parsed floating-point value if successful, otherwise None.

    Examples:
        >>> parse_money("USD 100.50")
        100.5
        >>> parse_money("Invalid input")
        None
    """
    if not text:
        return None

    dot_index = text.find(".")
    comma_index = text.find(",")

    if dot_index > 0 and comma_index > 0:
        index_value = dot_index - comma_index
        if index_value < 0:
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")

    if comma_index > 0:
        text = text.replace(",", "")

    text = "".join(re.findall(r"[\d+\.]", text))

    try:
        return float(text)
    except ValueError:
        return None


def no_special_characters(text: str) -> str or None:
    """Removes special characters from a string.

    Args:
        text: The string from which to remove special characters.

    Returns:
        The resulting string with special characters removed, or None if the input is empty.

    Examples:
        >>> no_special_characters("Hello, @World!")
        'Hello World'
        >>> no_special_characters("JusBR Project")
        JusBR Project
    """
    if not text:
        return None

    text_normalized = normalize_ascii(text)

    return " ".join([re.sub(r"[^a-zA-Z0-9]", "", s) for s in text_normalized.split(" ")])


def normalize_ascii(value: str) -> str:
    """Normalizes a string by removing non-ASCII characters.

    Args:
        value: The string to be normalized.

    Returns:
        The normalized string.

    Examples:
        >>> normalize_ascii("Café")
        'Cafe'
        >>> normalize_ascii("JusBR Project")
        'JusBR Project'
    """
    return unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("utf-8")


def alpha_characters_only(text: str) -> str or None:
    """Extracts and returns a string containing only alphabetic characters from the input text.

    Args:
        text: The input text from which to extract the alphabetic characters.

    Returns:
        A string containing only the alphabetic characters found in the input text. If the input text is empty or None,
        None is returned.

    Examples:
        >>> alpha_characters_only("abc123xyz")
        'abcxyz'
        >>> alpha_characters_only("Jus:br")
        Jusbr
    """
    if not text:
        return None
    return "".join(re.findall(r"[a-zA-Z]+", text))
