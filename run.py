import json
import sys

from genetic_cars.cars.car_framework import CarFramework


def main(filename):
    with open(filename) as f:
        populations = json.load(f)

    for population in populations:
        for individual in population["population"]:
            car_framework = CarFramework(population["route"])
            car_framework.perform(individual["genes"])


if __name__ == "__main__":
    main(sys.argv[1])
