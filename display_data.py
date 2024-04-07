#  coding: utf-8
from typing import List, Any, NewType, Union

from convert_data import integers_to_bits

Matrix = NewType('Matrix', Union[List[List[Any]], List[Any]])


def print_matrix(rows: Matrix):
    for row in rows:
        for i in row:
            print(i, end='  ')
        print()


def print_integers_as_matrix_of_bits(rows: List[int]):
    bits = integers_to_bits(rows)
    print_matrix(bits)


def print_matrix_as_datraframe(matrix: Matrix, columns: List[str], index: List[str]):
    from pandas import DataFrame
    print(DataFrame.from_records(matrix, columns=columns, index=index))
