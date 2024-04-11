#  coding: utf-8
from ga_qiEinstein import COLOR_SPACE, NACIONALITY_SPACE, DRINK_SPACE, CIGAR_SPACE, PET_SPACE
from ga_qiEinstein.fit_func import fitness_func

PYGAD_CONFIG: dict = {
    # NG: Quantas gerações serão simuladas
    "num_generations": 100,
    # NPM: Quantidade de soluções escolhidas para participarem do conjunto de reprodução
    "num_parents_mating": 10,
    # SPP: Quantas soluções terão por geração
    "sol_per_pop": 200,
    # KE: Elitismo (top X soluções será mantido)
    "keep_elitism": 20,
    # CT: Tipo do crossover
    "crossover_type": "scattered",
    # MT: Tipo da mutação
    "mutation_type": 'random',
    # MPG: Porcentagem de genes que serão mutados
    "mutation_percent_genes": 2,

    # Função de avaliação
    "fitness_func": fitness_func,
    # Numero de parâmetros da função
    "num_genes": 25,
    # Tipo do gene
    "gene_type": int,
    # Espaço de busca do gene
    "gene_space": [*COLOR_SPACE, *NACIONALITY_SPACE, *DRINK_SPACE, *CIGAR_SPACE, *PET_SPACE],
    # Tipo de seleção dos pais
    # SSS significa "Steady-State Selection". Os piores cromossomos são substituídos pelos filhos gerados
    # pelo cruzamento dos melhores cromossomos
    "parent_selection_type": "sss",
    # Substituir o gene mutado pelo gene substituto, e não apenas somar um valor random
    "mutation_by_replacement": True,
    # Permitir duplicatas
    "allow_duplicate_genes": False,
    # Isto otimiza o programa. Se o fitness não mudar por X gerações, o programa para.
    "stop_criteria": "saturate_10",
}
