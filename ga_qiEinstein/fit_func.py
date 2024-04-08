#  coding: utf-8
from math import factorial
from typing import List

import numpy as np
from pygad import GA

from convert_data import agglomerate_bits_from_bit_line
from display_data import Matrix
from ga_qiEinstein import METADATA


def locate_house(matrix: Matrix, row: str, item: str):
    return np.where(matrix[METADATA[row]['row_index']] == METADATA[row]['data_dictionary'][item])[0][0]


def fit(bitline: np.ndarray, debug=False):
    mtrx = agglomerate_bits_from_bit_line(bitline, 5)
    error = 0

    # Posições reutilizáveis
    green_house_index = locate_house(mtrx, 'Cor', 'VERDE')
    dunhill_house_index = locate_house(mtrx, 'Cigarro', 'DUNHILL')
    blend_house_index = locate_house(mtrx, 'Cigarro', 'BLEND')

    # Regra 1: Norueguês na casa 0
    norwish_house_index = locate_house(mtrx, 'Nacionalidade', 'NORUEGUES')
    error += norwish_house_index - 0

    # Regra 2: Inglês na casa vermelha
    red_house_index = locate_house(mtrx, 'Cor', 'VERMELHO')
    english_house_index = locate_house(mtrx, 'Nacionalidade', 'INGLES')
    error += abs(red_house_index - english_house_index)

    # Regra 3: Sueco tem cachorro
    dog_house_index = locate_house(mtrx, 'Animal', 'CACHORRO')
    swedish_house_index = locate_house(mtrx, 'Nacionalidade', 'SUECO')
    error += abs(dog_house_index - swedish_house_index)

    # Regra 4: O Dinamarquês toma chá
    tea_house_index = locate_house(mtrx, 'Bebida', 'CHA')
    danish_house_index = locate_house(mtrx, 'Nacionalidade', 'DINAMARQUES')
    error += abs(tea_house_index - danish_house_index)

    # Regra 5: A casa verde está à esquerda da casa branca
    white_house_index = locate_house(mtrx, 'Cor', 'BRANCO')
    error += abs(white_house_index - green_house_index - 1)

    # Regra 6: O dono da casa verde bebe café
    coffee_house_index = locate_house(mtrx, 'Bebida', 'CAFE')
    error += abs(coffee_house_index - green_house_index)

    # Regra 7: O homem que fuma Pall Mall tem pássaros
    pallmall_house_index = locate_house(mtrx, 'Cigarro', 'PALLMALL')
    bird_house_index = locate_house(mtrx, 'Animal', 'PASSARO')
    error += abs(pallmall_house_index - bird_house_index)

    # Regra 8: O homem que vive na casa amarela fuma Dunhill
    yellow_house_index = locate_house(mtrx, 'Cor', 'AMARELO')
    error += abs(yellow_house_index - dunhill_house_index)

    # Regra 9: O homem que vive na casa do meio bebe leite
    middle_house_index = 2
    milk_house_index = locate_house(mtrx, 'Bebida', 'LEITE')
    error += abs(middle_house_index - milk_house_index)

    # Regra 10: O homem que fuma Blends vive ao lado do que tem gatos
    cat_house_index = locate_house(mtrx, 'Animal', 'GATO')
    error += abs(abs(blend_house_index - cat_house_index) - 1)

    # Regra 11: O homem que tem cavalos vive ao lado do que fuma Dunhill
    horse_house_index = locate_house(mtrx, 'Animal', 'CAVALO')
    error += abs(abs(horse_house_index - dunhill_house_index) - 1)

    # Regra 12: O homem que fuma Blue Master bebe cerveja
    bluemaster_house_index = locate_house(mtrx, 'Cigarro', 'BLUEMASTER')
    beer_house_index = locate_house(mtrx, 'Bebida', 'CERVEJA')
    error += abs(bluemaster_house_index - beer_house_index)

    # Regra 13: O alemão fuma Prince
    german_house_index = locate_house(mtrx, 'Nacionalidade', 'ALEMAO')
    prince_house_index = locate_house(mtrx, 'Cigarro', 'PRINCE')
    error += abs(german_house_index - prince_house_index)

    # Regra 14: O Norueguês vive ao lado da casa Azul
    norwegian_house_index = locate_house(mtrx, 'Nacionalidade', 'NORUEGUES')
    blue_house_index = locate_house(mtrx, 'Cor', 'AZUL')
    error += abs(abs(norwegian_house_index - blue_house_index) - 1)

    # Regra 15: O homem que fuma Blends vive ao lado do que bebe água
    water_house_index = locate_house(mtrx, 'Bebida', 'AGUA')
    error += abs(abs(blend_house_index - water_house_index) - 1)

    return - error


def fitness_func(ga_instance: GA, solution, solution_idx: int):
    return fit(solution)
