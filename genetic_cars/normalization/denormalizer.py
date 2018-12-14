"""Denormalization methods"""

from . import MAX_COORDINATE, \
    MAX_FREQUENCY, \
    MAX_RADIUS


def denormalize_radius(radius):
    """
    Denormalize radius from gene
    :param radius: gene
    :return radius
    """

    return radius * MAX_RADIUS


def denormalize_coordinate(coordinate):
    """
    Denormalize coordinate from gene
    :param coordinate: gene
    :return coordinate
    """

    return coordinate * MAX_COORDINATE


def denormalize_frequency(frequency):
    """
    Denormalize frequency from gene
    :param frequency: gene
    :return frequency
    """

    return frequency * MAX_FREQUENCY


def denormalize_triangle_usage(usage):
    """Denormalize triangle usage
    :param usage: gene
    :return triangle usage
    """

    return usage >= 0.5
