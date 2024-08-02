#  coding: utf-8
import json
import os
from time import strftime, time
import numpy as np
# from pygad import GA

from convert_data import get_sorted_indexes, to_matrix, translate_matrix_values
from display_data import print_matrix_as_dataframe, print_translated_matrix
from ga_qiEinstein import COLUMNS, ROWS, TRANSLATION_DICTS
from ga_qiEinstein.fit_func import VALUES_OCCURRENCE, fit
from ga_qiEinstein.pygad_config import CONFIG
from ga_qiEinstein.custom_ga import CustomGA as GA
from utils import sort_dict_by_keys, sort_dict_by_values

DATE_TIME_STR = strftime("%Y-%m-%d_%H-%M-%S")

def should_insert(solution_fitness: any, gaint: GA):
    if max(solution_fitness) > gaint.fitness_threshold_to_insert:
        return True

    if gaint.generations_completed > gaint.num_generations * 1:
        return True

    return False

def on_fitness(gaint: GA, solution_fitness):
    size = len(gaint.population)
    if gaint.fitness_threshold_to_insert and not gaint.elite_inserted:
        if should_insert(solution_fitness, gaint):
            print("Inserindo melhores soluções da última rodada")
            best_index = np.argmin(max(solution_fitness))
            for i in range(len(gaint.elite_to_insert)):
                gaint.population[(i+best_index) % size] = gaint.elite_to_insert[i]
                solution_fitness[(i+best_index) % size] = gaint.elite_fitness_to_insert[i]

            gaint.elite_inserted = True

def generate_report(runs_data: list):
    print("Gerando relatório")

    keys = ["num_parents_mating", "keep_elitism", "mutation_percent_genes", "mutation_type"]
    data = {
        "first_run_config": {k: CONFIG[k] for k in keys},
        "second_run_config": {k: CONFIG[k] for k in keys},
        "runs": runs_data
    }
    with open(f"reports/{DATE_TIME_STR}_report.json", "w") as f:
        json.dump(data, f, indent=4)


def main(rounds_config):
    last_elitism = None
    elite_fitness_to_insert = None
    last_elitism_fitness_threshold = None
    rounds_data = []
    gaint = None

    for conf in rounds_config:
        if conf:
            merged_conf = {**CONFIG, **conf}
        else:
            merged_conf = {**CONFIG}

        progress_bar = merged_conf.pop('progress_bar')

        gaint = GA(
            **merged_conf, 
            on_fitness=on_fitness,
            on_generation=progress_bar
        )

        if last_elitism is not None:
            gaint.elite_to_insert = last_elitism
            gaint.fitness_threshold_to_insert = last_elitism_fitness_threshold
            gaint.elite_fitness_to_insert = elite_fitness_to_insert
        
        start_time = time()
        gaint.run()
        total_time = time() - start_time
        last_elitism = gaint.last_generation_elitism
        bs = gaint.best_solution()

        last_elitism_fitness_threshold = bs[1]
        elite_fitness_to_insert = list([fit(x) for x in last_elitism])

        rounds_data.append({
            'sol': bs[0],
            'sol_fit': bs[1],
            'total_time_s': total_time,
            'occurrences': sort_dict_by_keys(VALUES_OCCURRENCE),
            'fitness': [int(x) for x in gaint.best_solutions_fitness]
        })

        VALUES_OCCURRENCE.clear()


    return rounds_data, gaint

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
            print_translated_matrix(mtrx, TRANSLATION_DICTS, COLUMNS, ROWS)

    print("Média de fitness: ", avg_sol_fit/num_of_executions)
    print("Menor fitness: ", min_sol_fit)
    print("Maior fitness: ", max_sol_fit)
    print("Media de melhores soluções: ", best_sol_avg/num_of_executions)
    print("Tempo médio de execução: ", avg_execution_time)
    generate_report(runs_data)