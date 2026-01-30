from typing import Optional
from json import load
from pprint import pprint


def decodage_regle(source: dict, operator: Optional[str]=None):
    result: str = ""
    first: bool = True

    if isinstance(source, dict):
        operator = source.get("operator")
        if operator:
            result += "NOT" if operator == "NOT" else ""
            result += "("
            result += decodage_regle(source.get("components", []), operator)
            result += ")"

        else:
            raise Exception("Erreur", "pas d'operateur")

    elif isinstance(source, list):
        for element in source:
            if first:
                first = False
            else:
                result += f" {operator} "

            fonction = element.get("fonction")
            if fonction is None:
                result += decodage_regle(element)

            else:
                args = tuple(element.get("args",()))
                result += f"{fonction}{args}"

    else:
        raise Exception("Erreur", "type source inconnu")

    return result

try:
    with open("rule_test.json") as file_handle:
        rules = load(file_handle)

    print(decodage_regle(rules))
except Exception as e:
    print(e)
