"""Module with genetic algorithm"""

import random

from deap import base
from deap import creator
from deap import tools

# CXPB  is the probability of two individuals being crossed
# MUTPB is the probability of mutating an individual
CXPB, MUTPB = 0.7, 0.1

MIN_GENE_VALUE = 0.0
MAX_GENE_VALUE = 1.0
GENES_COUNT = 42
MUTATION_PROBABILITY = 0.1

ONE_POINT_CROSS = 1
UNIFORM_CROSS = 2

GAUSSIAN_MUT = 1
BIT_MUT = 2

TOURNAMENT_SEL = 1
ROULETTE_SEL = 2
BEST_SEL = 3

SELECTION = 0.5

random.seed()

# pylint: disable=no-member
creator.create("FitnessMax", base.Fitness, weights=(1.0, -0.001))
creator.create("Individual", list, fitness=creator.FitnessMax)

TOOLBOX = base.Toolbox()
TOOLBOX.register("attr_gene", random.uniform, MIN_GENE_VALUE, MAX_GENE_VALUE)
TOOLBOX.register("individual", tools.initRepeat, creator.Individual,
                 TOOLBOX.attr_gene, GENES_COUNT)

TOOLBOX.register("population", tools.initRepeat, list, TOOLBOX.individual)
