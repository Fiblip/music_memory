import pygame
import os
import random
import math

class tile4Matrix:
    def __init__(self):
        self.visible = True
        self.rect = None
        self.pairId = None
        self.image = None
        self.sound = None
        self.speakerAnimationCounter = 0

    def nextSoundAnimationImage(self):
        if self.sound != None:
            image = pygame.image.load(speakerAnimation[math.floor(self.speakerAnimationCounter)])
            scaledImage = pygame.transform.scale(image, sideTile1.rect.size)
            self.image = scaledImage

            self.speakerAnimationCounter += speakerAnimationSpeed
            if math.floor(self.speakerAnimationCounter) > len(os.listdir(speakerAnimationFolder)) - 1:
                self.speakerAnimationCounter = 0

class musicClass:
    def __init__(self, backgroundMusic, fadeIn, fadeOut):
        self.backgroundMusic = backgroundMusic
        self.backgroundMusicResumePosition = None
        self.timeSinceLastPause = 0
        self.fadeOut = fadeOut
        self.fadeIn = fadeIn
        self.currentlyPlaying = None
        self.tileSound = None

        pygame.mixer.music.load(self.backgroundMusic)
        pygame.mixer.music.play()
        self.currentlyPlaying = self.backgroundMusic
        pygame.mixer.music.set_volume(backgroundMusicVolume)
        pygame.mixer.music.set_endevent(RESTART_BACKGROUND_SONG)

    def resumeBackgroundMusic(self):
        global animateSideTile1Sound
        global animateSideTile2Sound

        pygame.mixer.music.load(self.backgroundMusic)
        pygame.mixer.music.play(0, self.backgroundMusicResumePosition/1000, self.fadeIn)
        pygame.mixer.music.set_volume(backgroundMusicVolume)
        self.currentlyPlaying = self.backgroundMusic
        pygame.mixer.music.set_endevent(RESTART_BACKGROUND_SONG)
        self.backgroundMusicResumePosition = None

        animateSideTile1Sound = False
        animateSideTile2Sound = False

    def soundHandler(self, caller):
        if music.tileSound == None:
            return

        elif caller == sideTile1:
            if self.tileSound == sideTile1.clickedTile.sound:
                self.playTileSound()
        
        else:
            if self.tileSound == sideTile2.clickedTile.sound:
                self.playTileSound()

    def playTileSound(self):
        pygame.mixer.music.unload()
        pygame.mixer.music.load(self.tileSound)
        self.currentlyPlaying = self.tileSound
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(soundVolume)
        pygame.mixer.music.set_endevent(RESUME_BACKGROUND_SONG)

        self.startSoundAnimation()
    
    def queueTileSound(self):
        if self.backgroundMusicResumePosition == None:
            self.backgroundMusicResumePosition = pygame.mixer.music.get_pos() + self.timeSinceLastPause + self.fadeOut
            self.timeSinceLastPause = self.backgroundMusicResumePosition

        pygame.mixer.music.fadeout(self.fadeOut)
        pygame.mixer.music.set_endevent(MUSIC_CHANNEL_STOPPED)

    def restartBackgroundMusic(self):
        pygame.mixer.music.play()
        self.timeSinceLastPause = 0

    def reset(self):
        if self.currentlyPlaying != self.backgroundMusic:
            pygame.mixer.music.fadeout(self.fadeOut)

        # fixes bug where the reset function is called just as the MUSIC_CHANNEL_STOPPED end event is recieved
        # by the eventhandler and before the sound has started playing
        elif pygame.mixer.music.get_busy() == False:
            self.resumeBackgroundMusic()
        
        self.tileSound = None

    def startSoundAnimation(self):
        global animateSideTile1Sound
        global animateSideTile2Sound

        if sideTile2.clickedTile != None:
            if sideTile2.clickedTile.sound == music.tileSound:
                animateSideTile1Sound = False
                animateSideTile2Sound = True

        if sideTile1.clickedTile.sound == music.tileSound:
            animateSideTile1Sound = True

class tileData:
    def __init__(self):
        self.size = None
        self.spacing = None
        self.radius = None
        self.outline = None

class sideTileClass:
    def __init__(self):
        self.rect = None
        self.radius = None
        self.clickedTile = None

class boardClass:
    def __init__(self):
        self.height = None
        self.width = None
        self.x = None
        self.y = None

