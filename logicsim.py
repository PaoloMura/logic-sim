# Logic Gate Simulation

import sys, os.path, pygame
from pygame.locals import *
from gateclass import *
from inputclass import *
from outputclass import *
from wireclass import *

# splits a pathname into (head, tail) where tail is the 
# final element in the path and head is everything before it
main_dir = os.path.split(os.path.abspath(__file__))[0]

SCREENRECT = Rect(0, 0, 1200, 800)
DROPZONERECT = Rect(150, 150, 900, 500)

BLACK = Color(0,0,0)
WHITE = Color(255,255,255)

def load_image(file):
    #loads an image, prepares it for play
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert_alpha()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs


# sort two components by x position
def sort_comps(comp_a:Component, comp_b:Component):
    if comp_a.get_pos_x() < comp_b.get_pos_x():
        return [comp_a, comp_b]
    else:
        return [comp_b, comp_a]


# choose which terminal to connect to
def choose_terminal(start_comp:Component, end_comp:Component):
    free_terminals = end_comp.avail_inp_terminals()
    if free_terminals == -1:    # no free terminals
        return None
    elif free_terminals < 2:    # one free terminal
        return free_terminals
    else:   # two free terminals to choose from
        if start_comp.get_pos_y() <= end_comp.get_pos_y():
            return 0
        else:
            return 1


# draw a set of lines between the start component's output terminal
# and the end component's chosen input terminal
def set_points(canvas, start_comp, end_comp, terminal):
    start = start_comp.get_out_terminal()
    end = end_comp.get_inp_terminal(terminal)
    delta_x = start[0] + 0.5 * (end[0] - start[0])
    mid1 = (delta_x, start[1])
    mid2 = (delta_x, end[1])
    points = (start, mid1, mid2, end)
    return points


# connect a wire between two components
def connect(canvas, comp_a:Component, comp_b:Component):
    # determine the start and end points
    if type(comp_b) == Gate:    # component_a is never a menu item
        if comp_a.is_menu_item():
            return None
    ordered_comps = sort_comps(comp_a, comp_b)
    start_comp = ordered_comps[0]
    end_comp = ordered_comps[1]
    if end_comp.get_pos_left() - start_comp.get_pos_right() < 10:
        return None
    terminal = choose_terminal(start_comp, end_comp)
    if terminal == None:
        return None
    # draw the lines and create a wire
    points = set_points(canvas, start_comp, end_comp, terminal)
    rect = pygame.draw.lines(canvas, BLACK, False, points)
    new_wire = Wire(start_comp, end_comp, terminal, points, rect)
    end_comp.add_input(start_comp, terminal)
    if type(start_comp) == Input:
        start_comp.connect()
    if type(end_comp) == Output:
        end_comp.connect()
    return new_wire


# clear a wire's lines from the screen
def clear_wire(canvas, wire:Wire):
    old_points = wire.get_points()
    pygame.draw.lines(canvas, WHITE, False, old_points)


# update a wire's position
def update_wire(canvas, wire:Wire):
    clear_wire(canvas, wire)
    new_points = set_points(canvas, wire.get_input(), wire.get_output(), wire.get_terminal())
    pygame.draw.lines(canvas, wire.get_colour(), False, new_points)
    wire.set_points(new_points)


