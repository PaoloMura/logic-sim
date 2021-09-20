# Class for Outputs

import sys, os.path, pygame
from pygame.locals import *
from componentclass import *

SCREENRECT = Rect(0, 0, 1200, 800)
DROPZONERECT = Rect(150, 150, 900, 500)


# the class for all outputs
class Output(Component):
    start_pos = 0
    tot_inp_terminals = 1
    names = ["X", "Y"]
    def __init__(self, input_id:int):
        first_image = 3 * input_id + 2
        super().__init__(first_image, (65,55))
        self.id = input_id  # X=0, Y=1
        self.name = self.names[self.id]
        self.start_pos = DROPZONERECT.top + (DROPZONERECT.height / 3) * (self.id + 1)
        self.rect.center = (DROPZONERECT.right, self.start_pos)
        self.inp_terminals = [self.rect.midleft]
        self.out_terminal = None
        self.connections = 0

    def connect(self):
        self.connections += 1

    def disconnect(self, gate):
        self.inputs = [None]
        self.connections -= 1

    def is_connected(self):
        return bool(self.connections)

    def update(self):
        # update state
        if self.inputs[0] == None:
            self.state = None
        else:
            self.state = self.inputs[0].get_state()
        # update image
        if self.state == None:
            self.image = self.images[3 * self.id + 2]
        else:
            self.image = self.images[3 * self.id + int(self.state)]

    def traverse(self):
        expression = (self.inputs[0]).traverse()
        if expression == None:
            return "Incomplete circuit"
        else:
            return self.name + " = " + expression
