import pygame
import os
import random
import math

pygame.init()

# STÄDA UPP KLASSERNA. SIZE OCH X OCH Y POSITIONER BEHÖVER INTE VARA MED
class tile4Matrix():
    def __init__(self):
        self.visible = True
        self.rect = None
        self.pairId = None
        self.image = None
        self.song = None

class tileData():
    def __init__(self):
        self.size = None
        self.spacing = None
        self.radius = None
        self.outline = None

class sideTileClass():
    def __init__(self):
        self.rect = None
        self.clickedTile = None
        self.radius = None

class boardClass():
    def __init__(self):
        self.height = None
        self.width = None
        self.x = None
        self.y = None

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# adjustable parameters
#totalTiles = 22
rootDir = "current_game"
imagesFolder = "images"
songsFolder = "songs"

minRatio = 3/2
boardScaleFactor = 0.9
tileScaleFactor = 0.9
radiusScaleFactor = 10
outlineScaleFactor = 40
sideBarScaleFactor = 1/3
sideTileScaleFactor = 0.65
animationTime = 1 # in seconds
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
def calculateTotalTiles():
    global run
    path = []

    for relPath, dirs, files in os.walk(rootDir):
        if imagesFolder in dirs:
            imagesPath = os.path.join(relPath, imagesFolder)
            images = os.listdir(imagesPath)

        if songsFolder in dirs:
            songsPath = os.path.join(relPath, songsFolder)
            songs = os.listdir(songsPath)

    for image in images:
        temp = os.path.join(imagesPath, image)
        path.append(r"%s" % temp)

    for song in songs:
        temp = os.path.join(songsPath, song)
        path.append(r"%s" % temp)
    
    if len(images) == len(songs):
        tiles = len(images) + len(songs)
        return(tiles, path)

    else:
        run = False

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

    sideTileList[0].rect = pygame.Rect([posX1, posY1, size, size])
    sideTileList[1].rect = pygame.Rect([posX2, posY2, size, size])

    sideTileList[0].radius = round(sideTileList[0].rect.width/radiusScaleFactor)
    sideTileList[1].radius = round(sideTileList[1].rect.width/radiusScaleFactor)  

    return(sideTileList)    

def calculateBoard():
    board = boardClass()
    tile = tileData()

    maxBoardHeight = screenHeight - 2*sideTileList[0].rect.y

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

    tile.radius = round(tile.size/radiusScaleFactor)
    tile.outline = round(tile.size/outlineScaleFactor)

    return(tile, board)

def drawElements():
    pygame.draw.rect(screen, black, sideBar)
    pygame.draw.rect(screen, white, sideTileList[0].rect, 0, sideTileList[0].radius)
    pygame.draw.rect(screen, white, sideTileList[1].rect, 0, sideTileList[1].radius)
    #boardObject = pygame.draw.rect(screen, black, [board.x, board.y, board.width, board.height])

def drawTiles():
    counter = 0
    stopLoop = False

    for i in range(rows):
        for j in range(columns):
            counter += 1

            if(tileMatrix[i][j].visible == True):
                pygame.draw.rect(screen, blue, tileMatrix[i][j].rect, 0, tile.radius)
            
            if counter >= totalTiles:
                stopLoop = True
                break
        
        if stopLoop:
            break

def outlineTiles():
    counter = 0
    stopLoop = False

    if numClickedTiles < 2:

        for i in range(rows):
            for j in range(columns):
                counter += 1

                if(tileMatrix[i][j].visible == True):
                    if(tileMatrix[i][j].rect.collidepoint(pygame.mouse.get_pos())):
                        pygame.draw.rect(screen, green, tileMatrix[i][j].rect, tile.outline, tile.radius)
            
                if counter >= totalTiles:
                    stopLoop = True
                    break
        
            if stopLoop:
                break

