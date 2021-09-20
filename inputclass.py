# Class for Inputs

import sys, os.path, pygame
from pygame.locals import *
from componentclass import *

SCREENRECT = Rect(0, 0, 1200, 800)
DROPZONERECT = Rect(150, 150, 900, 500)


# the class for all inputs
class Input(Component):
    start_pos = 0
    tot_inp_terminals = 0
    names = ["A", "B", "C"]
    def __init__(self, input_id:int):
        first_image = 3 * input_id + 2
        super().__init__(first_image, (65,55))
        self.id = input_id  # A=0, B=1, C=2
        self.name = self.names[self.id]
        self.start_pos = DROPZONERECT.top + (DROPZONERECT.height / 4) * (self.id + 1)
        self.rect.center = (DROPZONERECT.left, self.start_pos)
        self.inp_terminals = []
        self.out_terminal = self.rect.midright
        self.connections = 0

    def switch(self):
        if self.connections:
            if self.state == None:
                self.state = True
            else:
                self.state = not self.state
            self.image = self.images[3 * self.id + int(self.state)]
        else:
            state = None
            self.image = self.images[3 * self.id + 2]

    def connect(self):
        self.connections += 1

    def disconnect(self, gate):
        self.connections -= 1
        if self.connections == 0:
            self.switch()

    def traverse(self):
        return self.name
