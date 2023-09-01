from typing import Any


def is_sublist(lst_referencia: list[Any], lst_buscar: list[Any]) -> bool:
    return all(x in lst_referencia for x in lst_buscar)
