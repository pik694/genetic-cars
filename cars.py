"""Application module"""

import argparse

from genetic_cars.algorithm import AlgorithmError
from genetic_cars.algorithm.algorithm import run

PARSER = argparse.ArgumentParser(description='Semestral project from ALHE course',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
PARSER.add_argument('population', type=int,
                    help='Population size')
PARSER.add_argument('route', type=int, default=[1, 2, 3],
                    help='Route type')
PARSER.add_argument('selection', type=int, default=[1, 2, 3],
                    help='Selection type')
PARSER.add_argument('crossover', type=int, default=[1, 2],
                    help='Crossover type')
PARSER.add_argument('mutation', type=int, default=[1, 2],
                    help='Mutation type')
PARSER.add_argument('succession', type=int, default=[1],
                    help='Succession type')


def main():
    """
    Main function, runs generation of the best car
    """
    args = PARSER.parse_args()

    try:
        run(population_size=args.population,
            route=args.route,
            selection=args.selection,
            crossover=args.crossover,
            mutation=args.mutation,
            succession=args.succession)
    except AlgorithmError as err:
        print(str(err))


if __name__ == "__main__":
    main()
