import pygame
import math
import numpy as npArray

pygame.init()

class tile:
    def __init__(self):
        self.outline = False
        self.visible = True
        self.posX = None
        self.posY = None
        self.posCenterX = None
        self.posCenterY = None

# parameters
#displayInfo = pygame.display.Info()
#screenHeight = displayInfo.current_h
#screenWidth = displayInfo.current_w
screenScaleFactor = 80
screenHeight = 9*screenScaleFactor
screenWidth = 16*screenScaleFactor
screen = pygame.display.set_mode([screenWidth, screenHeight])

run = True
fps = 30
timer = pygame.time.Clock()

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# variables
totalTiles = 8
maxRatio = 3/2
boardScaleFactor = 0.9
tileScaleFactor = 0.9

# side bar
sideBarScaleFactor = 1/3
sideBarWidth = screenWidth*sideBarScaleFactor
sideBarHeight = screenHeight

# side bar tiles
sideTileScaleFactor = 0.65
sideTileSize = sideBarWidth*sideTileScaleFactor
sideTile1PosX = (sideBarWidth - sideTileSize)/2
sideTile1PosY = (sideBarHeight - 2*sideTileSize)/3
sideTile2PosX = sideTile1PosX
sideTile2PosY = sideTileSize + 2*(sideBarHeight - 2*sideTileSize)/3

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
        
        if(columns/rows > maxRatio):
            rows, columns = calculateRowsColumns(product + 2)
        
    return(int(rows), int(columns))

def calculateBoard():
    rows, columns = calculateRowsColumns(totalTiles)

    maxBoardHeight = screenHeight - 2*sideTile1PosY

    boardWidth = (screenWidth - sideBarWidth)*boardScaleFactor
    tileSize = boardWidth*tileScaleFactor/columns
    tileSpacing = (boardWidth - tileSize*columns)/(columns - 1)

    if((tileSize*rows + tileSpacing*(rows - 1)) >= maxBoardHeight):
        boardHeight = maxBoardHeight
        tileSize = boardHeight*tileScaleFactor/rows
        tileSpacing = (boardHeight - tileSize*rows)/(rows - 1)
        boardWidth = columns*tileSize + tileSpacing*(columns - 1)

    else:
        boardHeight = rows*tileSize + tileSpacing*(rows - 1)

    boardPosY = (screenHeight - boardHeight)/2
    boardPosX = sideBarWidth + (screenWidth - (sideBarWidth + boardWidth))/2
    excess = rows*columns - totalTiles

    return(rows, columns, tileSize, tileSpacing, boardHeight, boardWidth, boardPosX, boardPosY, excess)

def tilePositions():
    tilesPosX = npArray.empty(columns, dtype=int)
    tilesPosY = npArray.empty(columns, dtype=int)
    tilesCenterPosX = npArray.empty(columns, dtype=int)
    tilesCenterPosY = npArray.empty(columns, dtype=int)

    for i in range(columns):
        tilesPosX[i] = boardPosX + i*(tileSize + tileSpacing)
    
    for i in range(columns):
        tilesPosY[i] = boardPosY + i*(tileSize + tileSpacing)

    tilesCenterPosX = tilesPosX + tileSize/2
    tilesCenterPosY = tilesPosY + tileSize/2

    return(tilesPosX, tilesPosY, tilesCenterPosX, tilesCenterPosY)

def generateBackgrounds():
    sideBarObject = pygame.draw.rect(screen, black, [0, 0, sideBarWidth, sideBarHeight])
    tile1Object = pygame.draw.rect(screen, white, [sideTile1PosX, sideTile1PosY, sideTileSize, sideTileSize])
    tile2Object = pygame.draw.rect(screen, white, [sideTile2PosX, sideTile2PosY, sideTileSize, sideTileSize])
    #boardObject = pygame.draw.rect(screen, black, [boardPosX, boardPosY, boardWidth, boardHeight])

def drawTiles():
    for i in range(rows):

        if(i == (rows - 1)):
            for j in range(columns - excess):
                pygame.draw.rect(screen, blue, [tilesPosX[j], tilesPosY[i], tileSize, tileSize])

        else:
            for j in range(columns):
                pygame.draw.rect(screen, blue, [tilesPosX[j], tilesPosY[i], tileSize, tileSize])

def getPosition(x, y):
    for i in range(len(tilesPosY)):

        if((y >= tilesPosY[i]) & (y <= (tilesPosY[i] + tileSize))):
            row = i
            break

        else:
            row = None

    for j in range(len(tilesPosX)):

        if((x >= tilesPosX[j]) & (x <= (tilesPosX[j] + tileSize))):
            column = j
            break

        else:
            column = None
    
    return(row, column)

def generateTileMatrix():
    tileMatrix = npArray.full((rows, columns), tile())
    
    if(excess != 0):
        for i in range(excess):
            tileMatrix[rows - 1, columns - 1 - i] = None
    
    return tileMatrix

def assignTilePositions():
    for i in range(rows):

        if(i == (rows - 1)):
            for j in range(columns - excess):
                tileMatrix[i, j].posX = boardPosX + j*(tileSize + tileSpacing)
                tileMatrix[i, j].posY = boardPosY + i*(tileSize + tileSpacing)

        else:
            for j in range(columns):
                tileMatrix[i, j].posX = boardPosX + j*(tileSize + tileSpacing)
                tileMatrix[i, j].posY = boardPosY + i*(tileSize + tileSpacing)
                print(i, j)
                print(boardPosX + j*(tileSize + tileSpacing))  

# code that runs once   
rows, columns, tileSize, tileSpacing, boardHeight, boardWidth, boardPosX, boardPosY, excess = calculateBoard()
tilesPosX, tilesPosY, tilesCenterPosX, tilesCenterPosY = tilePositions()
tileMatrix = generateTileMatrix()
assignTilePositions()
print(tileMatrix[0,0].posX)
print(tilesPosX[0])

while run:

    timer.tick(fps)
    screen.fill(white)
    generateBackgrounds()
    drawTiles()
    #kan snygga till om muspositionen inte behövs
    mouseRow, mouseColumn = getPosition(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    #print(mouseRow, mouseColumn)

    for event in pygame.event.get():

        # if X-button is pressed
        if event.type == pygame.QUIT:
            run = False

        # checks for button presses
 
        if event.type == pygame.KEYDOWN:

            # funkar inte just nu
            #if event.key == pygame.K_q and event.key == pygame.K_LCTRL:
            #    run = False

            if event.key == pygame.K_q:
                run = False

    pygame.display.flip()
pygame.quit()
