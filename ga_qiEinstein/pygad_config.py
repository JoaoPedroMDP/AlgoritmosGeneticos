#  coding: utf-8
from ga_qiEinstein.fit_func import fitness_func

SOL_PER_POP = 20
NUM_GENES = 25

BASE_CONFIG: dict = {
    # NG: Quantas gerações serão simuladas
    "num_generations": 50,
    # Função de avaliação
    "fitness_func": fitness_func,
    # Numero de parâmetros da função
    "num_genes": NUM_GENES,
    # SPP: Quantas soluções terão por geração
    "sol_per_pop": SOL_PER_POP,
    # Tipo do gene
    "gene_type": int,
    # Espaço de busca do gene
    "gene_space": range(NUM_GENES),
    # Tipo de seleção dos pais
    # SSS significa "Steady-State Selection". Os piores cromossomos são substituídos pelos filhos gerados
    # pelo cruzamento dos melhores cromossomos
    "parent_selection_type": "sss",
    # Substituir o gene mutado pelo gene substituto, e não apenas somar um valor random
    "mutation_by_replacement": True,
    # Permitir duplicatas
    "allow_duplicate_genes": False,
    "stop_criteria": ["reach_0"],
}

FIRST_ROUND_CONFIG: dict = {
    **BASE_CONFIG,
    # NPM: Quantidade de soluções escolhidas para participarem do conjunto de reprodução
    "num_parents_mating": int(SOL_PER_POP * 0.1),
    # KE: Elitismo (top X soluções será mantido)
    "keep_elitism": int(SOL_PER_POP * 0.1),
    # CT: Tipo do crossover ('single_point', 'two_points', 'uniform', 'scattered')
    "crossover_type": "single_point",
    # MPG: Porcentagem de genes que serão mutados
    "mutation_percent_genes": 3,
    # MT: Tipo da mutação ('random', 'swap', 'inversion', 'scramble', 'adaptive')
    "mutation_type": 'random',
 }

SECOND_ROUND_CONFIG: dict = {
    **BASE_CONFIG,
    # NPM: Quantidade de soluções escolhidas para participarem do conjunto de reprodução
    "num_parents_mating": int(SOL_PER_POP * 0.75),
    # KE: Elitismo (top X soluções será mantido)
    "keep_elitism": int(SOL_PER_POP * 0.1),
    # CT: Tipo do crossover ('single_point', 'two_points', 'uniform', 'scattered')
    "crossover_type": "scattered",
    # MPG: Porcentagem de genes que serão mutados
    "mutation_percent_genes": 10,
    # MT: Tipo da mutação ('random', 'swap', 'inversion', 'scramble', 'adaptive')
    "mutation_type": 'random',
}
