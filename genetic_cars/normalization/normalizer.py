from . import MAX_COORDINATE, \
    MAX_FREQUENCY, \
    MAX_RADIUS


def normalize_radius(radius):
    return radius / MAX_RADIUS


def normalize_coordinate(coordinate):
    return coordinate / MAX_COORDINATE


def normalize_frequency(frequency):
    return frequency / MAX_FREQUENCY
