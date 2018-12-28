"""Box2d library wrapper"""

# pylint: disable=import-error
import time

import pygame
from Box2D import b2EdgeShape
from examples.framework import Framework

from . import MAX_DURATION, MAX_SAME_POSITION
from .car_factory import create_car


# pylint: disable=attribute-defined-outside-init
class CarFramework(Framework):
    """
    Class for running car evaluation
    """
    name = "Best car evolution"
    bridgePlanks = 20

    def __init__(self, route):
        super(CarFramework, self).__init__()
        self.running = False
        self.car = None
        self.duration = 0.0
        self.score = 0.0
        self.settings.drawMenu = False
        self.settings.drawFPS = False
        self.ground = None

        self._create_route(route)

    def _create_ground(self, start=-25.0, end=20.0):
        self.ground = self.world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=[(start, 0), (end, 0)])
        )

    @staticmethod
    def _get_vertices(route):
        if route == 1:
            vertices = [-1, 0.25, 1, 2, 0, 0, -1, -2, -2, -1.25, 0]
        elif route == 2:
            vertices = [1, 0.25, -0.7, 1.0, -1, -2, 0, 1, 0.5, 0, 1]
        elif route == 3:
            vertices = [0.5, -1, -0.7, 0, 1.5, 0.5, 1, 0, -0.5, 0, 1]
        else:
            raise RuntimeError("Undefined route")

        return vertices

    # pylint: disable=invalid-name
    def _create_route(self, route):
        x, y1, dx = 20, 0, 5
        self._create_ground(end=x)
        vertices = self._get_vertices(route)
        for y2 in vertices * 20:
            self._create_edge(x1=x, x2=x + dx, y1=y1, y2=y2)
            y1 = y2
            x += dx
        self._create_stop(x=x, y=y1)

    def _create_edge(self, x1, x2, y1, y2):
        self.ground.CreateEdgeFixture(
            vertices=[(x1, y1), (x2, y2)],
            density=0,
            friction=0.6,
        )

    def _create_stop(self, x, y):
        self._create_edge(x1=x, x2=x, y1=y, y2=100)

    def perform(self, genes):
        """
        Perform individual
        :return: performance
        """
        try:
            self.car = create_car(genes, self.world)
        except RuntimeError:
            return 0, 60

        self.run()

        return self.car.get_position(), self.duration

    def run(self):
        """
        Main loop.
        Updates the screen and tells the GUI to paint itself.
        """

        self.gui_table.updateGUI(self.settings)

        self.running = True
        clock = pygame.time.Clock()

        start_time = time.time()
        prev_position, same_position_counter = 0.0, 0
        self.duration = 0.0
        while self.running:
            self.screen.fill((0, 0, 0))
            self.SimulationLoop()
            pygame.display.flip()
            clock.tick(self.settings.hz)
            current_position = self.car.get_position()
            self.viewCenter = (current_position, 20)
            self.duration = time.time() - start_time

            if current_position <= prev_position:
                same_position_counter += 1
            else:
                prev_position = current_position

            if same_position_counter == MAX_SAME_POSITION:
                self.running = False
            elif self.duration > MAX_DURATION:
                self.running = False

        self.world.contactListener = None
        self.world.destructionListener = None
        self.world.renderer = None
