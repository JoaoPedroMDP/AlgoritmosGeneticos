#  coding: utf-8
from pygad import GA

from display_data import trace_route_between_points
from ga_caixeiro import POINTS, POINT_COUNT
from ga_caixeiro.fit_func import fit, fitness_func


def main():
    ga_instance = GA(
        # NG: Quantas gerações serão simuladas
        num_generations=200,
        # NPM: Quantidade de soluções escolhidas para participarem do conjunto de reprodução
        num_parents_mating=5,
        # SPP: Quantas soluções terão por geração
        sol_per_pop=200,
        # KE: Elitismo (top X soluções será mantido)
        keep_elitism=30,
        # CT: Tipo do crossover
        crossover_type="single_point",
        # MT: Tipo da mutação
        mutation_type='random',
        # MP: Probabilidade de mutação
        mutation_percent_genes=10,
        num_genes=POINT_COUNT,
        gene_type=int,
        gene_space=range(POINT_COUNT),
        fitness_func=fitness_func,
        parent_selection_type="rws",
        mutation_by_replacement=True,
        allow_duplicate_genes=False,
    )
    print(f"Coordenadas: {POINT_COUNT}")
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    return solution, solution_fitness


if __name__ == '__main__':
    # teste = [ 4, 11, 2, 23, 13, 21, 12, 29, 22, 3, 8, 26, 18, 20, 14, 7, 0, 9, 1, 5, 16, 6, 27, 19, 28, 25, 24, 17, 10, 15]
    # for point in teste:
    #     print(point, POINTS[point])
    # solution_point_order = [POINTS[i] for i in teste]
    # print(solution_point_order)
    # print(fit(teste))
    # trace_route_between_points(solution_point_order)
    # exit(1)

    avg_sol_fit = 0
    min_sol_fit = 100
    max_sol_fit = -100000
    num_of_executions = 3
    i = 0
    sol_fit = 0
    best_sol = []
    # while sol_fit != 0:
    while i < num_of_executions:
        sol, sol_fit = main()
        avg_sol_fit += sol_fit
        if sol_fit < min_sol_fit:
            min_sol_fit = sol_fit
            best_sol = sol
        if sol_fit > max_sol_fit:
            max_sol_fit = sol_fit
        print("Fitness: ", sol_fit)
        solution_point_order = [POINTS[i] for i in sol]
        print(solution_point_order)
        trace_route_between_points(solution_point_order)
        i+=1

    print("Média de fitness: ", avg_sol_fit/num_of_executions)
    print("Menor fitness: ", min_sol_fit)
    print("Maior fitness: ", max_sol_fit)
    print("Melhor solução: ", best_sol)
    # solution_point_order = [POINTS[i] for i in best_sol]
    # trace_route_between_points(solution_point_order)
