#  coding: utf-8
import os

import numpy as np
from pygad import GA

from convert_data import to_matrix, get_sorted_indexes
from display_data import Matrix, print_translated_matrix
from ga_qiEinstein import COLUMNS, METADATA, ROWS, TRANSLATION_DICTS


VALUES_OCCURRENCE: dict = {}
ERROR_OCCURENCES: dict = {}
WEIGHTS: dict = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}

def reset_weights():
    global WEIGHTS
    WEIGHTS = {x: 1 for x in WEIGHTS}

def add_value_occurrence(value: int):
    if value not in VALUES_OCCURRENCE:
        VALUES_OCCURRENCE[value] = 0
    VALUES_OCCURRENCE[value] += 1


def add_error_occurrence(rule_index: int):
    ERROR_OCCURENCES[0] = ERROR_OCCURENCES.get(0, 0) + 1

    if rule_index not in ERROR_OCCURENCES:
        ERROR_OCCURENCES[rule_index] = 0
    ERROR_OCCURENCES[rule_index] += 1


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
    rule = 0

    # Posições reutilizáveis
    green_house_index = locate_house(mtrx, 'Cor', 'VERDE')
    dunhill_house_index = locate_house(mtrx, 'Cigarro', 'DUNHILL')
    blend_house_index = locate_house(mtrx, 'Cigarro', 'BLEND')

    # Regra 1: Norueguês na casa 0
    rule = 1
    norwish_house_index = locate_house(mtrx, 'Nacionalidade', 'NORUEGUES')
    l_error = WEIGHTS[rule] * (norwish_house_index - 0) 
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 2: Inglês na casa vermelha
    rule = 2
    red_house_index = locate_house(mtrx, 'Cor', 'VERMELHO')
    english_house_index = locate_house(mtrx, 'Nacionalidade', 'INGLES')
    l_error += WEIGHTS[rule] * abs(red_house_index - english_house_index)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 3: Sueco tem cachorro
    rule = 3
    dog_house_index = locate_house(mtrx, 'Animal', 'CACHORRO')
    swedish_house_index = locate_house(mtrx, 'Nacionalidade', 'SUECO')
    l_error += WEIGHTS[rule] * abs(dog_house_index - swedish_house_index)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 4: O Dinamarquês toma chá
    rule = 4
    tea_house_index = locate_house(mtrx, 'Bebida', 'CHA')
    danish_house_index = locate_house(mtrx, 'Nacionalidade', 'DINAMARQUES')
    l_error += WEIGHTS[rule] * abs(tea_house_index - danish_house_index)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 5: A casa verde está à esquerda da casa branca
    rule = 5
    white_house_index = locate_house(mtrx, 'Cor', 'BRANCO')
    l_error += WEIGHTS[rule] * abs((white_house_index - 1) - green_house_index)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 6: O dono da casa verde bebe café
    rule = 6
    coffee_house_index = locate_house(mtrx, 'Bebida', 'CAFE')
    l_error += WEIGHTS[rule] * abs(coffee_house_index - green_house_index)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 7: O homem que fuma Pall Mall tem pássaros
    rule = 7
    pallmall_house_index = locate_house(mtrx, 'Cigarro', 'PALLMALL')
    bird_house_index = locate_house(mtrx, 'Animal', 'PASSARO')
    l_error += WEIGHTS[rule] * abs(pallmall_house_index - bird_house_index)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 8: O homem que vive na casa amarela fuma Dunhill
    rule = 8
    yellow_house_index = locate_house(mtrx, 'Cor', 'AMARELO')
    l_error += WEIGHTS[rule] * abs(yellow_house_index - dunhill_house_index)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 9: O homem que vive na casa do meio bebe leite
    rule = 9
    middle_house_index = 2
    milk_house_index = locate_house(mtrx, 'Bebida', 'LEITE')
    l_error += WEIGHTS[rule] * abs(middle_house_index - milk_house_index)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 10: O homem que fuma Blends vive ao lado do que tem gatos
    rule = 10
    cat_house_index = locate_house(mtrx, 'Animal', 'GATO')
    l_error += WEIGHTS[rule] * abs(abs(blend_house_index - cat_house_index) - 1)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 11: O homem que tem cavalos vive ao lado do que fuma Dunhill
    rule = 11
    horse_house_index = locate_house(mtrx, 'Animal', 'CAVALO')
    l_error += WEIGHTS[rule] * abs(abs(horse_house_index - dunhill_house_index) - 1)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 12: O homem que fuma Blue Master bebe cerveja
    rule = 12
    bluemaster_house_index = locate_house(mtrx, 'Cigarro', 'BLUEMASTER')
    beer_house_index = locate_house(mtrx, 'Bebida', 'CERVEJA')
    l_error += WEIGHTS[rule] * abs(bluemaster_house_index - beer_house_index)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 13: O alemão fuma Prince
    rule = 13
    german_house_index = locate_house(mtrx, 'Nacionalidade', 'ALEMAO')
    prince_house_index = locate_house(mtrx, 'Cigarro', 'PRINCE')
    l_error += WEIGHTS[rule] * abs(german_house_index - prince_house_index)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 14: O Norueguês vive ao lado da casa Azul
    rule = 14
    norwegian_house_index = locate_house(mtrx, 'Nacionalidade', 'NORUEGUES')
    blue_house_index = locate_house(mtrx, 'Cor', 'AZUL')
    l_error += WEIGHTS[rule] * abs(abs(norwegian_house_index - blue_house_index) - 1)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    # Regra 15: O homem que fuma Blends vive ao lado do que bebe água
    rule = 15
    water_house_index = locate_house(mtrx, 'Bebida', 'AGUA')
    l_error += WEIGHTS[rule] * abs(abs(blend_house_index - water_house_index) - 1)
    if l_error > 0:
        add_error_occurrence(rule)
    error += l_error

    add_value_occurrence(-error)
    
    if error == 0:
        print_translated_matrix(mtrx, TRANSLATION_DICTS, COLUMNS, ROWS)
    
    return -error


def fitness_func(ga_instance: GA, solution, solution_idx: int):
    return fit(solution)