class animationClass:
    def __init__(self, id):
        self.id = id
        self.clickedTile = None
        self.rect = None
        self.counter = 0
        self.animation2Run = None
        self.animationEnabled = False
        self.status = None

    def startAnimation(self, startAnimation, tile = None, rect = None):        
        if (tile != None) & (rect != None):
            self.clickedTile = tile
            self.rect = rect
        
        # if a clickedTile is assigned to the animation tile
        if self.clickedTile != None:
            if startAnimation == "disappear":
                self.animation2Run = disappearAnimation
                
                if self.id == "tile":
                    self.clickedTile.visible = False
                
                self.status = "started disappear"

            elif startAnimation == "appear":
                self.animation2Run = appearAnimation
                self.status = "started appear"
            
            # only side tiles can run the match animation
            elif startAnimation == "match":
                    self.animation2Run = disappearAnimation
                    self.status = "started match"

            self.animationEnabled = True

    def animateTile(self, rect):
        scaledRect = rect.scale_by(self.animation2Run[self.counter])
        scaledImage = pygame.transform.scale(tileTexture, scaledRect.size)
        screen.blit(scaledImage, scaledRect)
        self.counter += 1
        self.animationStatus()

    def animateSideTile(self, rect):
        global displaySideTile1
        global displaySideTile2

        scaledRect = rect.scale_by(self.animation2Run[self.counter])
        scaledImage = pygame.transform.scale(self.clickedTile.image, scaledRect.size)
        screen.blit(scaledImage, scaledRect)
        self.counter += 1
        self.animationStatus()

    def animationStatus(self):
        # checks if the animation is finished
        if self.counter > len(self.animation2Run) - 1:
            if self.id == "tile":  
                if self.status == "started disappear": 
                    self.status = "finished disappear"
                    
                else:
                    self.status = "finished appear"
                    self.clickedTile.visible = True
                    self.clearAnimationData()
            
            # if self is a side tile
            else:
                if self.status == "started disappear":
                    self.status = "finished disappear"
                    self.clearAnimationData()

                elif self.status == "started appear":
                    self.status = "finished appear"
                
                # the finished animation was "match"
                else:
                    self.status = "finished match"

            self.counter = 0
            self.animationEnabled = False
    
    def clearAnimationData(self):
        global animateSideTile1Sound
        global animateSideTile2Sound

        self.clickedTile = None
        self.rect = None
        self.animation2Run = None

        animateSideTile1Sound = False
        animateSideTile2Sound = False

pygame.init()

# event handler IDs
RESUME_BACKGROUND_SONG = pygame.USEREVENT+1
RESTART_BACKGROUND_SONG = pygame.USEREVENT+2
START_TILE_SONG = pygame.USEREVENT+3
MUSIC_CHANNEL_STOPPED = pygame.USEREVENT+4

# colors
black = (0, 0, 0)
blackTransparent = (0, 0, 0, 100)
redTransparent = (255, 0, 0, 50)
greenTransparent = (0, 255, 0, 50)
orange = (211, 119, 40)

# directories and files
rootDir = "current_game"
imagesFolder = "images"
soundsFolder = "sounds"
speakerAnimationFolder = "assets/notes_animation/"
tileTexturePath = "assets/tile_texture.png"
backgroundPath = "assets/background.jpg"

# adjustable parameters
minRatio = 3/2
boardScaleFactor = 0.9
tileScaleFactor = 0.9
radiusScaleFactor = 6
outlineScaleFactor = 20
sideBarScaleFactor = 1/3
sideTileScaleFactor = 0.7

# animation parameters
fps = 60
animationTime = 1 #in seconds
speakerAnimationSpeed = 0.4

# music parameters
fadeIn = animationTime*800 # in milliseconds
fadeOut = fadeIn
backgroundMusicVolume = 0.2
soundVolume = 0.3
soundEffectVolume = 0.6
backgroundMusic = "assets/background_music.mp3"
correctSound = pygame.mixer.Sound("assets/correct.mp3")
wrongSound = pygame.mixer.Sound("assets/wrong.mp3")
correctSound.set_volume(soundEffectVolume)
wrongSound.set_volume(soundEffectVolume)

# screen, side bar and game variables
displayInfo = pygame.display.Info()
screenHeight = displayInfo.current_h
screenWidth = displayInfo.current_w
# screenScaleFactor = 80
# screenHeight = 9*screenScaleFactor
# screenWidth = 16*screenScaleFactor
screen = pygame.display.set_mode([screenWidth, screenHeight])
screenSurfaceBack = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
screenSurfaceFront = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)

sideBar = pygame.Rect([0, 0, screenWidth*sideBarScaleFactor, screenHeight])

timer = pygame.time.Clock()
run = True

