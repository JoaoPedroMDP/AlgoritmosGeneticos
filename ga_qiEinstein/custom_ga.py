from pygad import GA


class CustomGA(GA):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chromossomes_to_insert = None
        self.chromossomes_fitness_to_insert = None
        # Depois que passar X% das gerações, insere os cromossomos
        self.fitness_threshold_to_insert = None
        self.chromossomes_inserted = False

