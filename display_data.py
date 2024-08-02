#  coding: utf-8
from typing import List, Any, NewType, Union, Tuple

from convert_data import get_sorted_indexes, integers_to_bits, translate_matrix_values

Matrix = NewType('Matrix', Union[List[List[Any]], List[Any]])
Point = NewType('Point', Tuple[int, int])


def print_matrix(rows: Matrix):
    for row in rows:
        for i in row:
            print(i, end='  ')
        print()


def print_integers_as_matrix_of_bits(rows: List[int]):
    bits = integers_to_bits(rows)
    print_matrix(bits)


def print_matrix_as_dataframe(matrix: Matrix, columns: List[str], index: List[str]):
    from pandas import DataFrame
    print(DataFrame.from_records(matrix, columns=columns, index=index))


def print_translated_matrix(mtrx, translation_dicts, columns, rows):
    mtrx = [get_sorted_indexes(row) for row in mtrx]
    translated = translate_matrix_values(mtrx, translation_dicts)
    print_matrix_as_dataframe(translated, columns=columns, index=rows)


def trace_route_between_points(points: List[Point]):
    import matplotlib.pyplot as plt
    for i in range(0, len(points)):
        x1, x2 = points[i][0], points[(i+1) % len(points)][0]
        y1, y2 = points[i][1], points[(i+1) % len(points)][1]
        plt.plot([x1, x2], [y1, y2], 'ro-')

    plt.grid(axis='x', color='0.95')
    plt.grid(axis='y', color='0.95')
    plt.show()
