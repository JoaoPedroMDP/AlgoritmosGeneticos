#  coding: utf-8
import numpy as np

from ga_qiEinstein.pygad_config import CHROMOSSOME_SEGMENT_COUNT


# Funciona, mas não teve impacto positivo no resultado final.
# O propósito dessa função era evitar que o cruzamente entre dois pais não misturasse
# as seções de cada cromossomo, mas sim trocasse as seções inteiras.
def crossover_func(parents: np.ndarray, offspring_size: tuple, ga_instance: GA):
    """
    Função de crossover.
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
