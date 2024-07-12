#  coding: utf-8

def difference(a: int, b: int) -> int:
    return abs(a - b)

def sort_dict_by_values(dictionary: dict[any: int]) -> dict[any: int]:
    """
    Ordena um dicionário de acordo com os valores
    Valores devem ser inteiros
    """
    return dict(sorted(dictionary.items(), key=lambda item: item[1]))

def sort_dict_by_keys(dictionary: dict[any: int]) -> dict[any: int]:
    """
    Ordena um dicionário de acordo com as chaves
    Chaves devem ser inteiros
    """
    return dict(sorted(dictionary.items(), key=lambda item: item[0]))