def generateTileMatrix():
    counter = 0
    stopLoop = False
    tileMatrix = [[None for i in range(columns)] for j in range(rows)]

    for i in range(rows):
        for j in range(columns):
            counter += 1
            tileMatrix[i][j] = tile4Matrix()
            tileMatrix[i][j].rect = pygame.Rect([board.x + j*(tile.size + tile.spacing), board.y + i*(tile.size + tile.spacing), tile.size, tile.size])

            if counter >= totalTiles:
                stopLoop = True
                break
            
        if stopLoop:
            break
    
    return tileMatrix

def assignFiles2Tiles(paths):
    counter = 0
    stopLoop = False

    for i in range(rows):
        for j in range(columns):
            counter += 1

            file = random.choice(paths)
            paths.remove(file)

            # extracts the number/name for each file
            temp = file.split("\\")[-1]
            id = temp.split(".")[0]

            if imagesFolder in file:
                image = pygame.image.load(file)
                scaledImage = pygame.transform.scale(image, sideTileList[0].rect.size)
                tileMatrix[i][j].image = scaledImage
                tileMatrix[i][j].pairId = id
            
            else:
                song = pygame.image.load(file)
                scaledSong = pygame.transform.scale(song, sideTileList[0].rect.size)
                tileMatrix[i][j].song = scaledSong
                tileMatrix[i][j].pairId = id
            
            if counter >= totalTiles:
                stopLoop = True
                break

        if stopLoop:
            break

def mouseClick(event, state):
    global setupAnimation1, setupAnimation2
    global animationSelection1, animationSelection2
    global clickedRow, clickedColumn
    global numClickedTiles
   
    counter = 0
    stopLoop = False
    
    if numClickedTiles < 2:
        if state == "down":
            for i in range(rows):
                for j in range(columns):

                    if counter > totalTiles - 1:
                        clickedRow = None
                        clickedColumn = None
                        stopLoop = True
                        break

                    if tileMatrix[i][j].rect.collidepoint(event.pos):
                        clickedRow = i
                        clickedColumn = j
                        stopLoop = True
                        break

                    counter += 1
                
                if stopLoop:
                    break

        elif state == "up":
            for i in range(rows):
                for j in range(columns):

                    if counter > totalTiles - 1:
                        clickedRow = None
                        clickedColumn = None
                        stopLoop = True
                        break

                    if (tileMatrix[i][j].rect.collidepoint(event.pos)) & (tileMatrix[i][j].visible == True):
                        if (clickedRow == i) & (clickedColumn == j):
                            numClickedTiles += 1
                            # assign file to side tile
                            sideTileList[numClickedTiles - 1].clickedTile = tileMatrix[i][j]
                            tileMatrix[i][j].visible = False

                            if numClickedTiles == 1:
                                setupAnimation1 = True
                                animationSelection1 = "disappear"
                            
                            elif numClickedTiles == 2:
                                setupAnimation2 = True
                                animationSelection2 = "disappear"
                        
                        stopLoop = True
                        break

                    counter += 1

                if stopLoop:
                    break

def displaySideTileFiles():
    # if the first side tile has a file attatched to it
    if sideTileList[0].clickedTile != None:
        # if the clicked tile is an image
        if sideTileList[0].clickedTile.image != None:
            screen.blit(sideTileList[0].clickedTile.image, sideTileList[0].rect)
        # if the clicked tile is a song
        else:
            screen.blit(sideTileList[0].clickedTile.song, sideTileList[0].rect)

    # if the second side tile has a file attatched to it
    if sideTileList[1].clickedTile != None:
        # if the clicked tile is an image
        if sideTileList[1].clickedTile.image != None:
            screen.blit(sideTileList[1].clickedTile.image, sideTileList[1].rect)
        # if the clicked tile is a song
        else:
            screen.blit(sideTileList[1].clickedTile.song, sideTileList[1].rect)

