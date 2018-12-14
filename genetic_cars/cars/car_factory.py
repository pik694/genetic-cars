"""
Car factory
Produces cars from genes
"""

from genetic_cars.normalization.denormalizer import denormalize_coordinate, \
    denormalize_frequency, \
    denormalize_radius, \
    denormalize_triangle_usage

from . import TRIANGLE_GENES, TRIANGLES


def parse_frequency(gene):
    """
    Parse frequency gene
    :param gene: frequency gene
    :return: frequency
    """

    return denormalize_frequency(gene)


def parse_wheel(genes):
    """
    Parse wheel's genes
    :param genes: wheel's genes
    :return: wheel
    """
    wheel = (
        (denormalize_coordinate(genes[0]),
         denormalize_coordinate(genes[1])),
        denormalize_radius(genes[2]))

    return wheel


def parse_point(genes):
    """
    Parse point's genes
    :param genes: point's genes
    :return: point
    """

    point = (
        denormalize_coordinate(genes[0]),
        denormalize_coordinate(genes[1])
    )

    return point


def parse_triangle(genes):
    """
    Parse single triangle's genes
    :param genes: triangle's genes
    :return: triangle or None if should not exist
    """
    if denormalize_triangle_usage(genes[0]) is False:
        return None

    triangle = (
        parse_point(genes[1:3]),
        parse_point(genes[3:5]),
        parse_point(genes[5:7])
    )

    return triangle


def parse_triangles(genes):
    """
    Parse chassis triangles' genes
    :param genes: triangles' genes
    :return: list of triangles
    """

    triangles = []
    for i in range(0, TRIANGLES):
        triangle = parse_triangle(genes[i * TRIANGLE_GENES:(i + 1) * TRIANGLE_GENES])
        if triangle is not None:
            triangles.append(triangle)

    return triangles


def parse_genes(genes):
    """
    Parse genes of single car
    :param genes: List of genes representing single car
    :return: wheels, frequency and chassis triangles
    """

    left_wheel = parse_wheel(genes[0:3])

    right_wheel = parse_wheel(genes[3:6])

    frequency = parse_frequency(genes[6])

    triangles = parse_triangles(genes[7:])

    return left_wheel, right_wheel, frequency, triangles