def main(winstyle = 0):
    #initialise pygame
    pygame.init()

    #set display mode
    winstyle = 0    # fullscreen
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    #load images, assign to sprite classes
    if pygame.image.get_extended():
        AndGate.images = load_images('and.png', 'andselected.png')
        OrGate.images = load_images('or.png', 'orselected.png')
        NotGate.images = load_images('not.png', 'notselected.png')
        NandGate.images = load_images('nand.png', 'nandselected.png')
        NorGate.images = load_images('nor.png', 'norselected.png')
        XorGate.images = load_images('xor.png', 'xorselected.png')
        # images are in the order {0=false, 1=true, ...} to make indexing match booleans
        Input.images = load_images('inputafalse.png', 'inputatrue.png', 'inputaoff.png',
                                    'inputbfalse.png', 'inputbtrue.png', 'inputboff.png',
                                    'inputcfalse.png', 'inputctrue.png', 'inputcoff.png')
        Output.images = load_images('outputxfalse.png', 'outputxtrue.png', 'outputxoff.png',
                                    'outputyfalse.png', 'outputytrue.png', 'outputyoff.png')
    else:
        sys.exit("Can't load PNGs")

    #decorate the game window
    icon = pygame.transform.scale(AndGate.images[0], (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('LogicSim')

    #create the background, tile the bgd image
    bgdtile = load_image('logicsimbgd.png')
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()

    #create the textbox
    font = pygame.font.Font('freesansbold.ttf', 32)
    expression = ""
    text = font.render(expression, True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (SCREENRECT.centerx, SCREENRECT.height * 0.9)
    screen.blit(text, text_rect)

    #initialize Game Groups
    gates = pygame.sprite.Group()
    inputs = pygame.sprite.Group()
    outputs = pygame.sprite.Group()
    wires = []
    all = pygame.sprite.RenderUpdates()
    
    #assign default groups to each sprite class
    Gate.containers = gates, all
    Input.containers = inputs, all
    Output.containers = outputs, all

    #Create Some Starting Values
    clock = pygame.time.Clock()

    #initialize our starting sprites
    and_gate = AndGate(True)
    or_gate = OrGate(True)
    not_gate = NotGate(True)
    nand_gate = NandGate(True)
    nor_gate = NorGate(True)
    xor_gate = XorGate(True)

    input_a = Input(0)
    input_b = Input(1)
    input_c = Input(2)

    output_x = Output(0)
    output_y = Output(1)

    selected_component = None
    

    while True:
        #get input
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
            elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                for gate in gates:
                    if gate.is_selected():
                        # erase lines and component connections
                        remove_list = []
                        for wire in wires:
                            if wire.connected_to(gate):
                                clear_wire(screen, wire)
                                wire.disconnect(gate)
                                remove_list.append(wire)
                        # kill the wires
                        for wire in remove_list:
                            wires.remove(wire)
                        # kill the gate
                        gate.kill()
                        selected_component = None
            elif event.type == KEYDOWN and event.key == K_SPACE:
                for gate in gates:
                    if gate.is_selected():
                        gate.mobilise()
                for inp in inputs:
                    if inp.is_selected():
                        inp.switch()
                for out in outputs:
                    if out.is_selected() and out.is_connected():
                        expression = out.traverse()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for gate in gates:
                    # if the mouse is over the gate
                    if gate.rect.collidepoint(mouse_pos):
                        rect_list = list(map(lambda x : x.rect, all.sprites())) # a list of all sprite rects
                        rect_list.remove(gate.rect)                             # excluding that of the selected gate
                        # if a menu gate is selected
                        if gate.is_menu_item() and selected_component == None:
                            new_gate = gate.give_birth()
                            new_gate.select()
                            new_gate.mobilise()
                            selected_component = new_gate
                        # the selected gate is dropped in the dropzone if allowed
                        elif gate.is_selected() and DROPZONERECT.contains(gate.rect) and gate.rect.collidelist(rect_list) == -1:
                            gate.deselect()
                            selected_component = None
                        # connect the gate to the selected component
                        elif (selected_component != None) and (selected_component != gate) and (not gate.is_menu_item()):
                            new_wire = connect(screen, gate, selected_component)
                            if new_wire != None:
                                wires.append(new_wire)
                        # a gate in the dropzone is selected
                        elif selected_component == None:
                            gate.select()
                            selected_component = gate
                for inp in inputs:
                    # if the mouse is over an input
                    if inp.rect.collidepoint(mouse_pos):
                        # connect the input to the selected gate
                        if (selected_component in gates):
                            new_wire = connect(screen, inp, selected_component)
                            if new_wire != None:
                                wires.append(new_wire)
                        # select this input
                        elif selected_component == None:
                            inp.select()
                            selected_component = inp
                for out in outputs:
                    # if the mouse is over an output
                    if out.rect.collidepoint(mouse_pos):
                        # connect the output to the selected gate
                        if (selected_component in gates):
                            new_wire = connect(screen, out, selected_component)
                            if new_wire != None:
                                wires.append(new_wire)
                        # select this output
                        elif selected_component == None:
                            out.select()
                            selected_component = out
                # deselect a selected component if the mouse clicks elsewhere
                if (selected_component != None) and (not selected_component.rect.collidepoint(mouse_pos)):
                    selected_component.deselect()
                    selected_component = None

        # clear/erase the last drawn sprites
        all.clear(screen, background)
        pygame.draw.rect(screen, WHITE, text_rect)

        #update all the sprites
        all.update()
        for gate in gates:
            if gate.is_selected():
                gate.move(mouse_pos)
                for wire in wires:
                    if wire.connected_to(gate):
                        update_wire(screen, wire)
        for wire in wires:
            wire.update()

        #draw the scene
        dirty = all.draw(screen)
        for wire in wires:
            colour = wire.get_colour()
            points = wire.get_points()
            pygame.draw.lines(screen, colour, False, points)
        text = font.render(expression, True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (SCREENRECT.centerx, SCREENRECT.height * 0.9)
        screen.blit(text, text_rect)
        pygame.display.update(dirty)

        #cap the framerate
        clock.tick(40)

    pygame.time.wait(1000)
    pygame.quit()


#call the "main" function if running this script
if __name__ == '__main__': main()
