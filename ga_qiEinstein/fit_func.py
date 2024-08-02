#  coding: utf-8
import os

import numpy as np
from pygad import GA

from convert_data import to_matrix, get_sorted_indexes
from display_data import Matrix, print_translated_matrix
from ga_qiEinstein import COLUMNS, METADATA, ROWS, TRANSLATION_DICTS


SHOULD_PRINT = False
ERROR_WEIGHT = 1
ABSOLUTE_ERROR_WEIGHT = 100
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

def fit(bitline: np.ndarray):
    mtrx = to_matrix(bitline, 5)
    mtrx = [get_sorted_indexes(row) for row in mtrx]
    
    error = 0
    rules_broken = 0
    rules_broken_step_increase = 0
    
    # Posições reutilizáveis
    green_house_index = locate_house(mtrx, 'Cor', 'VERDE')
    dunhill_house_index = locate_house(mtrx, 'Cigarro', 'DUNHILL')
    blend_house_index = locate_house(mtrx, 'Cigarro', 'BLEND')

    # Regra 1: Norueguês na casa 0
    norwish_house_index = locate_house(mtrx, 'Nacionalidade', 'NORUEGUES')
    l_error = ABSOLUTE_ERROR_WEIGHT * (norwish_house_index - 0) 
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 2: Inglês na casa vermelha
    red_house_index = locate_house(mtrx, 'Cor', 'VERMELHO')
    english_house_index = locate_house(mtrx, 'Nacionalidade', 'INGLES')
    l_error += ERROR_WEIGHT * abs(red_house_index - english_house_index)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 3: Sueco tem cachorro
    dog_house_index = locate_house(mtrx, 'Animal', 'CACHORRO')
    swedish_house_index = locate_house(mtrx, 'Nacionalidade', 'SUECO')
    l_error += ERROR_WEIGHT * abs(dog_house_index - swedish_house_index)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 4: O Dinamarquês toma chá
    tea_house_index = locate_house(mtrx, 'Bebida', 'CHA')
    danish_house_index = locate_house(mtrx, 'Nacionalidade', 'DINAMARQUES')
    l_error += ERROR_WEIGHT * abs(tea_house_index - danish_house_index)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 5: A casa verde está à esquerda da casa branca
    white_house_index = locate_house(mtrx, 'Cor', 'BRANCO')
    l_error += abs((white_house_index - 1) - green_house_index)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 6: O dono da casa verde bebe café
    coffee_house_index = locate_house(mtrx, 'Bebida', 'CAFE')
    l_error += ERROR_WEIGHT * abs(coffee_house_index - green_house_index)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 7: O homem que fuma Pall Mall tem pássaros
    pallmall_house_index = locate_house(mtrx, 'Cigarro', 'PALLMALL')
    bird_house_index = locate_house(mtrx, 'Animal', 'PASSARO')
    l_error += ERROR_WEIGHT * abs(pallmall_house_index - bird_house_index)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 8: O homem que vive na casa amarela fuma Dunhill
    yellow_house_index = locate_house(mtrx, 'Cor', 'AMARELO')
    l_error += ERROR_WEIGHT * abs(yellow_house_index - dunhill_house_index)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 9: O homem que vive na casa do meio bebe leite
    middle_house_index = 2
    milk_house_index = locate_house(mtrx, 'Bebida', 'LEITE')
    l_error += ABSOLUTE_ERROR_WEIGHT * abs(middle_house_index - milk_house_index)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 10: O homem que fuma Blends vive ao lado do que tem gatos
    cat_house_index = locate_house(mtrx, 'Animal', 'GATO')
    l_error += abs(abs(blend_house_index - cat_house_index) - 1)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 11: O homem que tem cavalos vive ao lado do que fuma Dunhill
    horse_house_index = locate_house(mtrx, 'Animal', 'CAVALO')
    l_error += abs(abs(horse_house_index - dunhill_house_index) - 1)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 12: O homem que fuma Blue Master bebe cerveja
    bluemaster_house_index = locate_house(mtrx, 'Cigarro', 'BLUEMASTER')
    beer_house_index = locate_house(mtrx, 'Bebida', 'CERVEJA')
    l_error += ERROR_WEIGHT * abs(bluemaster_house_index - beer_house_index)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 13: O alemão fuma Prince
    german_house_index = locate_house(mtrx, 'Nacionalidade', 'ALEMAO')
    prince_house_index = locate_house(mtrx, 'Cigarro', 'PRINCE')
    l_error += ERROR_WEIGHT * abs(german_house_index - prince_house_index)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 14: O Norueguês vive ao lado da casa Azul
    norwegian_house_index = locate_house(mtrx, 'Nacionalidade', 'NORUEGUES')
    blue_house_index = locate_house(mtrx, 'Cor', 'AZUL')
    l_error += abs(abs(norwegian_house_index - blue_house_index) - 1)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    # Regra 15: O homem que fuma Blends vive ao lado do que bebe água
    water_house_index = locate_house(mtrx, 'Bebida', 'AGUA')
    l_error += abs(abs(blend_house_index - water_house_index) - 1)
    if l_error > 0:
        rules_broken += 1 if rules_broken == 0 else rules_broken_step_increase
        l_error += rules_broken
    error += l_error

    SHOULD_PRINT and print(-error)
    add_value_occurrence(-error)
    
    if error == 0:
        print_translated_matrix(mtrx, TRANSLATION_DICTS, COLUMNS, ROWS)
    
    return -error


def fitness_func(ga_instance: GA, solution, solution_idx: int):
    return fit(solution)
