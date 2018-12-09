import unittest

from genetic_cars.normalization.normalizer import *


class NormalizerTests(unittest.TestCase):

    def test_normalize_radius(self):
        radius = 2
        self.assertEqual(radius / MAX_RADIUS, normalize_radius(radius))

    def test_normalize_coordinate(self):
        coordinate = 10
        self.assertEqual(coordinate / MAX_COORDINATE, normalize_coordinate(coordinate))

    def test_normalize_frequency(self):
        frequency = 5
        self.assertEqual(frequency / MAX_FREQUENCY, normalize_frequency(frequency))
