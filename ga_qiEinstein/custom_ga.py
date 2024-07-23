from pygad import GA


class CustomGA(GA):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.elite_to_insert = None
        self.elite_fitness_to_insert = None
        self.fitness_threshold_to_insert = None
        self.elite_inserted = False

