# Classes for Logic Gates

import sys, os.path, pygame, numpy
from pygame.locals import *
from componentclass import *

SCREENRECT = Rect(0, 0, 1200, 800)


# the parent class for all logic gates
class Gate(Component):
    start_pos = 0
    terminala_offset = (0,0)    # input A terminal offset
    terminalb_offset = (0,0)    # input B terminal offset
    terminalc_offset = (0,0)    # output terminal offset
    tot_inp_terminals = 2
    def __init__(self, menu_item):
        super().__init__(0, (79,55))
        self.rect.centerx = self.start_pos
        terminal_a = numpy.subtract(self.rect.topleft, self.terminala_offset)
        terminal_b = numpy.subtract(self.rect.bottomleft, self.terminalb_offset)
        terminal_c = numpy.subtract(self.rect.midright, self.terminalc_offset)
        self.inp_terminals = [terminal_a, terminal_b]
        self.out_terminal = terminal_c
        self.mobile = False
        self.menu_item = menu_item

    def select(self):
        self.selected = True
        self.image = self.images[1]
        
    def deselect(self):
        self.selected = False
        self.mobile = False
        self.image = self.images[0]

    def mobilise(self):
        if self.selected:
            self.mobile = True
            self.image = self.images[0]

    def move(self, destination):
        if not self.menu_item and self.mobile:
            x = destination[0] - self.rect.centerx
            y = destination[1] - self.rect.centery
            self.rect.move_ip(x,y)
            self.moveTerminals()

    def moveTerminals(self):
        terminal_a = numpy.subtract(self.rect.topleft, self.terminala_offset)
        terminal_b = numpy.subtract(self.rect.bottomleft, self.terminalb_offset)
        terminal_c = numpy.subtract(self.rect.midright, self.terminalc_offset)
        self.inp_terminals = [terminal_a, terminal_b]
        self.out_terminal = terminal_c

    def is_menu_item(self):
        return self.menu_item

    def give_birth(self):
        return Gate(False)

    def get_rect(self):
        return self.rect

    def traverse(self):
        if None in self.inputs:
            return None
        else:
            expr1 = (self.inputs[0]).traverse()
            expr2 = (self.inputs[1]).traverse()
            if expr1 == None or expr2 == None:
                return None
            else:
                if (self.inputs[0]).get_precedence() >= self.precedence:
                    expr1 = "(" + expr1 + ")"
                if (self.inputs[1]).get_precedence() >= self.precedence:
                    expr2 = "(" + expr2 + ")"
                return expr1 + " " + self.name + " " + expr2


class AndGate(Gate):
    start_pos = (SCREENRECT.right / 6) * 0.5
    terminala_offset = (0,-14)
    terminalb_offset = (0,14)
    def __init__(self, menu_item):
        super().__init__(menu_item)
        self.name = "and"
        self.precedence = 2

    def update(self):
        disconnected_inputs = self.inputs.count(None)
        if disconnected_inputs:
            self.state = None
        else:
            self.state = self.inputs[0].get_state() and self.inputs[1].get_state()
    
    def give_birth(self):
        return AndGate(False)


class OrGate(Gate):
    start_pos = (SCREENRECT.right / 6) * 1.5
    terminala_offset = (-5,-14)
    terminalb_offset = (-5,14)
    def __init__(self, menu_item):
        super().__init__(menu_item)
        self.name = "or"
        self.precedence = 3

    def update(self):
        disconnected_inputs = self.inputs.count(None)
        if disconnected_inputs:
            self.state = None
        else:
            self.state = self.inputs[0].get_state() or self.inputs[1].get_state()

    def give_birth(self):
        return OrGate(False)


class NotGate(Gate):
    start_pos = (SCREENRECT.right / 6) * 2.5
    tot_inp_terminals = 1
    def __init__(self, menu_item):
        super().__init__(menu_item)
        self.inp_terminals = [self.rect.midleft]
        self.name = "not"
        self.precedence = 1

    def moveTerminals(self):
        self.inp_terminals = [self.rect.midleft]
        self.out_terminal = self.rect.midright

    def update(self):
        if self.inputs[0] == None:
            self.state = None
        else:
            self.state = not self.inputs[0].get_state()

    def give_birth(self):
        return NotGate(False)

    def traverse(self):
        if self.inputs[0] == None:
            return None
        else:
            expr = (self.inputs[0]).traverse()
            if expr == None:
                return None
            else:
                if (self.inputs[0]).get_precedence() >= self.precedence:
                    expr = "(" + expr + ")"
                return self.name + " " + expr


class NandGate(Gate):
    start_pos = (SCREENRECT.right / 6) * 3.5
    terminala_offset = (0,-14)
    terminalb_offset = (0,14)
    def __init__(self, menu_item):
        super().__init__(menu_item)
        self.name = "nand"
        self.precedence = 3

    def update(self):
        disconnected_inputs = self.inputs.count(None)
        if disconnected_inputs:
            self.state = None
        else:
            self.state = not(self.inputs[0].get_state() and self.inputs[1].get_state())
    
    def give_birth(self):
        return NandGate(False)


class NorGate(Gate):
    start_pos = (SCREENRECT.right / 6) * 4.5
    terminala_offset = (-5,-14)
    terminalb_offset = (-5,14)
    def __init__(self, menu_item):
        super().__init__(menu_item)
        self.name = "nor"
        self.precedence = 2

    def update(self):
        disconnected_inputs = self.inputs.count(None)
        if disconnected_inputs:
            self.state = None
        else:
            self.state = not (self.inputs[0].get_state() or self.inputs[1].get_state())

    def give_birth(self):
        return NorGate(False)


class XorGate(Gate):
    start_pos = (SCREENRECT.right / 6) * 5.5
    terminala_offset = (-5,-14)
    terminalb_offset = (-5,14)
    def __init__(self, menu_item):
        super().__init__(menu_item)
        self.name = "xor"
        self.precedence = 4

    def update(self):
        disconnected_inputs = self.inputs.count(None)
        if disconnected_inputs:
            self.state = None
        else:
            self.state = (self.inputs[0].get_state() and (not self.inputs[1].get_state())) or \
                        ((not self.inputs[0].get_state()) and self.inputs[1].get_state())

    def give_birth(self):
        return XorGate(False)
