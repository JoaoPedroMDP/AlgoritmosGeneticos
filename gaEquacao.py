#  coding: utf-8
from numpy import ndarray
from pygad import GA


def fitness_func(ga_instance: GA, solution: ndarray, solution_idx: int):
    return - (solution[0] + solution[1] - abs(solution[0] - solution[1]))


ga_config: dict = {
    # Função de avaliação
    "fitness_func": fitness_func,
    # Quantas gerações serão simuladas
    "num_generations": 100,
    # Quantidade de soluções escolhidas para participarem do conjunto de reprodução
    "num_parents_mating": 4,
    # Quantas soluções terão por geração
    "sol_per_pop": 50,
    # Numero de parâmetros da função
    "num_genes": 2,
    # Tipo do gene
    "gene_type": int,
    # Tipo de seleção dos pais
    "parent_selection_type": "sss",
    # Elitismo (top X soluções será mantido)
    "keep_elitism": 5,
    # Tipo do crossover
    "crossover_type": "single_point",
    # Tipo da mutação
    "mutation_type": "random",
    # Porcentagem de genes que serão mutados
    "mutation_percent_genes": 10
}


def main():
    ga_instance = GA(**ga_config)
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print(solution, solution_fitness, solution_idx)


if __name__ == "__main__":
    main()
