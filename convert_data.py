#  coding: utf-8
from copy import copy
from typing import List

from numpy import ndarray
import numpy as np

def int_to_bits(int_: int) -> List[int]:
    if int_ > 127:
        print('Warning: int_ > 127')
    return [int(i) for i in bin(int_)[2:].rjust(7, '0')]


def integers_to_bits(ints: List[int]):
    return [int_to_bits(i) for i in ints]


def to_matrix(bit_line: ndarray, group_size: int) -> List[ndarray]:
    final_groups = []
    for i in range(0, len(bit_line), group_size):
        final_groups.append(bit_line[i:i + group_size])

    return final_groups


def translate_array_values(array: ndarray, translation_dict: dict[any, any]):
    return [translation_dict[k] for k in array]


def translate_matrix_values(values: List[ndarray], translation_dicts: list[dict[any, any]]) -> List[ndarray]:
    translated = []
    for i in range(len(translation_dicts)):
        translated.append(translate_array_values(values[i], translation_dicts[i]))

    return translated

def to_dataframe(matrix: List[List[any]], columns: List[str] = None, index: List[str] = None):
    columns = columns or []
    index = index or []

    from pandas import DataFrame
    return DataFrame.from_records(matrix, columns=columns, index=index)


def get_sorted_indexes(array: ndarray):
    """
    Vou traduzir os números em um array para que cada um seja 
    representado por seu index no mesmo array caso este fosse ordenado
    
    P.Ex: 12, 18, 13, 17 se tornaria 1, 4, 2, 3, 
    pois este array ordenado seria 12, 13, 17, 18
    """
    sorted = [x for x in array]
    sorted.sort()
    translated = [np.where(sorted == i)[0][0] + 1 for i in array]
    return translated