# functions
def calculateTotalTiles():
    path = []

    for relPath, dirs, files in os.walk(rootDir):
        if imagesFolder in dirs:
            imagesPath = os.path.join(relPath, imagesFolder)
            images = os.listdir(imagesPath)

        if soundsFolder in dirs:
            soundsPath = os.path.join(relPath, soundsFolder)
            sounds = os.listdir(soundsPath)

    for image in images:
        temp = os.path.join(imagesPath, image)
        path.append(r"%s" % temp)

    for sound in sounds:
        temp = os.path.join(soundsPath, sound)
        path.append(r"%s" % temp)
    
    tiles = len(images) + len(sounds)
    return(tiles, path)

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
    sideTile1 = sideTileClass()
    sideTile2 = sideTileClass()

    size = sideBar.width*sideTileScaleFactor
    posX1 = (sideBar.width - size)/2
    posY1 = (sideBar.height - 2*size)/3
    posX2 = posX1
    posY2 = size + 2*(sideBar.height - 2*size)/3

    sideTile1.rect = pygame.Rect([posX1, posY1, size, size])
    sideTile2.rect = pygame.Rect([posX2, posY2, size, size])

    sideTile1.radius = round(sideTile1.rect.width/radiusScaleFactor)
    sideTile2.radius = round(sideTile2.rect.width/radiusScaleFactor)  

    return(sideTile1, sideTile2)    

def calculateBoard():
    board = boardClass()
    tile = tileData()

    maxBoardHeight = screenHeight - 2*sideTile1.rect.y

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

def drawBackgroundElements():
    screen.blit(background, backgroundPosition)
    screen.blit(screenSurfaceBack, (0, 0))
    pygame.draw.rect(screenSurfaceBack, blackTransparent, sideTile1.rect, 0, sideTile1.radius)
    pygame.draw.rect(screenSurfaceBack, blackTransparent, sideTile2.rect, 0, sideTile2.radius)

def loadTileTexture():
    tileTexture = pygame.image.load(tileTexturePath)
    scaledTileTexture = pygame.transform.scale(tileTexture, tileMatrix[0][0].rect.size)

    return scaledTileTexture

def drawTiles():
    counter = 0
    stopLoop = False

    for i in range(rows):
        for j in range(columns):
            counter += 1

            if tileMatrix[i][j].visible == False:
                pygame.draw.rect(screenSurfaceBack, blackTransparent, tileMatrix[i][j].rect, 0, tile.radius)

            if tileMatrix[i][j].visible == True:
                screen.blit(tileTexture, tileMatrix[i][j].rect)
            
            if counter >= totalTiles:
                stopLoop = True
                break
        
        if stopLoop:
            break

def outlineTiles():
    counter = 0
    stopLoop = False

    if (sideTile1.clickedTile == None) or (sideTile2.clickedTile == None):
        for i in range(rows):
            for j in range(columns):
                counter += 1

                if(tileMatrix[i][j].visible == True):
                    if(tileMatrix[i][j].rect.collidepoint(pygame.mouse.get_pos())):
                        pygame.draw.rect(screen, orange, tileMatrix[i][j].rect, tile.outline, tile.radius)
            
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
                scaledImage = pygame.transform.scale(image, sideTile1.rect.size)
                tileMatrix[i][j].image = scaledImage
                tileMatrix[i][j].pairId = id
            
            # if the chosen element was a sound
            else:
                tileMatrix[i][j].sound = file
                tileMatrix[i][j].pairId = id
            
            if counter >= totalTiles:
                stopLoop = True
                break

        if stopLoop:
            break

def mouseClick(event, state):
    global clickedRow, clickedColumn
   
    counter = 0
    stopLoop = False
    
    if (sideTile1.clickedTile == None) or (sideTile2.clickedTile == None):
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

                            if sideTile1.clickedTile == None:
                                sideTile1.clickedTile = tileMatrix[i][j]

                                if sideTile1.clickedTile.sound != None:
                                    music.tileSound = sideTile1.clickedTile.sound
                                    music.queueTileSound()

                                if tile1Animation.animationEnabled == False:
                                    tile1Animation.startAnimation("disappear", sideTile1.clickedTile, sideTile1.clickedTile.rect)
                                
                                # tile1Animation is busy and is currently running another animation
                                else:
                                    tile1AnimationExtra.startAnimation("disappear", sideTile1.clickedTile, sideTile1.clickedTile.rect)

                            # sideTile1.clickedTile is assigned a tile but sideTile2.clickedTile is not
                            else:
                                sideTile2.clickedTile = tileMatrix[i][j]

                                if sideTile2.clickedTile.sound != None:
                                    music.tileSound = sideTile2.clickedTile.sound
                                    music.queueTileSound()

                                if tile2Animation.animationEnabled == False:
                                    tile2Animation.startAnimation("disappear", sideTile2.clickedTile, sideTile2.clickedTile.rect)
                                
                                # tile2Animation is busy and is currently running another animation
                                else:
                                    tile2AnimationExtra.startAnimation("disappear", sideTile2.clickedTile, sideTile2.clickedTile.rect)                                
                        
                        stopLoop = True
                        break

                    counter += 1

                if stopLoop:
                    break

