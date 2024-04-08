#  coding: utf-8
from typing import List

from numpy import ndarray


def int_to_bits(int_: int) -> List[int]:
    if int_ > 127:
        print('Warning: int_ > 127')
    return [int(i) for i in bin(int_)[2:].rjust(7, '0')]


def integers_to_bits(ints: List[int]):
    return [int_to_bits(i) for i in ints]


def agglomerate_bits_from_bit_line(bit_line: ndarray, group_size: int) -> List[ndarray]:
    final_groups = []
    for i in range(0, len(bit_line), group_size):
        final_groups.append(bit_line[i:i + group_size])

    return final_groups


def translate_values(values: List[any], translation_dict: dict[any, any]) -> List[any]:
    return [translation_dict[val] for val in values]


def to_dataframe(matrix: List[List[any]], columns: List[str] = None, index: List[str] = None):
    columns = columns or []
    index = index or []

    from pandas import DataFrame
    return DataFrame.from_records(matrix, columns=columns, index=index)
