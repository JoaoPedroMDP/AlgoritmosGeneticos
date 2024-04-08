#  coding: utf-8
from ga_caixeiro import POINT_COUNT
from ga_caixeiro.fit_func import fitness_func

PYGAD_CONFIG: dict = {
    # Função de avaliação
    "fitness_func": fitness_func,
    # Quantas gerações serão simuladas
    "num_generations": 100,
    # Quantidade de soluções escolhidas para participarem do conjunto de reprodução
    "num_parents_mating": 5,
    # Quantas soluções terão por geração
    "sol_per_pop": 200,
    # Numero de parâmetros da função
    "num_genes": POINT_COUNT,
    # Tipo do gene
    "gene_type": int,
    # Espaço de busca do gene
    "gene_space": range(POINT_COUNT),

    # Tipo de seleção dos pais
    # SSS significa "Steady-State Selection". Os piores cromossomos são substituídos pelos filhos gerados
    # pelo cruzamento dos melhores cromossomos
    "parent_selection_type": "sss",

    # Elitismo (top X soluções será mantido)
    "keep_elitism": 5,
    # Tipo do crossover
    "crossover_type": "single_point",
    # Tipo da mutação
    "mutation_type": 'random',
    # Porcentagem de genes que serão mutados
    "mutation_percent_genes": 5,
    # Permitir duplicatas
    "allow_duplicate_genes": False,
    # Isto otimiza o programa. Se o fitness não mudar por X gerações, o programa para.
    "stop_criteria": "saturate_10",
}
