from itemloaders.processors import Identity, MapCompose
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from crawlers import items, processors
from crawlers.utils import format_npu, parse_date, parse_money


class DefaultLoader(ItemLoader):
    default_input_processor = processors.DefaultInputProcessor()
    default_output_processor = processors.DefaultOutputProcessor()

    def add_xpaths(self, fields: dict) -> None:
        """Helper method to add XPath expressions for extracting data to the spider.

        Args:
            fields (dict): A dictionary where the keys represent the fields to extract and the values are the arguments
                to be passed to the add_xpath method.

        Note:
            Dictionary items with keys starting with '_' will be ignored.

        Returns:
            None
        """
        for field, args in fields.items():
            if not field or field.startswith("_"):
                continue

            args, kwargs = self._resolve_args(args)
            self.add_xpath(field, *args, **kwargs)

    def add_values(self, fields: dict) -> None:
        """Helper method to add a dictionary of values to the loader.

        Args:
            fields (dict): A dictionary containing field names as keys and their corresponding values as values.

        Note:
            Dictionary items with keys starting with '_' will be ignored.

        Returns:
            None
        """
        for field, args in fields.items():
            if not field or field.startswith("_"):
                continue

            args, kwargs = self._resolve_args(args)
            self.add_value(field, *args, **kwargs)

    def _resolve_args(self, args):
        kwargs = {}
        if not isinstance(args, tuple):
            args = (args,)
        elif isinstance(args[-1], dict):
            args, kwargs = args[:-1], args[-1]
        return args, kwargs


class ProcessoLoader(DefaultLoader):
    default_item_class = items.ProcessoItem

    numero_in = MapCompose(remove_tags, str.strip, format_npu)
    data_distribuicao_in = MapCompose(parse_date)
    valor_acao_in = MapCompose(parse_money)
    assuntos_out = Identity()


class ParteLoader(DefaultLoader):
    default_item_class = items.Parte

    papel_in = MapCompose(remove_tags, str.strip)
    advogados_out = Identity()


class AndamentoLoader(DefaultLoader):
    default_item_class = items.Andamento

    data_in = MapCompose(parse_date)
    title_in = MapCompose(str.strip)
