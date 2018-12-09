from genetic_cars.normalization.denormalizer import denormalize_coordinate, \
    denormalize_frequency, \
    denormalize_radius


def parse_frequency(gene):
    return denormalize_frequency(gene)


def parse_wheel(genes):
    wheel = (
        (denormalize_coordinate(genes[0]),
         denormalize_coordinate(genes[1])),
        denormalize_radius(genes[2]))

    return wheel


def parse_point(genes):
    point = (
        denormalize_coordinate(genes[0]),
        denormalize_coordinate(genes[1])
    )

    return point


def parse_triangle(genes):
    triangle = (
        parse_point(genes[0:2]),
        parse_point(genes[2:4]),
        parse_point(genes[4:6])
    )

    return triangle


def parse_triangles(genes):
    if len(genes) % 6 != 0:
        raise ValueError('Wrong amount of coordinates for triangles: ' + str(len(genes)))

    triangles = []
    for i in range(0, int(len(genes) / 6)):
        triangles.append(parse_triangle(genes[i * 6:(i + 1) * 6]))

    return triangles


def parse_genes(genes):
    left_wheel = parse_wheel(genes[0:3])

    right_wheel = parse_wheel(genes[3:6])

    frequency = parse_frequency(genes[6])

    triangles = parse_triangles(genes[7:])

    return left_wheel, right_wheel, frequency, triangles


def gen_car(genes):
    left_wheel, right_wheel, frequency, triangles = parse_genes(genes)
    pass
