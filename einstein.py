#  coding: utf-8
import numpy as np
from pygad import GA

from convert_data import agglomerate_bits_from_bit_line, translate_values
from display_data import print_matrix_as_dataframe
from ga_qiEinstein import I_TRANSLATION_DICT, COLUMNS, ROWS
from ga_qiEinstein.fit_func import fit
from ga_qiEinstein.pygad_config import PYGAD_CONFIG


def main():
    ga_instance = GA(**PYGAD_CONFIG)
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    return solution, solution_fitness, ga_instance


if __name__ == '__main__':
    if False:
        sol = np.array([1, 2, 5, 4, 3, 9, 7, 8, 6, 10, 11, 14, 15, 12, 13, 18, 16, 19, 20, 17, 23, 22, 24, 25, 21])
        print(fit(sol))
        exit(1)

    avg_sol_fit = 0
    min_sol_fit = 100
    max_sol_fit = -100
    num_of_executions = 5
    sol_fit = -10
    # while sol_fit != 0:
    for i in range(num_of_executions):
        sol, sol_fit, ga_int = main()
        avg_sol_fit += sol_fit
        if sol_fit < min_sol_fit:
            min_sol_fit = sol_fit
        if sol_fit > max_sol_fit:
            max_sol_fit = sol_fit
        ga_int.plot_fitness()
        print("Fitness: ", sol_fit)
        print(sol)
        translated = agglomerate_bits_from_bit_line(
            translate_values(sol, I_TRANSLATION_DICT),
            5
        )
        print_matrix_as_dataframe(translated, columns=COLUMNS, index=ROWS)

    print("Média de fitness: ", avg_sol_fit/num_of_executions)
    print("Menor fitness: ", min_sol_fit)
    print("Maior fitness: ", max_sol_fit)
