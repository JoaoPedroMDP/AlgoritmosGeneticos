#  coding: utf-8
from typing import List

import numpy as np
from pygad import GA

from convert_data import agglomerate_bits_from_bit_line, translate_values
from display_data import print_matrix_as_datraframe, Matrix

# CORES
COLORS = {"AMARELO": 1, "AZUL": 2, "BRANCO": 3, "VERDE": 4, "VERMELHO": 5}
I_COLORS = {v: k for k, v in COLORS.items()}

# CIDADANIAS
NACIONALITIES = {"ALEMAO": 6, "DINAMARQUES": 7, "INGLES": 8, "NORUEGUES": 9, "SUECO": 10}
I_NACIONALITIES = {v: k for k, v in NACIONALITIES.items()}

# BEBIDAS
DRINKS = {"AGUA": 11, "CAFE": 12, "CERVEJA": 13, "CHA": 14, "LEITE": 15}
I_DRINKS = {v: k for k, v in DRINKS.items()}

# CIGARROS
CIGARS = {"BLEND": 16, "BLUEMASTER": 17, "DUNHILL": 18, "PALLMALL": 19, "PRINCE": 20}
I_CIGARS = {v: k for k, v in CIGARS.items()}

# ANIMAIS
ANIMALS = {"CACHORRO": 21, "CAVALO": 22, "GATO": 23, "PASSARO": 24, "PEIXE": 25}
I_ANIMALS = {v: k for k, v in ANIMALS.items()}

I_TRANSLATION_DICT = {**I_COLORS, **I_NACIONALITIES, **I_DRINKS, **I_CIGARS, **I_ANIMALS}

# Espaços de geração de cada gene baseado no seu tipo
# COLOR_GENE_SPACE
CGS = {"low": COLORS['AMARELO'], "high": COLORS['VERMELHO']+1}
# NACIONALITY_GENE_SPACE
NGS = {"low": NACIONALITIES['ALEMAO'], "high": NACIONALITIES['SUECO']+1}
# DRINK_GENE_SPACE
DGS = {"low": DRINKS['AGUA'], "high": DRINKS['LEITE']+1}
# CIGAR_GENE_SPACE
CiGS = {"low": CIGARS['BLEND'], "high": CIGARS['PRINCE']+1}
# PET_GENE_SPACE
PGS = {"low": ANIMALS['CACHORRO'], "high": ANIMALS['PEIXE']+1}

# Espaços finais de criação dos genes
COLOR_SPACE = [CGS, CGS, CGS, CGS, CGS]
NACIONALITY_SPACE = [NGS, NGS, NGS, NGS, NGS]
DRINK_SPACE = [DGS, DGS, DGS, DGS, DGS]
CIGAR_SPACE = [CiGS, CiGS, CiGS, CiGS, CiGS]
PET_SPACE = [PGS, PGS, PGS, PGS, PGS]

COLUMNS = ["Casa 0", "Casa 1", "Casa 2", "Casa 3", "Casa 4"]
ROWS = ["Cor", "Nacionalidade", "Bebida", "Cigarro", "Animal"]
CHROMOSSOME_SEGMENT_COUNT = len(ROWS)

METADATA = {
    "Cor": {
        "row_index": 0,
        "data_dictionary": COLORS
    },
    "Nacionalidade": {
        "row_index": 1,
        "data_dictionary": NACIONALITIES
    },
    "Bebida": {
        "row_index": 2,
        "data_dictionary": DRINKS
    },
    "Cigarro": {
        "row_index": 3,
        "data_dictionary": CIGARS
    },
    "Animal": {
        "row_index": 4,
        "data_dictionary": ANIMALS
    }
}


def locate_house(matrix: Matrix, row: str, item: str):
    return np.where(matrix[METADATA[row]['row_index']] == METADATA[row]['data_dictionary'][item])[0][0]


def fit(bitline: List[int], debug = False):
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


def crossover_func(parents: np.ndarray, offspring_size: tuple, ga_instance: GA):
    """
    Função de crossover. NÃO ESTOU USANDO
    :param parents:
    :param offspring_size:
    :param ga_instance:
    :return:
    """
    offspring = []
    offspring_child_count = offspring_size[0]

    while len(offspring) < offspring_child_count:
        random_int = np.random.randint(0, len(parents))
        parent1 = parents[random_int].copy()
        parent2 = parents[(random_int + 1) % len(parents)].copy()

        # Crossover baseado no tamanho de cada seção do cromossomo
        # 1. Seleciono um dos 5 temas para trocar entre os dois pais
        # 2. Troco as seções correspondentes entre os pais

        theme = np.random.randint(0, CHROMOSSOME_SEGMENT_COUNT)
        cross_start = theme*CHROMOSSOME_SEGMENT_COUNT - CHROMOSSOME_SEGMENT_COUNT
        cross_end = theme*CHROMOSSOME_SEGMENT_COUNT

        tmp = parent1[cross_start:cross_end].copy()
        parent1[cross_start:cross_end] = parent2[cross_start:cross_end]
        parent2[cross_start:cross_end] = tmp

        offspring.append(parent1)
        offspring.append(parent2)

    return np.array(offspring)


def main():
    ga_config: dict = {
        # Função de avaliação
        "fitness_func": fitness_func,
        # Quantas gerações serão simuladas
        "num_generations": 100,
        # Quantidade de soluções escolhidas para participarem do conjunto de reprodução
        "num_parents_mating": 10,
        # Quantas soluções terão por geração
        "sol_per_pop": 100,
        # Numero de parâmetros da função
        "num_genes": 25,
        # Tipo do gene
        "gene_type": int,
        # Espaço de busca do gene
        "gene_space": [*COLOR_SPACE, *NACIONALITY_SPACE, *DRINK_SPACE, *CIGAR_SPACE, *PET_SPACE],

        # Tipo de seleção dos pais
        # SSS significa "Steady-State Selection". Os piores cromossomos são substituídos pelos filhos gerados
        # pelo cruzamento dos melhores cromossomos
        "parent_selection_type": "sss",

        # Elitismo (top X soluções será mantido)
        "keep_elitism": 20,
        # Tipo do crossover
        "crossover_type": "scattered",
        # Tipo da mutação
        "mutation_type": 'random',
        # Substituir o gene mutado pelo gene substituto, e não apenas somar um valor random
        "mutation_by_replacement": True,
        # Porcentagem de genes que serão mutados
        "mutation_percent_genes": 10,
        # Permitir duplicatas
        "allow_duplicate_genes": False,
        # Isto otimiza o programa. Se o fitness não mudar por X gerações, o programa para.
        "stop_criteria": "saturate_10",
    }

    ga_instance = GA(**ga_config)
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    return solution, solution_fitness, ga_instance


if __name__ == '__main__':
    avg_sol_fit = 0
    min_sol_fit = 100
    max_sol_fit = -100
    num_of_executions = 10

    for i in range(num_of_executions):
        sol, sol_fit, ga_int = main()
        avg_sol_fit += sol_fit
        if sol_fit < min_sol_fit:
            min_sol_fit = sol_fit
        if sol_fit > max_sol_fit:
            max_sol_fit = sol_fit
        # ga_int.plot_fitness()
        print("Fitness: ", sol_fit)

        if sol_fit == 0:
            translated = agglomerate_bits_from_bit_line(
                translate_values(sol, I_TRANSLATION_DICT),
                5
            )
            print_matrix_as_datraframe(translated, columns=COLUMNS, index=ROWS)

    print("Média de fitness: ", avg_sol_fit/num_of_executions)
    print("Menor fitness: ", min_sol_fit)
    print("Maior fitness: ", max_sol_fit)
