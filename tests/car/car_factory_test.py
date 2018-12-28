import unittest

from genetic_cars.cars.car_factory import *


class CarFactoryTests(unittest.TestCase):

    def parse_frequency(self):
        frequency = 0.5
        self.assertEqual(25, parse_frequency(frequency))

    def test_parse_point(self):
        point = [0.6, 0.4]
        self.assertEqual((6.0, 4.0), parse_point(point))

    def test_parse_wheel(self):
        wheel = [0.6, 0.4, 0.5]
        self.assertEqual(((6.0, 4.0), 2.5), parse_wheel(wheel))

    def test_parse_triangle(self):
        triangle = [0.5, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4]
        self.assertEqual(((6.0, 4.0), (6.0, 4.0), (6.0, 4.0)),
                         parse_triangle(triangle))

    def test_parse_triangles(self):
        triangles = [0.5, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4,
                     0.3, 0.4, 0.6, 0.4, 0.6, 0.4, 0.6,
                     0.4, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4,
                     0.7, 0.4, 0.6, 0.4, 0.6, 0.4, 0.6,
                     0.2, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4]

        result = parse_triangles(triangles)
        self.assertEqual(len(result), 2)
        self.assertEqual(((6.0, 4.0), (6.0, 4.0), (6.0, 4.0)), result[0])
        self.assertEqual(((4.0, 6.0), (4.0, 6.0), (4.0, 6.0)), result[1])

    def test_parse_genes(self):
        genes = [0.6, 0.4, 0.5, 0.4, 0.6, 1.0, 0.6,
                 0.3, 0.4, 0.6, 0.4, 0.6, 0.4, 0.6,
                 0.4, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4,
                 0.1, 0.4, 0.6, 0.4, 0.6, 0.4, 0.6,
                 0.2, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4,
                 0.5, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4]

        left_wheel, right_wheel, frequency, triangles = \
            parse_genes(genes)

        self.assertEqual(((6.0, 4.0), 2.5), left_wheel)
        self.assertEqual(((4.0, 6.0), 5), right_wheel)
        self.assertEqual(30, frequency)
        self.assertEqual([((6.0, 4.0), (6.0, 4.0), (6.0, 4.0))], triangles)
