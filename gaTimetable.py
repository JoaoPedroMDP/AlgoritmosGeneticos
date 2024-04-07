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
    row_sums = [0] * LINHAS

    for i in range(LINHAS):
        row_sums[i] = sum(rows[i])
        j = 0
        while j < COLUNAS:
            column_sums[j] += rows[i][j]
            j += 1

    for i in range(COLUNAS):
        column_validity[i] = 1 - abs(1 - column_sums[i])

    for i in range(LINHAS):
        # Essa conta doida aí serve pra calcular o quão diferente a soma de uma linha é da soma das outras linhas
        # Meu objetivo com ela é distrbuir os números '1' da maneira mais uniforme possível

        # 'diff_from_row_sum_average': Diferença do valor da linhas atual para a média das somas das linhas
        diff_from_row_sum_average = abs(sum(row_sums)/LINHAS - row_sums[i])

        # Ali no final eu divido por 'row_sums[i]' pra normalizar o valor, e não adicionar um peso muito grande para a soma das linhas
        # Se não faço essa divisão, o GA acha que quanto maior a soma da linha, melhor, mesmo que a soma das colunas fique maior que 1
        row_validity[i] = (row_sums[i] - diff_from_row_sum_average) / row_sums[i]

    fitness = sum(row_validity) + sum(column_validity)

    if debug:
        print(f"Validade das linhas: {row_validity}")
        print(f"Validade das colunas: {column_validity}")
        print(f"Soma das colunas: {column_sums}")
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
        # SSS significa "Steady-State Selection". Os piores cromossomos são substituídos pelos filhos gerados
        # pelo cruzamento dos melhores cromossomos
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
