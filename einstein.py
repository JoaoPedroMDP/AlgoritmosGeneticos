#  coding: utf-8
import json
from math import floor
from time import strftime, time
import numpy as np
from ga_qiEinstein.fit_func import VALUES_OCCURRENCE, WEIGHTS, fit
from ga_qiEinstein.pygad_config import CONFIG
from ga_qiEinstein.custom_ga import CustomGA as GA
from utils import sort_dict_by_keys

DATE_TIME_STR = strftime("%Y-%m-%d_%H-%M-%S")
WEIGHT_HISTORY = []
ERRORS_HISTORY = []

def on_fitness(gaint: GA, solution_fitness):
    size = len(gaint.population)
    if not gaint.chromossomes_inserted and \
        gaint.chromossomes_to_insert and \
        (gaint.generation_percent_to_insert * gaint.num_generations <= gaint.generations_completed):
        
        print("Inserindo cromossomos")
        best_index = np.argmin(max(solution_fitness))
        for i in range(len(gaint.chromossomes_to_insert)):
            gaint.population[(i+best_index) % size] = gaint.chromossomes_to_insert[i]
            solution_fitness[(i+best_index) % size] = gaint.chromossomes_fitness_to_insert[i]

        gaint.chromossomes_inserted = True


def build_on_generation(progress_bar):
    def on_generation(gaint: GA):
        progress_bar(gaint)
        WEIGHT_HISTORY.append(WEIGHTS.copy())

        bs = gaint.best_solution()
        errors = {x: 1 for x in range(16)}
        fit(bs[0], errors)
        total = errors.pop(0)
        ERRORS_HISTORY.append(errors)
        
        for key in list(errors.keys()):
            # WEIGHTS[key] = errors[key]
            error_percentage = errors[key]/total
            new_weight = 15 * error_percentage

            if new_weight > 1:
                WEIGHTS[key] = new_weight

    return on_generation


def main(rounds_config):    
    chromos_to_insert = None
    chromos_fit_to_insert = []
    generation_percent_to_insert = 0.5

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
            on_generation=build_on_generation(progress_bar),
        )
        gaint.generation_percent_to_insert = generation_percent_to_insert

        if chromos_to_insert:
            gaint.chromossomes_to_insert = chromos_to_insert
            gaint.chromossomes_fitness_to_insert = chromos_fit_to_insert

        start_time = time()
        gaint.run()
        total_time = time() - start_time
        bs = gaint.best_solution()
        
        data = {
            'sol': bs[0],
            'sol_fit': bs[1],
            'total_time_s': total_time,
            'occurrences': sort_dict_by_keys(VALUES_OCCURRENCE),
            'fitness': [int(x) for x in gaint.best_solutions_fitness],
        }

        fits_and_indexes = [tup for tup in zip(gaint.population, gaint.last_generation_fitness)]
        fits_and_indexes = sorted(fits_and_indexes, key=lambda x: x[1], reverse=True)

        chromos_to_insert = []
        error_occurrences = {}
        for chromossome, _ in fits_and_indexes[:5]:
            fitness = fit(chromossome, error_occurrences)
            chromos_to_insert.append(chromossome)
            chromos_fit_to_insert.append(fitness)

        rounds_data.append(data)
        VALUES_OCCURRENCE.clear()

    return {
        "rounds_data": rounds_data,
        "weight_history": WEIGHT_HISTORY,
        "error_history": ERRORS_HISTORY
    }, gaint
