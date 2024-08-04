#  coding: utf-8
import json
import os
from time import strftime, time
import numpy as np

from convert_data import get_sorted_indexes, to_matrix, translate_matrix_values
from display_data import print_matrix_as_dataframe, print_translated_matrix
from ga_qiEinstein import COLUMNS, ROWS, TRANSLATION_DICTS
from ga_qiEinstein.fit_func import ERROR_OCCURENCES, VALUES_OCCURRENCE, WEIGHTS, fit, reset_weights
from ga_qiEinstein.pygad_config import CONFIG
from ga_qiEinstein.custom_ga import CustomGA as GA
from utils import sort_dict_by_keys

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
    
    # Vou resetar os pesos
    for key in WEIGHTS:
        WEIGHTS[key] = 1

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
            'fitness': [int(x) for x in gaint.best_solutions_fitness],
            "error_weights": WEIGHTS
        })

        for key in list(ERROR_OCCURENCES.keys())[1:]:
            error_percentage = ERROR_OCCURENCES[key]/ERROR_OCCURENCES[0]
            new_weight = 15 * (error_percentage)
            WEIGHTS[key] = new_weight

        print(WEIGHTS)
        ERROR_OCCURENCES.clear()
        VALUES_OCCURRENCE.clear()


    return rounds_data, gaint
