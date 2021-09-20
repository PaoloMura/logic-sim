# Class for Components
# Children are: Gates, Inputs, Outputs

import sys, os.path, pygame
from pygame.locals import *

SCREENRECT = Rect(0, 0, 1200, 800)
DROPZONERECT = Rect(150, 150, 900, 500)


# the parent class for all components
class Component(pygame.sprite.Sprite):
    images = []
    tot_inp_terminals = 2   # total number of input terminals
    def __init__(self, first_image, scale_factor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = list(map(lambda x : pygame.transform.scale(x, scale_factor), self.images))
        self.image = self.images[first_image]
        self.rect = self.image.get_rect()
        self.inputs = [None for x in range(self.tot_inp_terminals)]    # a list of input components
        self.state = None   # i.e. True/False
        self.inp_terminals = [self.rect.topleft, self.rect.bottomleft]  # the coordinates of the terminals
        self.out_terminal = self.rect.midright
        self.selected = False
        self.name = ""
        self.precedence = 0

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def is_selected(self):
        return self.selected

    def disconnect(self, gate):
        i = self.inputs.index(gate)
        self.inputs[i] = None

    def add_input(self, new_input, terminal):
        self.inputs[terminal] = new_input

    def remove_input(self, old_input):
        index = self.inputs.index(old_input)
        self.inputs[index] = None

    def get_state(self):
        return self.state

    def get_inp_terminal(self, terminal):
        return self.inp_terminals[terminal]

    def get_out_terminal(self):
        return self.out_terminal

    def get_pos_x(self):
        return self.rect.centerx

    def get_pos_y(self):
        return self.rect.centery

    def get_pos_left(self):
        return self.rect.left

    def get_pos_right(self):
        return self.rect.right

    def get_precedence(self):
        return self.precedence

    # find which terminals are available
    # -1 indicates no free terminals
    # 0 or 1 indicate which terminal is available
    # 2 indicates both are available
    def avail_inp_terminals(self):
        num_free_terminals = self.inputs.count(None)
        if num_free_terminals == 0:
            return -1
        elif num_free_terminals == 1:
            if self.inputs[0] == None:
                return 0
            else:
                return 1
        else:
            return 2

    def traverse(self):
        return None
