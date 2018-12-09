from . import MAX_COORDINATE, \
    MAX_FREQUENCY, \
    MAX_RADIUS


def denormalize_radius(radius):
    return radius * MAX_RADIUS


def denormalize_coordinate(coordinate):
    return coordinate * MAX_COORDINATE


def denormalize_frequency(frequency):
    return frequency * MAX_FREQUENCY
