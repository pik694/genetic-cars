"""Genetic algorithm implementation"""

import json
import os
import random

from deap import tools

from . import TOOLBOX, MUTATION_PROBABILITY, \
    ONE_POINT_CROSS, UNIFORM_CROSS, BIT_MUT, GAUSSIAN_MUT, \
    CXPB, MUTPB, TOURNAMENT_SEL, ROULETTE_SEL, BEST_SEL, SELECTION


def is_even(number):
    """
    Check whether number is even
    :param number: number to check
    :return: True if number is even
    """
    return number & 1 == 0


def individual_to_dict(ind):
    """
    Convert individual to serializable dictionary
    :param ind: individual
    :return: dict
    """
    individual = {
        'route': ind.fitness.values[0],
        'time': ind.fitness.values[1],
        'genes': ind
    }
    return individual


def population_to_dict(generation, population):
    """
    Prepare json containing given population
    :param generation: current population number
    :param population: genes of all population
    :return: population dict
    """
    inds = []
    for ind in population:
        individual = individual_to_dict(ind)
        inds.append(individual)
    pop = {
        "generation": generation,
        "population": inds
    }
    return pop


def save_population(generation, population, file):
    """
    Save population to json file
    :param generation: current population number
    :param population: genes of all population
    :param file: filepath
    :return: None
    """
    pop = population_to_dict(generation, population)
    if os.path.isfile(file):
        with open(file, 'ab') as outfile:
            outfile.seek(-1, os.SEEK_END)
            outfile.truncate()
            outfile.write(','.encode())
            outfile.write(json.dumps(pop).encode())
            outfile.write(']'.encode())
    else:
        with open(file, 'w') as outfile:
            array = [pop]
            json.dump(array, outfile)


def eval_best_car(individual, route):
    """
    Perform given individual
    :param individual: car genotype
    :param route: selected route
    :return: performance of an individual
    """
    # TODO
    return sum(individual), 100


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
    :raise ValueError: in case of undefined crossover type
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
    :raise ValueError: in case of undefined mutation type
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
    :raise ValueError: in case of undefined selection type or
    odd population size
    :return: None
    """
    if is_even(population_size) is False:
        raise ValueError("Population size must be even, given: {}"
                         .format(population_size))

    if selection == TOURNAMENT_SEL:
        TOOLBOX.register("select", tools.selTournament, tournsize=population_size)
    elif selection == ROULETTE_SEL:
        TOOLBOX.register("select", tools.selRoulette)
    elif selection == BEST_SEL:
        TOOLBOX.register("select", tools.selBest)
    else:
        raise ValueError("Invalid selection: {}".format(selection))


def init(population_size, route, selection, crossover, mutation):
    """
    Initialize genetic algorithm
    :param population_size: size of population
    :param route: route type
    :param selection: selection type
    :param crossover: crossover type
    :param mutation: mutation type
    :return: generation and initialized population
    """

    register_evaluation(route)
    register_selection(population_size, selection)
    register_crossover(crossover)
    register_mutation(mutation)

    return init_population(population_size)


# pylint: disable=no-member
def evaluate(individuals):
    """
    Evaluate individuals
    :param individuals: individuals to be evaluated
    :return: evaluated individuals
    """

    fitnesses = map(TOOLBOX.evaluate, individuals)
    for ind, fit in zip(individuals, fitnesses):
        ind.fitness.values = fit


# pylint: disable=no-member
def do_crossover(population):
    """
    Do crossover with probability CXPB
    :param population: population to be crossed
    :return: offspring
    """
    for child1, child2 in zip(population[::2], population[1::2]):
        if random.random() < CXPB:
            TOOLBOX.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    return population


# pylint: disable=no-member
def do_mutation(offspring):
    """
    Do mutation with probability MUTPB
    :param offspring: offspring to mutate
    :return: mutated offspring
    """

    for mutant in offspring:
        if random.random() < MUTPB:
            TOOLBOX.mutate(mutant)
            del mutant.fitness.values

    return offspring


# pylint: disable=no-member
def do_selection(population):
    """
    Do selection of best individuals
    :param population: whole population
    :return: cloned best individuals and their offspring
    """

    bests = TOOLBOX.select(population, int(SELECTION * len(population)))
    bests = list(map(TOOLBOX.clone, bests))
    offspring = list(map(TOOLBOX.clone, bests))

    return bests, offspring


# pylint: disable=no-member
def init_population(population_size):
    """
    Initialize population
    :param population_size: size of each population
    :return: population
    """

    population = TOOLBOX.population(n=population_size)
    evaluate(population)

    return 0, population


def do_evaluation(offspring):
    """
    Evaluate the offspring with an invalid fitness
    :param offspring: offspring
    :return: evaluated offspring
    """

    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    evaluate(invalid_ind)
    return offspring


# pylint: disable=too-many-arguments
def run(population_size, route, selection, crossover, mutation, file):
    """
    Genetic algorithm that prepare the best car
    :param file: file to save populations
    :param population_size: size of each population
    :param route: route type
    :param selection: selection type
    :param crossover: crossover type
    :param mutation: mutation type
    :return: None
    """
    generation, population = init(population_size=population_size,
                                  selection=selection, crossover=crossover,
                                  mutation=mutation, route=route)

    try:
        while True:
            save_population(generation, population, file)

            bests, offspring = do_selection(population)
            offspring = do_crossover(offspring)
            offspring = do_mutation(offspring)
            offspring = do_evaluation(offspring)

            generation, population[:] = generation + 1, offspring + bests

            best_ind = tools.selBest(population, 1)[0]
            print("Best score: {}".format(best_ind.fitness.values[0]))

    except KeyboardInterrupt:
        print("Car generation stopped!")
