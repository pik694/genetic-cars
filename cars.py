"""Application module"""

import argparse

from genetic_cars.algorithm.algorithm import run

PARSER = argparse.ArgumentParser(description='Semestral project from ALHE course',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
PARSER.add_argument('population', type=int,
                    help='Population size')
PARSER.add_argument('route', type=int,
                    help='Route type')
PARSER.add_argument('selection', type=int,
                    help='Selection type')
PARSER.add_argument('crossover', type=int,
                    help='Crossover type')
PARSER.add_argument('mutation', type=int,
                    help='Mutation type')
PARSER.add_argument("--file", default="evolution.json",
                    help="file to save populations")


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
            file=args.file)
    except ValueError as err:
        print(str(err))
    except KeyboardInterrupt:
        print("\nCar generation stopped!")


if __name__ == "__main__":
    main()
