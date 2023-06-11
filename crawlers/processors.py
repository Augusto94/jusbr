from crawlers.utils import clear_value


class DefaultInputProcessor:
    def __call__(self, input_values: list) -> list:
        processed_values = []
        for value in input_values:
            if isinstance(value, str):
                processed_value = clear_value(value)
                if processed_value is not None and processed_value != "":
                    processed_values.append(processed_value)
            elif isinstance(value, dict):
                processed_dict_values = {
                    clear_value(key): clear_value(val) for key, val in value.items()
                }
                processed_values.append(processed_dict_values)
            else:
                processed_values.append(value)

        return processed_values


class DefaultOutputProcessor:
    def __call__(self, output_values):
        if isinstance(output_values, str):
            return str(output_values).strip()
        elif isinstance(output_values, list):
            return output_values[0]
        else:
            return output_values
