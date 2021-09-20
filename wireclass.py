# Class for Wires
# use Wire objects to keep a track of the line points

import sys, os.path, pygame
from pygame.locals import *
from componentclass import *
from inputclass import *
from outputclass import *
from gateclass import *

SCREENRECT = Rect(0, 0, 1200, 800)
DROPZONERECT = Rect(150, 150, 900, 500)

BLACK = Color(0,0,0)
WHITE = Color(255,255,255)
RED = Color(255,0,0)
GREEN = Color(0,255,0)


# the class for all wires
class Wire():
    def __init__(self, input_component:Component, output_component:Component, terminal:int, points:tuple, rect:Rect):
        self.input = input_component
        self.output = output_component
        self.terminal = terminal
        self.points = points
        self.rect = rect
        self.state = self.input.get_state()
        self.selected = False

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def is_selected(self):
        return self.selected

    def update(self):
        self.state = self.input.get_state()

    def get_rect(self):
        return self.rect

    def get_colour(self):
        if self.state == True:
            return GREEN
        elif self.state == False:
            return RED
        else:
            return BLACK

    def get_points(self):
        return self.points

    def set_points(self, points:tuple):
        self.points = points

    def connected_to(self, comp):
        if self.input == comp or self.output == comp:
            return True
        else:
            return False

    def disconnect(self, gate:Gate):
        if self.input == gate:
            self.output.disconnect(gate)
        elif type(self.input) == Input:
            self.input.disconnect(gate)

    def get_input(self):
        return self.input

    def get_output(self):
        return self.output

    def get_terminal(self):
        return self.terminal
