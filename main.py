import pygame
import os
import random
import math

pygame.init()

# STÄDA UPP KLASSERNA. SIZE OCH X OCH Y POSITIONER BEHÖVER INTE VARA MED
class tile4Matrix:
    def __init__(self):
        self.visible = True
        self.rect = None
        self.pairId = None
        self.image = None
        self.song = None

class tileData:
    def __init__(self):
        self.size = None
        self.spacing = None
        self.radius = None
        self.outline = None

class sideTileClass:
    def __init__(self):
        self.rect = None
        self.clickedTile = None
        self.radius = None

class boardClass:
    def __init__(self):
        self.height = None
        self.width = None
        self.x = None
        self.y = None

class animationClass:
    def __init__(self, id):
        self.id = id
        self.object = None
        self.counter = 0
        self.animation2Run = None
        self.runAnimation = False
        self.status = None

    def startAnimation(self, startAnimation, object = None):
        if object != None:
            self.object = object
        
        # if an object is assigned to the animation tile
        if self.object != None:
            if startAnimation == "disappear":
                self.animation2Run = disappearAnimation
                self.status = "started disappear"

            # the animation to start is "appear"
            else:
                self.animation2Run = appearAnimation
                self.status = "started appear"
            
            self.runAnimation = True

    def animateTile(self, rect):
        scaledRect = rect.scale_by(self.animation2Run[self.counter])
        pygame.draw.rect(screen, blue, scaledRect, 0, 0, tile.radius)
        self.counter += 1
        self.animationStatus()

    def animateSideTile(self, rect):
        global displaySideTile1
        global displaySideTile2

        scaledRect = rect.scale_by(self.animation2Run[self.counter])
        scaledImage = pygame.transform.scale(self.object.clickedTile.image, scaledRect.size)
        screen.blit(scaledImage, scaledRect)
        self.counter += 1
        self.animationStatus()

    def animationStatus(self):
        # checks if the animation is finished
        if self.counter > len(self.animation2Run) - 1:
            if self.id == "tile":     
                if self.status == "started disappear":
                    self.status = "finished disappear"
                
                # the finished animation was "appear"
                else:
                    self.status = "finished appear"
                    self.object.clickedTile.visible = True
                    self.clearData()
            
            # if the object is a side tile
            else:
                if self.status == "started disappear":
                    self.status = "finished disappear"
                    self.clearData()
                
                # the finished animation was "appear"
                else:
                    self.status = "finished appear"

            self.counter = 0
            self.runAnimation = False
    
    def clearData(self):
        self.object = None
        self.animation2Run = None

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
radiusScaleFactor = 1000
outlineScaleFactor = 1000
#radiusScaleFactor = 10
#outlineScaleFactor = 40
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
                # ÄNDRA HÄR
                tileMatrix[i][j].image = scaledSong
                tileMatrix[i][j].pairId = id
            
            if counter >= totalTiles:
                stopLoop = True
                break

        if stopLoop:
            break

def mouseClick(event, state):
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
                                tile1.startAnimation("disappear", sideTileList[0])
                            
                            elif numClickedTiles == 2:
                                tile2.startAnimation("disappear", sideTileList[1])
                        
                        stopLoop = True
                        break

                    counter += 1

                if stopLoop:
                    break

def displaySideTileFiles():
    if sideTile1.status == "finished appear":
        screen.blit(sideTileList[0].clickedTile.image, sideTileList[0].rect)
    
    if sideTile2.status == "finished appear":
        screen.blit(sideTileList[1].clickedTile.image, sideTileList[1].rect)

def animationHandler():
    global numClickedTiles
    
    if tile1.runAnimation == True:
        tile1.animateTile(tile1.object.clickedTile.rect)

        if tile1.status == "finished disappear":
            sideTile1.startAnimation("appear", sideTileList[0])

        elif tile1.status == "finished appear":
            sideTile2.startAnimation("disappear", sideTileList[1])

    if tile2.runAnimation == True:
        tile2.animateTile(tile2.object.clickedTile.rect)

        if tile2.status == "finished disappear":
            sideTile2.startAnimation("appear", sideTileList[1])

        elif tile2.status == "finished appear":
            numClickedTiles = 0

    if sideTile1.runAnimation == True:
        sideTile1.animateSideTile(sideTile1.object.rect)

        if sideTile1.status == "finished disappear":
            # if the two tiles didn't match
            if tilesMatch != True:
                tile1.startAnimation("appear", sideTileList[0])

    if sideTile2.runAnimation == True:
        sideTile2.animateSideTile(sideTile2.object.rect)

        if sideTile2.status == "finished disappear":

            if tilesMatch == True:
                resetAfterMatch()

            else:
                tile2.startAnimation("appear", sideTileList[1])

def createAnimations():
    dX = 1/fps
    a = -8
    x = -0.112
    c = 1.1

    disappear = []

    while True:
        scaleFactor = a*pow(x, 2) + c

        if scaleFactor < 0:
            break
        
        else:
            disappear.append(scaleFactor)
            x += dX

    appear = disappear.copy()
    appear.reverse()

    return disappear, appear

def checkIfMatch():
    global tilesMatch
    global tilesLeftOnBoard

    id1 = sideTileList[0].clickedTile.pairId
    id2 = sideTileList[1].clickedTile.pairId

    if(id1 == id2):
        tilesMatch = True
        sideTile1.startAnimation("dissapear", sideTileList[0])
        sideTile2.startAnimation("dissapear", sideTileList[1])

        tilesLeftOnBoard -= 2
        if tilesLeftOnBoard == 0:
            print("DU VANN!!!")

def resetAfterMatch():
    global numClickedTiles
    global tilesMatch

    tile1.clearData()
    tile2.clearData()

    numClickedTiles = 0
    tilesMatch = False

# global variables
totalTiles, path2Files = calculateTotalTiles()
# run is set to false if the amount of songs and images are not equal
if(run == True):
    numClickedTiles = 0
    numEnterClicks = 0
    tilesMatch = False
    tilesLeftOnBoard = totalTiles

    rows, columns = calculateRowsColumns(totalTiles)
    sideTileList = calculateSideTiles()   
    tile, board = calculateBoard()
    tileMatrix = generateTileMatrix()
    assignFiles2Tiles(path2Files)
    
    tile1 = animationClass("tile")
    tile2 = animationClass("tile")
    sideTile1 = animationClass("sideTile")
    sideTile2 = animationClass("sideTile")
    disappearAnimation, appearAnimation = createAnimations()

    displaySideTile1 = False
    displaySideTile2 = False

while run:
    timer.tick(fps)
    screen.fill(white)
    drawElements()
    drawTiles()
    outlineTiles()
    displaySideTileFiles()
    animationHandler()

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
                    checkIfMatch()
                    if tilesMatch == True:
                        print("MATCH!!!")
                        sideTile1.startAnimation("disappear")
                        sideTile2.startAnimation("disappear")


                    else:
                        sideTile1.startAnimation("disappear")                    

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
