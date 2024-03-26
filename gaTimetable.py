#  coding: utf-8
from typing import List

from pygad import GA

from convert_data import agglomerate_bits_from_bit_line
from display_data import print_matrix


def fit(bit_line: List[int], debug=False):
    rows = agglomerate_bits_from_bit_line(bit_line, 7)
    column_validity = [0] * len(rows[0])
    row_validity = [0] * len(rows)
    column_sums = [0] * len(rows[0])

    for i in range(len(rows)):
        row_validity[i] = 1 if sum(rows[i]) > 0 else -1
        j = 0
        while j < len(rows[i]):
            column_sums[j] += rows[i][j]
            j += 1

    for i in range(len(column_validity)):
        if column_sums[i] == 0:
            column_validity[i] = +10
        elif column_sums[i] == 1:
            column_validity[i] = 0
        elif column_sums[i] > 1:
            column_validity[i] = column_sums[i]

    not debug or print_matrix(rows)
    not debug or print(row_validity, column_validity)
    not debug or print(sum(row_validity) - abs(sum(column_validity)))

    return sum(row_validity) - sum(column_validity)


def fitness_func(ga_instance: GA, solution, solution_idx: int):
    return fit(solution)


def main():
    ga_config: dict = {
        # Função de avaliação
        "fitness_func": fitness_func,
        # Quantas gerações serão simuladas
        "num_generations": 200,
        # Quantidade de soluções escolhidas para participarem do conjunto de reprodução
        "num_parents_mating": 10,
        # Quantas soluções terão por geração
        "sol_per_pop": 100,
        # Numero de parâmetros da função
        "num_genes": 28,
        # Tipo do gene
        "gene_type": int,
        # Espaço de busca do gene
        "gene_space": {"low": 0, "high": 2},
        # Tipo de seleção dos pais
        "parent_selection_type": "sss",
        # Elitismo (top X soluções será mantido)
        "keep_elitism": 3,
        # Tipo do crossover
        "crossover_type": "single_point",
        # Tipo da mutação
        "mutation_type": "random",
        # Porcentagem de genes que serão mutados
        "mutation_percent_genes": 25,
    }

    ga_instance = GA(**ga_config)
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    # test_solution = [
    #     1, 0, 0, 0, 1, 0, 0,
    #     0, 1, 0, 0, 0, 1, 0,
    #     0, 0, 1, 0, 0, 0, 1,
    #     0, 0, 0, 1, 0, 0, 0,
    # ]
    fit(solution, True)


if __name__ == "__main__":
    main()
