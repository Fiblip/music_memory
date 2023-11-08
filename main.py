import pygame
import math

pygame.init()

# STÄDA UPP KLASSERNA. SIZE OCH X OCH Y POSITIONER BEHÖVER INTE VARA MED
class tile4Matrix:
    def __init__(self):
        self.visible = True
        self.data = None
        self.pairID = None

class tileData:
    def __init__(self):
        self.size = None
        self.spacing = None
        self.radius = None
        self.outline = None

class sideTileClass():
    def __init__(self):
        self.data = None
        self.radius = None

class boardClass():
    def __init__(self):
        self.height = None
        self.width = None
        self.x = None
        self.y = None
        self.excess = None

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# status variables
mouseStatus = None

# adjustable parameters
totalTiles = 22
minRatio = 3/2
boardScaleFactor = 0.9
tileScaleFactor = 0.9
radiusScaleFactor = 10
outlineScaleFactor = 40
sideBarScaleFactor = 1/3
sideTileScaleFactor = 0.65
fps = 60

# screen, side bar and game variables
displayInfo = pygame.display.Info()
#screenHeight = displayInfo.current_h
#screenWidth = displayInfo.current_w
screenScaleFactor = 80
screenHeight = 9*screenScaleFactor
screenWidth = 16*screenScaleFactor
screen = pygame.display.set_mode([screenWidth, screenHeight])

sideBar = pygame.Rect([0, 0, screenWidth*sideBarScaleFactor, screenHeight])

timer = pygame.time.Clock()
run = True

# functions
def calculateRowsColumns(product):
    if(product == 8):
        rows = 3
        columns = 3

    else:
        for i in range(2, math.floor(math.sqrt(product)) + 1):
            
            if (product % i == 0):
                rows = min(i, product/i)
                columns = max(i, product/i)
        
        if(columns/rows > minRatio):
            rows, columns = calculateRowsColumns(product + 2)
        
    return(int(rows), int(columns))

def calculateSideTiles():
    sideTileList = [sideTileClass(), sideTileClass()]

    size = sideBar.width*sideTileScaleFactor
    posX1 = (sideBar.width - size)/2
    posY1 = (sideBar.height - 2*size)/3
    posX2 = posX1
    posY2 = size + 2*(sideBar.height - 2*size)/3

    sideTileList[0].data = pygame.Rect([posX1, posY1, size, size])
    sideTileList[1].data = pygame.Rect([posX2, posY2, size, size])

    sideTileList[0].radius = round(sideTileList[0].data.width/radiusScaleFactor)
    sideTileList[1].radius = round(sideTileList[1].data.width/radiusScaleFactor)  

    return(sideTileList)    

def calculateBoard():
    board = boardClass()
    tile = tileData()

    maxBoardHeight = screenHeight - 2*sideTileList[0].data.y

    board.width = (screenWidth - sideBar.width)*boardScaleFactor
    tile.size = board.width*tileScaleFactor/columns
    tile.spacing = (board.width - tile.size*columns)/(columns - 1)

    if((tile.size*rows + tile.spacing*(rows - 1)) >= maxBoardHeight):
        board.height = maxBoardHeight
        tile.size = board.height*tileScaleFactor/rows
        tile.spacing = (board.height - tile.size*rows)/(rows - 1)
        board.width = columns*tile.size + tile.spacing*(columns - 1)

    else:
        board.height = rows*tile.size + tile.spacing*(rows - 1)

    board.y = (screenHeight - board.height)/2
    board.x = sideBar.width + (screenWidth - (sideBar.width + board.width))/2
    board.excess = rows*columns - totalTiles

    tile.radius = round(tile.size/radiusScaleFactor)
    tile.outline = round(tile.size/outlineScaleFactor)

    return(tile, board)

def drawElements():
    pygame.draw.rect(screen, black, sideBar)
    pygame.draw.rect(screen, white, sideTileList[0].data, 0, sideTileList[0].radius)
    pygame.draw.rect(screen, white, sideTileList[1].data, 0, sideTileList[1].radius)
    #boardObject = pygame.draw.rect(screen, black, [board.x, board.y, board.width, board.height])

def drawTiles():
    for i in range(rows):
        if(i == (rows - 1)):
            for j in range(columns - board.excess):
                if(tileMatrix[i][j].visible == True):
                    pygame.draw.rect(screen, blue, tileMatrix[i][j].data, 0, tile.radius)

                    if(tileMatrix[i][j].data.collidepoint(pygame.mouse.get_pos())):
                        pygame.draw.rect(screen, green, tileMatrix[i][j].data, tile.outline, tile.radius)

        else:
            for j in range(columns):
                if(tileMatrix[i][j].visible == True):
                    pygame.draw.rect(screen, blue, tileMatrix[i][j].data, 0, tile.radius)

                    if(tileMatrix[i][j].data.collidepoint(pygame.mouse.get_pos())):
                        pygame.draw.rect(screen, green, tileMatrix[i][j].data, tile.outline, tile.radius)

# IMPLEMENTERA SAMMA KOD SOM VID clickCollision
def generateTileMatrix():
    tileMatrix = [[tile4Matrix() for i in range(columns)] for j in range(rows)]
    
    if(board.excess != 0):
        for i in range(board.excess):
            tileMatrix[rows - 1][columns - 1 - i] = None

    for i in range(rows):
        if(i == (rows - 1)):
            for j in range(columns - board.excess):

                tileMatrix[i][j].data = pygame.Rect([board.x + j*(tile.size + tile.spacing), board.y + i*(tile.size + tile.spacing), tile.size, tile.size])

        else:
            for j in range(columns):
                tileMatrix[i][j].data = pygame.Rect([board.x + j*(tile.size + tile.spacing), board.y + i*(tile.size + tile.spacing), tile.size, tile.size])
    
    return tileMatrix

def clickCollision(pos):
    counter = 0

    for i in range(rows):
        for j in range(columns):

            if counter > totalTiles - 1:
                break

            elif(tileMatrix[i][j].data.collidepoint(pos)):
                tileMatrix[i][j].visible = False

            counter += 1

# code that runs once
rows, columns = calculateRowsColumns(totalTiles)
sideTileList = calculateSideTiles()   
tile, board = calculateBoard()
tileMatrix = generateTileMatrix()

while run:
    timer.tick(fps)
    screen.fill(white)
    drawElements()
    drawTiles()

    for event in pygame.event.get():

        # if X-button is pressed
        if event.type == pygame.QUIT:
            run = False

        # checks for keyboard presses
 
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                run = False

        # FIXA SÅ ATT KNAPPEN MÅSTE VARA TRYCKT OCH SLÄPPT PÅ RUTAN
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clickCollision(event.pos)

    pygame.display.flip()
pygame.quit()
