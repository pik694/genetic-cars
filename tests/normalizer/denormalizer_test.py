import unittest

from genetic_cars.normalization.denormalizer import *


class DenormalizerTests(unittest.TestCase):

    def test_denormalize_radius(self):
        radius = 0.5
        self.assertEqual(MAX_RADIUS * radius, denormalize_radius(radius))

    def test_denormalize_coordinate(self):
        coordinate = 0.5
        self.assertEqual(MAX_COORDINATE * coordinate, denormalize_coordinate(coordinate))

    def test_denormalize_frequency(self):
        frequency = 0.5
        self.assertEqual(MAX_FREQUENCY * frequency, denormalize_frequency(frequency))
