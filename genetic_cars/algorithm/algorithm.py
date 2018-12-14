"""Genetic algorithm implementation"""

import random

from deap import tools

from . import TOOLBOX, MUTATION_PROBABILITY


def eval_best_car(individual, route):
    """
    Perform given individual
    :param individual: car genotype
    :param route: selected route
    :return: performance of an individual
    """
    return sum(individual),


def register_evaluation(route):
    """
    Register evaluation method
    :param route: route type
    :raise RegistrationError: in case of undefined route
    :return: None
    """
    TOOLBOX.register("evaluate", eval_best_car, route=route)


def register_crossover(crossover):
    """
    Register the crossover operator
    :param crossover: crossover type
    :raise RegistrationError: in case of undefined crossover type
    :return: None
    """

    TOOLBOX.register("mate", tools.cxOnePoint)


def register_mutation(mutation):
    """
    Register a mutation operator
    :param mutation: mutation type
    :raise RegistrationError: in case of undefined mutation type
    :return: None
    """

    TOOLBOX.register("mutate", tools.mutFlipBit, indpb=MUTATION_PROBABILITY)


def register_selection(selection):
    """
    Register operator for selecting individuals for breeding the next
    generation
    :param selection: selection type
    :raise RegistrationError: in case of undefined selection type
    :return: None
    """

    TOOLBOX.register("select", tools.selTournament, tournsize=3)


def register_succession(succession):
    """
    Register succession
    :param succession: succession type
    :raise RegistrationError: in case of undefined succession type
    :return: None
    """


def init_toolbox(route, selection, crossover, mutation, succession):
    """
    Initialize genetic algorithm
    :param route: route type
    :param selection: selection type
    :param crossover: crossover type
    :param mutation: mutation type
    :param succession: succession type
    :return: None
    """

    register_evaluation(route)
    register_selection(selection)
    register_crossover(crossover)
    register_mutation(mutation)
    register_succession(succession)


def run(population_size, route, selection, crossover, mutation, succession):
    init_toolbox(selection=selection, crossover=crossover,
                 mutation=mutation, succession=succession,
                 route=route)

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = TOOLBOX.population(n=population_size)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2

    print("Start of evolution")

    # Evaluate the entire population
    fitnesses = list(map(TOOLBOX.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while g < 1000:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = TOOLBOX.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(TOOLBOX.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                TOOLBOX.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                TOOLBOX.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(TOOLBOX.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
