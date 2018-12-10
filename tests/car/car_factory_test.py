import unittest

from genetic_cars.cars.car_factory import *


class CarFactoryTests(unittest.TestCase):

    def parse_frequency(self):
        frequency = 0.5
        self.assertEqual(25, parse_frequency(frequency))

    def test_parse_point(self):
        point = [0.6, 0.4]
        self.assertEqual((60, 40), parse_point(point))

    def test_parse_wheel(self):
        wheel = [0.6, 0.4, 0.5]
        self.assertEqual(((60, 40), 5), parse_wheel(wheel))

    def test_parse_triangle(self):
        triangle = [0.5, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4]
        self.assertEqual(((60, 40), (60, 40), (60, 40)),
                         parse_triangle(triangle))

    def test_parse_triangles(self):
        triangles = [0.5, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4,
                     0.3, 0.4, 0.6, 0.4, 0.6, 0.4, 0.6,
                     0.4, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4,
                     0.7, 0.4, 0.6, 0.4, 0.6, 0.4, 0.6,
                     0.2, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4]

        result = parse_triangles(triangles)
        self.assertEqual(len(result), 2)
        self.assertEqual(((60.0, 40.0), (60.0, 40.0), (60.0, 40.0)), result[0])
        self.assertEqual(((40.0, 60.0), (40.0, 60.0), (40.0, 60.0)), result[1])

    def test_parse_genes(self):
        genes = [0.6, 0.4, 0.5, 0.4, 0.6, 1.0, 0.6,
                 0.3, 0.4, 0.6, 0.4, 0.6, 0.4, 0.6,
                 0.4, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4,
                 0.1, 0.4, 0.6, 0.4, 0.6, 0.4, 0.6,
                 0.2, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4,
                 0.5, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4]

        left_wheel, right_wheel, frequency, triangles = \
            parse_genes(genes)

        self.assertEqual(((60, 40), 5), left_wheel)
        self.assertEqual(((40, 60), 10), right_wheel)
        self.assertEqual(30, frequency)
        self.assertEqual([((60.0, 40.0), (60.0, 40.0), (60.0, 40.0))], triangles)