def animateTile1():
    global setupAnimation2
    global animationSelection2

    global setupAnimation1
    global runAnimation1

    global centerPosX
    global centerPosY
    global counter

    global animationTile
    
    if setupAnimation1 == True:
        setupAnimation1 = False
        runAnimation1 = True

        counter = 0

        centerPosX = sideTileList[0].clickedTile.rect.centerx
        centerPosY = sideTileList[0].clickedTile.rect.centery
        
        animationTile = sideTileList[0].clickedTile.rect.copy()

    if runAnimation1:
        if animationSelection1 == "disappear":
            if counter < len(tileAnimation):
                animationTile.width = tileAnimation[counter]
                animationTile.height = tileAnimation[counter]
                animationTile.centerx = centerPosX
                animationTile.centery = centerPosY
            
            else:
                runAnimation1 = False
        
        elif animationSelection1 == "appear":
            if counter < len(tileAnimation):
                animationTile.width = tileAnimation[-counter - 1]
                animationTile.height = tileAnimation[-counter - 1]
                animationTile.centerx = centerPosX
                animationTile.centery = centerPosY
            
            else:
                sideTileList[0].clickedTile.visible = True
                runAnimation1 = False
                sideTileList[0].clickedTile = None
                setupAnimation2 = True
                animationSelection2 = "appear"

        pygame.draw.rect(screen, blue, animationTile, 0, 0, tile.radius)
        counter += 1

def animateTile2():
    global numClickedTiles

    global setupAnimation2
    global runAnimation2

    global centerPosX
    global centerPosY
    global counter

    global animationTile
    
    if setupAnimation2 == True:
        setupAnimation2 = False
        runAnimation2 = True

        counter = 0

        centerPosX = sideTileList[1].clickedTile.rect.centerx
        centerPosY = sideTileList[1].clickedTile.rect.centery
        
        animationTile = sideTileList[1].clickedTile.rect.copy()

    if runAnimation2:
        if animationSelection2 == "disappear":
            if counter < len(tileAnimation):
                animationTile.width = tileAnimation[counter]
                animationTile.height = tileAnimation[counter]
                animationTile.centerx = centerPosX
                animationTile.centery = centerPosY
            
            else:
                runAnimation2 = False
        
        elif animationSelection2 == "appear":
            if counter < len(tileAnimation):
                animationTile.width = tileAnimation[-counter - 1]
                animationTile.height = tileAnimation[-counter - 1]
                animationTile.centerx = centerPosX
                animationTile.centery = centerPosY
            
            else:
                sideTileList[1].clickedTile.visible = True
                runAnimation2 = False
                numClickedTiles = 0
                sideTileList[1].clickedTile = None

        pygame.draw.rect(screen, blue, animationTile, 0, 0, tile.radius)
        counter += 1
    

def createTileAnimation():
    dX = 1/fps
    a = 5
    x = -0.2
    c = 1.2
    scaleFactor = -a*pow(x, 2) + c

    animation = []

    while scaleFactor >= 0:
        scaleFactor = -a*pow(x, 2) + c
        animation.append(scaleFactor*tile.size)
        x += dX

    return animation

# global variables
totalTiles, path2Files = calculateTotalTiles()
# run is set to false if the amount of songs and images are not equal
if(run == True):
    setupAnimation1 = False
    setupAnimation2 = False
    runAnimation1 = False
    runAnimation2 = False

    numClickedTiles = 0
    rows, columns = calculateRowsColumns(totalTiles)
    sideTileList = calculateSideTiles()   
    tile, board = calculateBoard()
    tileMatrix = generateTileMatrix()
    assignFiles2Tiles(path2Files)
    
    tileAnimation = createTileAnimation()
    animationStarted = False
    animationSelection1 = None
    animationSelection2 = None

while run:
    timer.tick(fps)
    screen.fill(white)
    drawElements()
    drawTiles()
    outlineTiles()
    displaySideTileFiles()
    animateTile1()
    animateTile2()

    # event handler
    for event in pygame.event.get():

        # if X-button is pressed
        if event.type == pygame.QUIT:
            run = False

        # checks for keyboard presses
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

            if event.key == pygame.K_RETURN:
                if numClickedTiles >= 2:
                    setupAnimation1 = True
                    animationSelection1 = "appear"

        # checks for mouse down
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseClick(event, "down")

        # checks for mouse button up
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouseClick(event, "up")

    pygame.display.flip()
pygame.quit()