def displaySideTileFiles():
    if sideTile1Animation.status == "finished appear":
        screen.blit(sideTile1.clickedTile.image, sideTile1.rect)
    
    if sideTile2Animation.status == "finished appear":
        screen.blit(sideTile2.clickedTile.image, sideTile2.rect)

def animationHandler():
    if (animateSideTile1Sound == True) & (sideTile1.clickedTile != None):
        sideTile1.clickedTile.nextSoundAnimationImage()

    if (animateSideTile2Sound == True) & (sideTile2.clickedTile != None):
        sideTile2.clickedTile.nextSoundAnimationImage()
    
    if tile1Animation.animationEnabled == True:
        tile1Animation.animateTile(tile1Animation.rect)

        if tile1Animation.status == "finished disappear":
            # loads the first speaker animation image so we dont get errors
            sideTile1.clickedTile.nextSoundAnimationImage()
            sideTile1Animation.startAnimation("appear", sideTile1.clickedTile, sideTile1.rect)

        elif tile1Animation.status == "finished appear":
            sideTile2Animation.startAnimation("disappear", sideTile2.clickedTile, sideTile2.rect)

    if tile2Animation.animationEnabled == True:
        tile2Animation.animateTile(tile2Animation.rect)

        if tile2Animation.status == "finished disappear":
            sideTile2.clickedTile.nextSoundAnimationImage()
            sideTile2Animation.startAnimation("appear", sideTile2.clickedTile, sideTile2.rect)
    
    # this is only used when tile1Animation is busy and a new tile is clicked
    if tile1AnimationExtra.animationEnabled == True:
        tile1AnimationExtra.animateTile(tile1AnimationExtra.rect)

        if tile1AnimationExtra.status == "finished disappear":
            # loads the first speaker animation image so we dont get errors
            sideTile1.clickedTile.nextSoundAnimationImage()
            sideTile1Animation.startAnimation("appear", sideTile1.clickedTile, sideTile1.rect)
            transferAnimationDataTo(tile1Animation)
    
    # this is only used when tile2Animation is busy and a new tile is clicked
    if tile2AnimationExtra.animationEnabled == True:
        tile2AnimationExtra.animateTile(tile2AnimationExtra.rect)

        if tile2AnimationExtra.status == "finished disappear":
            # loads the first speaker animation image so we dont get errors
            sideTile2.clickedTile.nextSoundAnimationImage()
            sideTile2Animation.startAnimation("appear", sideTile2.clickedTile, sideTile2.rect)
            transferAnimationDataTo(tile2Animation)

    if sideTile1Animation.animationEnabled == True:
        sideTile1Animation.animateSideTile(sideTile1.rect)

        if sideTile1Animation.status == "finished disappear":
            tile1Animation.startAnimation("appear")
            resetSideTile(sideTile1)
        
        elif sideTile1Animation.status == "finished appear":
            music.soundHandler(sideTile1)

        elif sideTile1Animation.status == "finished match":
            resetSideTile(sideTile1)

    if sideTile2Animation.animationEnabled == True:
        sideTile2Animation.animateSideTile(sideTile2.rect)

        if sideTile2Animation.status == "finished disappear":
            tile2Animation.startAnimation("appear")
            resetSideTile(sideTile2)
        
        elif sideTile2Animation.status == "finished appear":
            music.soundHandler(sideTile2)
        
        elif sideTile2Animation.status == "finished match":
            resetSideTile(sideTile2)

def transferAnimationDataTo(transferTo):
    global tile1Animation
    global tile2Animation
    global tile1AnimationExtra
    global tile2AnimationExtra

    if transferTo == tile1Animation:
        del tile1Animation
        tile1Animation = tile1AnimationExtra
        tile1AnimationExtra = animationClass("tile")
    
    # transfer to is equal to tile2animation
    else:
        del tile2Animation
        tile2Animation = tile2AnimationExtra
        tile2AnimationExtra = animationClass("tile")

