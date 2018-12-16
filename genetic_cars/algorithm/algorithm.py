"""Genetic algorithm implementation"""

import random

from deap import tools

from . import TOOLBOX, MUTATION_PROBABILITY, \
    ONE_POINT_CROSS, UNIFORM_CROSS, BIT_MUT, GAUSSIAN_MUT, \
    CXPB, MUTPB, TOURNAMENT_SEL, ROULETTE_SEL, BEST_SEL


def eval_best_car(individual, route):
    """
    Perform given individual
    :param individual: car genotype
    :param route: selected route
    :return: performance of an individual
    """
    # TODO
    return sum(individual),


def register_evaluation(route):
    """
    Register evaluation method
    :param route: route type
    :raise ValueError: in case of undefined route
    :return: None
    """
    if route not in [1, 2, 3]:
        raise ValueError("Invalid route: {}".format(route))

    TOOLBOX.register("evaluate", eval_best_car, route=route)


def register_crossover(crossover):
    """
    Register the crossover operator
    :param crossover: crossover type
    :raise RegistrationError: in case of undefined crossover type
    :return: None
    """

    if crossover == ONE_POINT_CROSS:
        TOOLBOX.register("mate", tools.cxOnePoint)
    elif crossover == UNIFORM_CROSS:
        TOOLBOX.register("mate", tools.cxUniform, indpb=0.5)
    else:
        raise ValueError("Invalid crossover: {}".format(crossover))


def register_mutation(mutation):
    """
    Register a mutation operator
    :param mutation: mutation type
    :raise RegistrationError: in case of undefined mutation type
    :return: None
    """

    if mutation == BIT_MUT:
        TOOLBOX.register("mutate", tools.mutFlipBit, indpb=MUTATION_PROBABILITY)
    elif mutation == GAUSSIAN_MUT:
        TOOLBOX.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=MUTATION_PROBABILITY)
    else:
        raise ValueError("Invalid mutation: {}".format(mutation))


def register_selection(population_size, selection):
    """
    Register operator for selecting individuals for breeding the next
    generation
    :param population_size: size of population
    :param selection: selection type
    :raise RegistrationError: in case of undefined selection type
    :return: None
    """
    if selection == TOURNAMENT_SEL:
        TOOLBOX.register("select", tools.selTournament, tournsize=int(population_size * 0.5))
    elif selection == ROULETTE_SEL:
        TOOLBOX.register("select", tools.selRoulette)
    elif selection == BEST_SEL:
        TOOLBOX.register("select", tools.selBest)


def init_toolbox(population_size, route, selection, crossover, mutation):
    """
    Initialize genetic algorithm
    :param population_size: size of population
    :param route: route type
    :param selection: selection type
    :param crossover: crossover type
    :param mutation: mutation type
    :return: None
    """

    register_evaluation(route)
    register_selection(population_size, selection)
    register_crossover(crossover)
    register_mutation(mutation)


# pylint: disable=no-member
def run(population_size, route, selection, crossover, mutation):
    """
    Genetic algorithm that prepare the best car
    :param population_size: size of each population
    :param route: route type
    :param selection: selection type
    :param crossover: crossover type
    :param mutation: mutation type
    :return: None
    """

    init_toolbox(population_size=population_size,
                 selection=selection, crossover=crossover,
                 mutation=mutation, route=route)

    population = TOOLBOX.population(n=population_size)
    fitnesses = list(map(TOOLBOX.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(population))

    # Begin the evolution
    for g in range(0, 1000):

        print(g)
        # Select the next generation individuals
        offspring = TOOLBOX.select(population, len(population))
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

        # The population is entirely replaced by the offspring
        population[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in population]

        print("  Max %s" % max(fits))

    best_ind = tools.selBest(population, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
