import pygame

pygame.init()

# pygame parameters
displayInfo = pygame.display.Info()
screenHeight = displayInfo.current_h
screenWidth = displayInfo.current_w

run = True
fps = 60
timer =pygame.time.Clock()

# colors
white = (255, 255, 255)
black = (0, 0, 0)

# create screen
screen = pygame.display.set_mode([screenWidth, screenHeight])

# classes
class sideBarClass:
    
    def __init__(self, width, height):
        self.width = width/3
        self.height = height
        self.x = 0
        self.y = 0

        self.tileSize = self.width*0.75
        self.tile1PosX = (self.tileSize*0.25)/2
        self.tile1PosY = (height/2 - self.tileSize)/2
        self.tile2PosX = self.tile1PosX
        self.tile2PosY = height/2 + (height/2 - self.tileSize)/2

# init classes
sideBar = sideBarClass(screenWidth, screenHeight)

# functions
def generateBackgrounds():

    sideBarObject = pygame.draw.rect(screen, black, [sideBar.x, sideBar.y, sideBar.width, sideBar.height])
    tile1Object = pygame.draw.rect(screen, white, [sideBar.tile1PosX, sideBar.tile1PosY, sideBar.tileSize, sideBar.tileSize])
    tile2Object = pygame.draw.rect(screen, white, [sideBar.tile2PosX, sideBar.tile2PosY, sideBar.tileSize, sideBar.tileSize])

while run:

    timer.tick(fps)
    screen.fill(white)
    generateBackgrounds()

    for event in pygame.event.get():

        # if X-button is pressed
        if event.type == pygame.QUIT:
            run = False

        # checks for button presses
        if event.type == pygame.KEYDOWN:

            if event.key == (pygame.K_q and pygame.K_LCTRL):
                run = False

    pygame.display.flip()
pygame.quit()
