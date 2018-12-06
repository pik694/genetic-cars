import unittest

from genetic_cars.normalizer.normalizer import normalize_wheel


class NormalizerTests(unittest.TestCase):

    def test_normalize_wheel(self):
        self.assertEqual(normalize_wheel(1), 1)
