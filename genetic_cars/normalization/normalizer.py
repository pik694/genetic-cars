"""Normalization methods"""

from . import MAX_COORDINATE, \
    MAX_FREQUENCY, \
    MAX_RADIUS


def normalize_radius(radius):
    """
    Convert radius value to gene
    :param radius: value
    :return: gene value
    """

    return radius / MAX_RADIUS


def normalize_coordinate(coordinate):
    """
    Convert coordinate to gene
    :param coordinate: value
    :return: coordinate gene
    """

    return coordinate / MAX_COORDINATE


def normalize_frequency(frequency):
    """
    Convert frequency to gene
    :param frequency: value
    :return: frequency gene
    """

    return frequency / MAX_FREQUENCY
