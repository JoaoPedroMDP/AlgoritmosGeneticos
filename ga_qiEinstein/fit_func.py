#  coding: utf-8
import os

import numpy as np
from pygad import GA

from convert_data import to_matrix, get_sorted_indexes
from display_data import Matrix, print_matrix
from ga_qiEinstein import METADATA


SHOULD_PRINT = False
ERROR_WEIGHT = 5
ABSOLUTE_ERROR_WEIGHT = 200
VALUES_OCCURRENCE: dict = {}

def process_value(value: int):
    absol = abs(value)

    if absol >= ABSOLUTE_ERROR_WEIGHT:
        return (absol // ABSOLUTE_ERROR_WEIGHT) * ABSOLUTE_ERROR_WEIGHT

    if absol > 100:
        return (absol // 100) * 100

    if absol > 10:
        return (absol // 10) * 10

    return absol

def add_value_occurrence(value: int):
    processed = process_value(value)

    if processed not in VALUES_OCCURRENCE:
        VALUES_OCCURRENCE[processed] = 0
    VALUES_OCCURRENCE[processed] += 1


def set_should_print(value: bool):
    global SHOULD_PRINT
    SHOULD_PRINT = value

def locate_house(matrix: Matrix, row: str, item: str):
    mrow = matrix[METADATA[row]['row_index']]
    item = METADATA[row]['data_dictionary'][item]

    try:
        index = mrow.index(item)
    except Exception as e:
        print(mrow)
        print(item)
        print(e)
        raise e
    
    return index

def fit(bitline: np.ndarray, debug=False):
    mtrx = to_matrix(bitline, 5)
    SHOULD_PRINT and print("---------------------------")
    SHOULD_PRINT and print_matrix(mtrx)
    mtrx = [get_sorted_indexes(row) for row in mtrx]
    SHOULD_PRINT and print_matrix(mtrx)
    SHOULD_PRINT and print("---------------------------")

    error = 0

    # Posições reutilizáveis
    green_house_index = locate_house(mtrx, 'Cor', 'VERDE')
    dunhill_house_index = locate_house(mtrx, 'Cigarro', 'DUNHILL')
    blend_house_index = locate_house(mtrx, 'Cigarro', 'BLEND')

    # Regra 1: Norueguês na casa 0
    norwish_house_index = locate_house(mtrx, 'Nacionalidade', 'NORUEGUES')
    error += ABSOLUTE_ERROR_WEIGHT * (norwish_house_index - 0)

    # Regra 2: Inglês na casa vermelha
    red_house_index = locate_house(mtrx, 'Cor', 'VERMELHO')
    english_house_index = locate_house(mtrx, 'Nacionalidade', 'INGLES')
    error += ERROR_WEIGHT * abs(red_house_index - english_house_index)

    # Regra 3: Sueco tem cachorro
    dog_house_index = locate_house(mtrx, 'Animal', 'CACHORRO')
    swedish_house_index = locate_house(mtrx, 'Nacionalidade', 'SUECO')
    error += ERROR_WEIGHT * abs(dog_house_index - swedish_house_index)

    # Regra 4: O Dinamarquês toma chá
    tea_house_index = locate_house(mtrx, 'Bebida', 'CHA')
    danish_house_index = locate_house(mtrx, 'Nacionalidade', 'DINAMARQUES')
    error += ERROR_WEIGHT * abs(tea_house_index - danish_house_index)

    # Regra 5: A casa verde está à esquerda da casa branca
    white_house_index = locate_house(mtrx, 'Cor', 'BRANCO')
    error += abs((white_house_index - 1) - green_house_index)

    # Regra 6: O dono da casa verde bebe café
    coffee_house_index = locate_house(mtrx, 'Bebida', 'CAFE')
    error += ERROR_WEIGHT * abs(coffee_house_index - green_house_index)

    # Regra 7: O homem que fuma Pall Mall tem pássaros
    pallmall_house_index = locate_house(mtrx, 'Cigarro', 'PALLMALL')
    bird_house_index = locate_house(mtrx, 'Animal', 'PASSARO')
    error += ERROR_WEIGHT * abs(pallmall_house_index - bird_house_index)

    # Regra 8: O homem que vive na casa amarela fuma Dunhill
    yellow_house_index = locate_house(mtrx, 'Cor', 'AMARELO')
    error += ERROR_WEIGHT * abs(yellow_house_index - dunhill_house_index)

    # Regra 9: O homem que vive na casa do meio bebe leite
    middle_house_index = 2
    milk_house_index = locate_house(mtrx, 'Bebida', 'LEITE')
    error += ABSOLUTE_ERROR_WEIGHT * abs(middle_house_index - milk_house_index)

    # Regra 10: O homem que fuma Blends vive ao lado do que tem gatos
    cat_house_index = locate_house(mtrx, 'Animal', 'GATO')
    error += abs(abs(blend_house_index - cat_house_index) - 1)

    # Regra 11: O homem que tem cavalos vive ao lado do que fuma Dunhill
    horse_house_index = locate_house(mtrx, 'Animal', 'CAVALO')
    error += abs(abs(horse_house_index - dunhill_house_index) - 1)

    # Regra 12: O homem que fuma Blue Master bebe cerveja
    bluemaster_house_index = locate_house(mtrx, 'Cigarro', 'BLUEMASTER')
    beer_house_index = locate_house(mtrx, 'Bebida', 'CERVEJA')
    error += ERROR_WEIGHT * abs(bluemaster_house_index - beer_house_index)

    # Regra 13: O alemão fuma Prince
    german_house_index = locate_house(mtrx, 'Nacionalidade', 'ALEMAO')
    prince_house_index = locate_house(mtrx, 'Cigarro', 'PRINCE')
    error += ERROR_WEIGHT * abs(german_house_index - prince_house_index)

    # Regra 14: O Norueguês vive ao lado da casa Azul
    norwegian_house_index = locate_house(mtrx, 'Nacionalidade', 'NORUEGUES')
    blue_house_index = locate_house(mtrx, 'Cor', 'AZUL')
    error += abs(abs(norwegian_house_index - blue_house_index) - 1)

    # Regra 15: O homem que fuma Blends vive ao lado do que bebe água
    water_house_index = locate_house(mtrx, 'Bebida', 'AGUA')
    error += abs(abs(blend_house_index - water_house_index) - 1)

    SHOULD_PRINT and print(-error)
    add_value_occurrence(-error)

    return - error


def fitness_func(ga_instance: GA, solution, solution_idx: int):
    return fit(solution)
