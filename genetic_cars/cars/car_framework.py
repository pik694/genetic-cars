"""Box2d library wrapper"""

# pylint: disable=import-error
import time

import pygame
from Box2D import b2EdgeShape
from examples.framework import Framework

from . import MAX_DURATION, MAX_SAME_POSITION
from .car_factory import create_car


# pylint: disable=invalid-name, attribute-defined-outside-init
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
        self.ground = None

        self._create_route(route)

    def _create_ground(self, start=-25.0, end=20.0):
        self.ground = self.world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=[(start, 0), (end, 0)])
        )

    def _create_route(self, route):
        # TODO
        if route == 1:
            self._create_route1()
        else:
            raise RuntimeError("Undefined route")

    def _create_route1(self):
        x, y1, dx = 20, 0, 5
        self._create_ground(end=x)
        vertices = [0.25, 1, 4, 0, 0, -1, -2, -2, -1.25, 0]
        for y2 in vertices * 2:  # iterate through vertices twice
            self.ground.CreateEdgeFixture(
                vertices=[(x, y1), (x + dx, y2)],
                density=0,
                friction=0.6,
            )
            y1 = y2
            x += dx

        x_offsets = [0, 80, 40, 20, 40]
        x_lengths = [40, 40, 10, 40, 0]
        y2s = [0, 0, 5, 0, 20]

        for x_offset, x_length, y2 in zip(x_offsets, x_lengths, y2s):
            x += x_offset
            self.ground.CreateEdgeFixture(
                vertices=[(x, 0), (x + x_length, y2)],
                density=0,
                friction=0.6,
            )

    def perform(self, genes):
        """
        Perform individual
        :return: performance
        """
        try:
            self.car = create_car(genes, self.world)
        except RuntimeError:
            return 0, 0

        self.run()

        return self.car.get_position(), self.duration

    def run(self):
        """
        Main loop.

        Continues to run while checkEvents indicates the user has
        requested to quit.

        Updates the screen and tells the GUI to paint itself.
        """
        # If any of the test constructors update the settings, reflect
        # those changes on the GUI before running

        self.gui_table.updateGUI(self.settings)

        self.running = True
        clock = pygame.time.Clock()

        start_time = time.time()
        prev_position, same_position_counter = 0.0, 0
        self.duration = 0.0
        while self.running:
            self.screen.fill((0, 0, 0))

            self.SimulationLoop()
            self.viewCenter = (self.car.get_position(), 20)

            if self.settings.drawMenu:
                self.gui_app.paint(self.screen)

            pygame.display.flip()
            clock.tick(self.settings.hz)
            self.fps = clock.get_fps()
            current_position = self.car.get_position()
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
