#  coding: utf-8
import os

import numpy as np
from pygad import GA

from convert_data import to_matrix, get_sorted_indexes
from display_data import Matrix, print_translated_matrix
from ga_qiEinstein import COLUMNS, METADATA, ROWS, TRANSLATION_DICTS


SHOULD_PRINT = False
ABSOLUTE_ERROR_WEIGHT = 100
VALUES_OCCURRENCE: dict = {}
WEIGHTS= [
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
]

def add_value_occurrence(value: int):
    processed = value

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

def fit(bitline: np.ndarray):
    mtrx = to_matrix(bitline, 5)
    mtrx = [get_sorted_indexes(row) for row in mtrx]
    
    error = 0
    
    # Posições reutilizáveis
    green_house_index = locate_house(mtrx, 'Cor', 'VERDE')
    dunhill_house_index = locate_house(mtrx, 'Cigarro', 'DUNHILL')
    blend_house_index = locate_house(mtrx, 'Cigarro', 'BLEND')

    # Regra 1: Norueguês na casa 0
    norwish_house_index = locate_house(mtrx, 'Nacionalidade', 'NORUEGUES')
    error = 1.9 * (norwish_house_index - 0) 

    # Regra 2: Inglês na casa vermelha
    red_house_index = locate_house(mtrx, 'Cor', 'VERMELHO')
    english_house_index = locate_house(mtrx, 'Nacionalidade', 'INGLES')
    error += 1.6 * abs(red_house_index - english_house_index)

    # Regra 3: Sueco tem cachorro
    dog_house_index = locate_house(mtrx, 'Animal', 'CACHORRO')
    swedish_house_index = locate_house(mtrx, 'Nacionalidade', 'SUECO')
    error += 1.4 * abs(dog_house_index - swedish_house_index)

    # Regra 4: O Dinamarquês toma chá
    tea_house_index = locate_house(mtrx, 'Bebida', 'CHA')
    danish_house_index = locate_house(mtrx, 'Nacionalidade', 'DINAMARQUES')
    error += 1.5 * abs(tea_house_index - danish_house_index)

    # Regra 5: A casa verde está à esquerda da casa branca
    white_house_index = locate_house(mtrx, 'Cor', 'BRANCO')
    error += 1.7 * abs((white_house_index - 1) - green_house_index)

    # Regra 6: O dono da casa verde bebe café
    coffee_house_index = locate_house(mtrx, 'Bebida', 'CAFE')
    error += 1.7 * abs(coffee_house_index - green_house_index)

    # Regra 7: O homem que fuma Pall Mall tem pássaros
    pallmall_house_index = locate_house(mtrx, 'Cigarro', 'PALLMALL')
    bird_house_index = locate_house(mtrx, 'Animal', 'PASSARO')
    error += 1.2 * abs(pallmall_house_index - bird_house_index)

    # Regra 8: O homem que vive na casa amarela fuma Dunhill
    yellow_house_index = locate_house(mtrx, 'Cor', 'AMARELO')
    error += 1.6 * abs(yellow_house_index - dunhill_house_index)

    # Regra 9: O homem que vive na casa do meio bebe leite
    middle_house_index = 2
    milk_house_index = locate_house(mtrx, 'Bebida', 'LEITE')
    error += 1.9 * abs(middle_house_index - milk_house_index)

    # Regra 10: O homem que fuma Blends vive ao lado do que tem gatos
    cat_house_index = locate_house(mtrx, 'Animal', 'GATO')
    error += abs(abs(blend_house_index - cat_house_index) - 1)

    # Regra 11: O homem que tem cavalos vive ao lado do que fuma Dunhill
    horse_house_index = locate_house(mtrx, 'Animal', 'CAVALO')
    error += abs(abs(horse_house_index - dunhill_house_index) - 1)

    # Regra 12: O homem que fuma Blue Master bebe cerveja
    bluemaster_house_index = locate_house(mtrx, 'Cigarro', 'BLUEMASTER')
    beer_house_index = locate_house(mtrx, 'Bebida', 'CERVEJA')
    error += 1.3 * abs(bluemaster_house_index - beer_house_index)

    # Regra 13: O alemão fuma Prince
    german_house_index = locate_house(mtrx, 'Nacionalidade', 'ALEMAO')
    prince_house_index = locate_house(mtrx, 'Cigarro', 'PRINCE')
    error += 1.4 * abs(german_house_index - prince_house_index)

    # Regra 14: O Norueguês vive ao lado da casa Azul
    norwegian_house_index = locate_house(mtrx, 'Nacionalidade', 'NORUEGUES')
    blue_house_index = locate_house(mtrx, 'Cor', 'AZUL')
    error += 1.8 * abs(abs(norwegian_house_index - blue_house_index) - 1)

    # Regra 15: O homem que fuma Blends vive ao lado do que bebe água
    water_house_index = locate_house(mtrx, 'Bebida', 'AGUA')
    error += 1.2 * abs(abs(blend_house_index - water_house_index) - 1)

    SHOULD_PRINT and print(-error)
    add_value_occurrence(-error)
    
    if error == 0:
        print_translated_matrix(mtrx, TRANSLATION_DICTS, COLUMNS, ROWS)
    
    return -error


def fitness_func(ga_instance: GA, solution, solution_idx: int):
    return fit(solution)