def resetSideTile(sideTile):
    global tilesMatch
    global enableColors
    global enterPressed

    sideTile.clickedTile.speakerAnimationCounter = 0
    sideTile.clickedTile = None

    if sideTile == sideTile2:
        tilesMatch = False
        enableColors = False
        enterPressed = False

def createAnimations():
    dX = 1/(animationTime*fps)
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

def loadSoundAnimation():
    imageList = []
    files = os.listdir(speakerAnimationFolder)

    for fileName in files:
        imageList.append(speakerAnimationFolder + fileName)
        
    return imageList

def checkIfMatch():
    global tilesMatch
    global tilesLeftOnBoard
    global enableColors

    enableColors = True

    if sideTile1.clickedTile.pairId == sideTile2.clickedTile.pairId:
        tilesMatch = True
        correctSound.play()
        tilesLeftOnBoard -= 2

        sideTile1Animation.startAnimation("match")
        sideTile2Animation.startAnimation("match")

        if tilesLeftOnBoard == 0:
            print("DU VANN!!!")
    
    # the tiles didn't match
    else:
        sideTile1Animation.startAnimation("disappear")
        wrongSound.play()

def displayColors():
    if enableColors == True:
        if tilesMatch == True:
            pygame.draw.rect(screenSurfaceFront, greenTransparent, sideBar)

        else:
            pygame.draw.rect(screenSurfaceFront, redTransparent, sideBar)
        
        screen.blit(screenSurfaceFront, (0, 0))

def scaleBackground():
    background = pygame.image.load(backgroundPath)
    backgroundWidth, backgroundHeight = background.get_size()

    # assume scaling the height will work
    scaleFactor = backgroundHeight/screenHeight

    scaledWidth = math.ceil(backgroundWidth*scaleFactor)
    scaledHeight = math.ceil(backgroundHeight*scaleFactor)

    # check if it worked. If it didn't, use width as dimensioning factor
    if (scaledWidth < screenWidth) or (scaledHeight < screenHeight):
        scaleFactor = screenWidth/backgroundWidth

        scaledWidth = math.ceil(backgroundWidth*scaleFactor)
        scaledHeight = math.ceil(backgroundHeight*scaleFactor)

    scaledBackground = pygame.transform.scale(background, (scaledWidth, scaledHeight))

    x = (screenWidth - scaledWidth)/2
    y = (screenHeight - scaledHeight)/2

    return scaledBackground, (x, y)
    

# global variables
totalTiles, path2Files = calculateTotalTiles()
enterPressed = False
tilesMatch = False
enableColors = False
tilesLeftOnBoard = totalTiles

rows, columns = calculateRowsColumns(totalTiles)
sideTile1, sideTile2 = calculateSideTiles()

tile, board = calculateBoard()
tileMatrix = generateTileMatrix()
assignFiles2Tiles(path2Files)
tileTexture = loadTileTexture()
background, backgroundPosition = scaleBackground()

music = musicClass(backgroundMusic, fadeIn, fadeOut)

tile1Animation = animationClass("tile")
tile2Animation = animationClass("tile")
tile1AnimationExtra = animationClass("tile")
tile2AnimationExtra = animationClass("tile")
sideTile1Animation = animationClass("sideTile")
sideTile2Animation = animationClass("sideTile")
disappearAnimation, appearAnimation = createAnimations()

animateSideTile1Sound = False
animateSideTile2Sound = False
speakerAnimation = loadSoundAnimation()

displaySideTile1 = False
displaySideTile2 = False

while run:
    timer.tick(fps)
    screen.fill(black)
    drawBackgroundElements()
    drawTiles()
    outlineTiles()
    displaySideTileFiles()
    animationHandler()
    displayColors()

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
                if (sideTile2Animation.status == "started appear") or (sideTile2Animation.status == "finished appear"):
                    if enterPressed == False:
                        enterPressed = True
                        checkIfMatch()
                        music.reset()

        # checks for mouse down
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseClick(event, "down")

        # checks for mouse button up
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouseClick(event, "up")

        # checks for music end events
        elif event.type == RESUME_BACKGROUND_SONG:
            music.resumeBackgroundMusic()

        elif event.type == RESTART_BACKGROUND_SONG:   
            music.restartBackgroundMusic()

        elif event.type == MUSIC_CHANNEL_STOPPED:
            if music.tileSound == None:
                music.resumeBackgroundMusic()

    pygame.display.flip()
pygame.quit()