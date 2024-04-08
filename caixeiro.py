#  coding: utf-8
from pygad import GA

from display_data import trace_route_between_points
from ga_caixeiro import POINTS
from ga_caixeiro.fit_func import fit
from ga_caixeiro.pygad_config import PYGAD_CONFIG


def main():
    ga_instance = GA(**PYGAD_CONFIG)
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    fit(solution, debug=True)
    solution_point_order = [POINTS[i] for i in solution]
    trace_route_between_points(solution_point_order)
    # ga_instance.plot_fitness()


if __name__ == '__main__':
    num_executions = 5
    for i in range(num_executions):
        main()
