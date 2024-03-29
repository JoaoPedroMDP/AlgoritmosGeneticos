#  coding: utf-8
import argparse
from typing import List

from pygad import GA

from convert_data import agglomerate_bits_from_bit_line
from display_data import print_matrix

LINHAS = 3
COLUNAS = 7


def fit(bit_line: List[int], debug=False):
    rows = agglomerate_bits_from_bit_line(bit_line, 7)
    column_validity = [0] * COLUNAS
    row_validity = [0] * LINHAS
    column_sums = [0] * COLUNAS

    for i in range(LINHAS):
        row_validity[i] = 1 if sum(rows[i]) > 0 else -1
        j = 0
        while j < COLUNAS:
            column_sums[j] += rows[i][j]
            j += 1

    for i in range(COLUNAS):
        if column_sums[i] > 1:
            column_validity[i] = -column_sums[i]
        else:
            column_validity[i] = column_sums[i]

    fitness = sum(row_validity) + sum(column_validity)

    if debug:
        print(f"Validade das linhas: {row_validity}")
        print(f"Validade das colunas: {column_validity}")
        print(fitness)
        print_matrix(rows)

    return fitness


def fitness_func(ga_instance: GA, solution, solution_idx: int):
    return fit(solution)


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
        "num_genes": LINHAS*COLUNAS,
        # Tipo do gene
        "gene_type": int,
        # Espaço de busca do gene
        "gene_space": {"low": 0, "high": 2},
        # Tipo de seleção dos pais
        "parent_selection_type": "sss",
        # Elitismo (top X soluções será mantido)
        "keep_elitism": 25,
        # Tipo do crossover
        "crossover_type": "single_point",
        # Tipo da mutação
        "mutation_type": "random",
        # Porcentagem de genes que serão mutados
        "mutation_percent_genes": 4,
    }

    ga_instance = GA(**ga_config)
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    fit(solution, debug=True)
    # ga_instance.plot_fitness()


def arguments():
    parser = argparse.ArgumentParser(prog='GA de Timetable')
    parser.add_argument('--test', action='store_true', help='Testa a função de fitness com uma matriz pré definida')
    return parser.parse_args()


if __name__ == "__main__":
    args = arguments()
    if args.test:
        test_solution = [
            1, 0, 0, 1, 1, 0, 0,
            0, 1, 0, 0, 0, 1, 0,
            0, 0, 1, 0, 0, 0, 1,
        ]
        fit(test_solution, debug=True)
    else:
        main()
