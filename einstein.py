#  coding: utf-8
from copy import copy
import json
import os
from time import strftime, time
import numpy as np
from pygad import GA

from convert_data import get_sorted_indexes, to_matrix, translate_matrix_values
from display_data import print_matrix_as_dataframe
from ga_qiEinstein import COLUMNS, ROWS, TRANSLATION_DICTS
from ga_qiEinstein.fit_func import FIRST_ERRORS, VALUES_OCCURRENCE, fit
from ga_qiEinstein.pygad_config import FIRST_ROUND_CONFIG, SECOND_ROUND_CONFIG
from utils import sort_dict_by_keys, sort_dict_by_values

DATE_TIME_STR = strftime("%Y-%m-%d_%H-%M-%S")

def generate_report(runs_data: list):
    print("Gerando relatório")

    keys = ["num_parents_mating", "keep_elitism", "mutation_percent_genes", "mutation_type"]
    data = {
        "first_run_config": {k: FIRST_ROUND_CONFIG[k] for k in keys},
        "second_run_config": {k: SECOND_ROUND_CONFIG[k] for k in keys},
        "runs": runs_data
    }
    with open(f"reports/{DATE_TIME_STR}_report.json", "w") as f:
        json.dump(data, f, indent=4)


def main(rounds_config):
    last_elitism = None
    rounds_data = []
    gaint = None
    
    for conf in rounds_config:
        if conf:
            merged_conf = {**FIRST_ROUND_CONFIG, **conf}
        else:
            merged_conf = {**FIRST_ROUND_CONFIG}

        gaint = GA(**merged_conf)
        if last_elitism is not None:
            gaint.initialize_population(
                low=gaint.init_range_low,
                high=gaint.init_range_high,
                allow_duplicate_genes=gaint.allow_duplicate_genes,
                mutation_by_replacement=True,
                gene_type=gaint.gene_type
            )
            for i in range(conf['keep_elitism']):
                gaint.population[i] = last_elitism[i]
        
        gaint.run()
        last_elitism = gaint.last_generation_elitism 

        rounds_data.append({
            'occurrences': sort_dict_by_keys(VALUES_OCCURRENCE),
            'last_ten_first_errors': FIRST_ERRORS[-10:],
            'fitness': [int(x) for x in gaint.best_solutions_fitness]
        })

        VALUES_OCCURRENCE.clear()
        FIRST_ERRORS.clear()

    bs = gaint.best_solution()
    best_solution = bs[0]
    best_solution_fitness = bs[1]

    data = {
        "sol": best_solution,
        "sol_fit": best_solution_fitness,
        "rounds_data": rounds_data
    }

    return data, gaint

if __name__ == '__main__':
    # Crio pasta para os relatórios
    try:
        os.mkdir(f"reports")
    except FileExistsError:
        pass

    if False:
        sol = np.array([1, 2, 5, 4, 3, 9, 7, 8, 6, 10, 11, 14, 15, 12, 13, 18, 16, 19, 20, 17, 23, 22, 24, 25, 21])
        mtrx = to_matrix(sol, 5)
        mtrx = [get_sorted_indexes(row) for row in mtrx]
        translated = translate_matrix_values(mtrx, TRANSLATION_DICTS)
        print_matrix_as_dataframe(translated, columns=COLUMNS, index=ROWS)
        print(fit(sol))
        exit(1)
    
    num_of_executions = 2
    
    best_sol_avg = 0
    avg_sol_fit = 0
    min_sol_fit = 100
    max_sol_fit = -100
    avg_execution_time = 0
    runs_data = []
    # while sol_fit != 0:
    for i in range(num_of_executions):
        start_time = time()
        data, ga_int = main()
        end_time = time()
        avg_sol_fit += data['sol_fit']
        avg_execution_time = end_time - start_time
        
        runs_data.append({
            "first_run": data['first_data'],
            "second_run": data['second_data'],
        })

        if data['sol_fit'] < min_sol_fit:
            min_sol_fit = data['sol_fit']
        if data['sol_fit'] > max_sol_fit:
            max_sol_fit = data['sol_fit']

        print("Fitness: ", data['sol_fit'])
        print("Tempo: ", end_time - start_time)
        if data['sol_fit'] >= 0:
            ga_int.plot_fitness()
            best_sol_avg += 1
            print(data['sol'])
            mtrx = to_matrix(data['sol'], 5)
            mtrx = [get_sorted_indexes(row) for row in mtrx]
            translated = translate_matrix_values(mtrx, TRANSLATION_DICTS)
            print_matrix_as_dataframe(translated, columns=COLUMNS, index=ROWS)

    print("Média de fitness: ", avg_sol_fit/num_of_executions)
    print("Menor fitness: ", min_sol_fit)
    print("Maior fitness: ", max_sol_fit)
    print("Media de melhores soluções: ", best_sol_avg/num_of_executions)
    print("Tempo médio de execução: ", avg_execution_time)
    generate_report(runs_data)