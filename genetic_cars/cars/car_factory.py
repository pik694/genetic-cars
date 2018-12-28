"""
Car factory
Produces cars from genes
"""

from math import inf

from Box2D import b2CircleShape, b2FixtureDef, b2PolygonShape

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

    wheel_1 = parse_wheel(genes[0:3])

    wheel_2 = parse_wheel(genes[3:6])

    frequency = parse_frequency(genes[6])

    triangles = parse_triangles(genes[7:])

    return wheel_1, wheel_2, frequency, triangles


def create_car(genes, world):
    """
    Create car from given genes
    :param world:
    :param genes: List of genes representing single car
    :return: Car
    """

    wheel_1, wheel_2, freq, triangles = parse_genes(genes)

    car = Car(wheel_1, wheel_2, freq, triangles, world)

    return car


# pylint: disable=too-few-public-methods, too-many-instance-attributes
class Car:
    """
    Represents car created in Box2d library
    """

    # pylint: disable=too-many-arguments
    def __init__(self, wheel_1, wheel_2, frequency, triangles, world):
        self.wheels = []
        self.springs = []
        self.triangles = []
        self.world = world
        self.density = 1.0
        self.frequency = frequency
        self.joints = []
        self.damping_ratio = 0.7

        self._create_chassis(triangles=triangles)
        self._create_wheels(wheel_1=wheel_1, wheel_2=wheel_2)

    def _create_wheels(self, wheel_1, wheel_2):
        self._create_wheel(wheel_1)
        self._create_wheel(wheel_2)
        self._join_wheels()

    def _create_chassis(self, triangles):
        if not triangles:
            raise RuntimeError("No triangles for chassis")

        for triangle in triangles:
            self._create_triangle(triangle)

        self._join_chassis()

    def _create_triangle(self, triangle_params):
        vertices = list(triangle_params)
        chassis_triangle = self.world.CreateDynamicBody(
            position=(0, 0),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(vertices=vertices),
                density=self.density,
            )
        )

        self.triangles.append(chassis_triangle)

    def _create_wheel_joint(self, wheel):
        triangle = self._find_nearest_triangle(wheel.position)
        spring = self.world.CreateWheelJoint(
            bodyA=triangle,
            bodyB=wheel,
            anchor=wheel.position,
            axis=(0.0, 1.0),
            motorSpeed=-self.frequency,
            maxMotorTorque=20.0,
            enableMotor=True,
            frequencyHz=self.frequency,
            dampingRatio=self.damping_ratio
        )

        self.springs.append(spring)

    def _create_chassis_joint(self, triangle):
        nearest = self._find_nearest_triangle(triangle.localCenter)
        joint = self.world.CreateDistanceJoint(
            bodyA=triangle,
            bodyB=nearest,
            dampingRatio=self.damping_ratio
        )

        self.joints.append(joint)

    def _join_wheels(self):
        for wheel in self.wheels:
            self._create_wheel_joint(wheel=wheel)

    def _join_chassis(self):
        # no need for joining if only 1 triangle exists
        if len(self.triangles) > 1:
            for triangle in self.triangles:
                self._create_chassis_joint(triangle)

    def _create_wheel(self, wheel_params):
        wheel = self.world.CreateDynamicBody(
            position=(wheel_params[0][0], wheel_params[0][1]),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=wheel_params[-1]),
                density=self.density,
            )
        )

        self.wheels.append(wheel)

    def _find_nearest_triangle(self, position):
        distance = inf
        triangle = None

        for tmp_triangle in self.triangles:
            if tmp_triangle.localCenter == position:
                continue

            tmp_distance = ((tmp_triangle.localCenter[0] - position[0]) ** 2 +
                            (tmp_triangle.localCenter[1] - position[1]) ** 2)

            if tmp_distance < distance:
                distance, triangle = tmp_distance, tmp_triangle

        return triangle

    def get_position(self):
        """
        Get current position
        :return: current position
        """
        return max(self.wheels[0].position[0], self.wheels[1].position[0])
