# Logic Gate Simulation

import sys, os.path, pygame
from pygame.locals import *

# splits a pathname into (head, tail) where tail is the 
# final element in the path and head is everything before it
main_dir = os.path.split(os.path.abspath(__file__))[0]

SCREENRECT = Rect(0, 0, 1200, 800)

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


# the parent class for all logic gates
class Gate(pygame.sprite.Sprite):
    image = None
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.selected = False

    def select(self):
        self.selected = True

    def move(self, destination):
        if self.selected:
            x = destination[0] - self.rect.centerx
            y = destination[1] - self.rect.centery
            self.rect.move_ip(x,y)
        self.selected = False

def main(winstyle = 0):
    #initialise pygame
    pygame.init()

    #set display mode
    winstyle = 0    # fullscreen
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    #load images, assign to sprite classes
    if pygame.image.get_extended():
        img = load_image('and.png')
        Gate.image = img
    else:
        sys.exit("Can't load PNGs")

    #decorate the game window
    icon = pygame.transform.scale(Gate.image, (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('LogicSim')

    #create the background, tile the bgd image
    bgdtile = load_image('logicsimbgd.png')
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()

    #initialize Game Groups
    gates = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    
    #assign default groups to each sprite class
    Gate.containers = all

    #Create Some Starting Values
    clock = pygame.time.Clock()

    #initialize our starting sprites
    gate = Gate()
    

    while True:
        #get input
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                if gate.rect.collidepoint(mousepos):
                    gate.select()
                else:
                    gate.move(mousepos)
        keystate = pygame.key.get_pressed()

        # clear/erase the last drawn sprites
        all.clear(screen, background)

        #update all the sprites
        all.update()

        #handle user input

        # Detect collisions

        #draw the scene
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        #cap the framerate
        clock.tick(40)

    pygame.time.wait(1000)
    pygame.quit()


#call the "main" function if running this script
if __name__ == '__main__': main()
