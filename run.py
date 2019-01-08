import json
import sys

from genetic_cars.cars.car_framework import CarFramework


def main(filename):
    with open(filename) as f:
        best = json.load(f)

    genes = best['genes']
    car_framework = CarFramework(1)
    car_framework.perform(genes)


if __name__ == "__main__":
    main(sys.argv[1])
