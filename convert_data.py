#  coding: utf-8
from typing import List


def int_to_bits(int_: int) -> List[int]:
    if int_ > 127:
        print('Warning: int_ > 127')
    return [int(i) for i in bin(int_)[2:].rjust(7, '0')]


def integers_to_bits(ints: List[int]):
    return [int_to_bits(i) for i in ints]


def agglomerate_bits_from_bit_line(bit_line: List[int], group_size: int) -> List[List[int]]:
    final_groups = []
    for i in range(0, len(bit_line), group_size):
        final_groups.append(bit_line[i:i + group_size])

    return final_groups
