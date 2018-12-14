"""Module with genetic algorithm"""

import random

from deap import base
from deap import creator
from deap import tools

MIN_GENE_VALUE = 0.0
MAX_GENE_VALUE = 1.0
GENES_COUNT = 42
MUTATION_PROBABILITY = 0.1

random.seed()

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

TOOLBOX = base.Toolbox()
TOOLBOX.register("attr_gene", random.uniform, MIN_GENE_VALUE, MAX_GENE_VALUE)
TOOLBOX.register("individual", tools.initRepeat, creator.Individual,
                 TOOLBOX.attr_gene, GENES_COUNT)

TOOLBOX.register("population", tools.initRepeat, list, TOOLBOX.individual)


class AlgorithmError(ValueError):
    """
    Thrown when occurs problem during algorithm execution
    """

    def __init__(self, message, errors):
        super().__init__(message, errors)


class RegistrationError(AlgorithmError):
    """
    Thrown when unexpected value is passed during registration
    """

    def __init__(self, message, errors):
        super().__init__(message, errors)
