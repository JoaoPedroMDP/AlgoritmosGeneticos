#  coding: utf-8
from typing import List, Any, NewType, Union

from convert_data import integers_to_bits

Matrix = NewType('Matrix', Union[List[List[Any]], List[str]])


def print_matrix(rows: Matrix):
    for row in rows:
        for i in row:
            print(i, end=' ')
        print()


def print_integers_as_matrix_of_bits(rows: List[int]):
    bits = integers_to_bits(rows)
    print_matrix(bits)
