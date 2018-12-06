import unittest

from genetic_cars.cars.car import Car


class CarTests(unittest.TestCase):

    def test_car(self):
        car = Car(5)
        self.assertEqual(car.x, 5)
