#  coding: utf-8


# CORES
COLORS = {"AMARELO": 1, "AZUL": 2, "BRANCO": 3, "VERDE": 4, "VERMELHO": 5}
I_COLORS = {v: k for k, v in COLORS.items()}

# CIDADANIAS
NACIONALITIES = {"ALEMAO": 1, "DINAMARQUES": 2, "INGLES": 3, "NORUEGUES": 4, "SUECO": 5}
I_NACIONALITIES = {v: k for k, v in NACIONALITIES.items()}

# BEBIDAS
DRINKS = {"AGUA": 1, "CAFE": 2, "CERVEJA": 3, "CHA": 4, "LEITE": 5}
I_DRINKS = {v: k for k, v in DRINKS.items()}

# CIGARROS
CIGARS = {"BLEND": 1, "BLUEMASTER": 2, "DUNHILL": 3, "PALLMALL": 4, "PRINCE": 5}
I_CIGARS = {v: k for k, v in CIGARS.items()}

# ANIMAIS
ANIMALS = {"CACHORRO": 1, "CAVALO": 2, "GATO": 3, "PASSARO": 4, "PEIXE": 5}
I_ANIMALS = {v: k for k, v in ANIMALS.items()}

TRANSLATION_DICTS = [I_COLORS, I_NACIONALITIES, I_DRINKS, I_CIGARS, I_ANIMALS]

# Espaços de geração de cada gene baseado no seu tipo
# COLOR_GENE_SPACE
CGS = {"low": COLORS['AMARELO'], "high": COLORS['VERMELHO']+1}
# NACIONALITY_GENE_SPACE
NGS = {"low": NACIONALITIES['ALEMAO'], "high": NACIONALITIES['SUECO']+1}
# DRINK_GENE_SPACE
DGS = {"low": DRINKS['AGUA'], "high": DRINKS['LEITE']+1}
# CIGAR_GENE_SPACE
CiGS = {"low": CIGARS['BLEND'], "high": CIGARS['PRINCE']+1}
# PET_GENE_SPACE
PGS = {"low": ANIMALS['CACHORRO'], "high": ANIMALS['PEIXE']+1}

COLUMNS = ["Casa 0", "Casa 1", "Casa 2", "Casa 3", "Casa 4"]
ROWS = ["Cor", "Nacionalidade", "Bebida", "Cigarro", "Animal"]
CHROMOSSOME_SEGMENT_COUNT = len(ROWS)

METADATA = {
    "Cor": {
        "row_index": 0,
        "data_dictionary": COLORS
    },
    "Nacionalidade": {
        "row_index": 1,
        "data_dictionary": NACIONALITIES
    },
    "Bebida": {
        "row_index": 2,
        "data_dictionary": DRINKS
    },
    "Cigarro": {
        "row_index": 3,
        "data_dictionary": CIGARS
    },
    "Animal": {
        "row_index": 4,
        "data_dictionary": ANIMALS
    }
}
