#!/usr/bin/python3

import random, sys, time, math, pygame
from pygame.locals import *

pygame.init()
WINWIDTH = 640  # width of the program's window, in pixels
WINHEIGHT = 480  # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)
QUARTILE_WINWIDTH = int(WINWIDTH / 5)
QUARTILE_WINHEIGHT = int(WINHEIGHT / 5)

FPS = 30  # frames per second to update the screen

GRASSCOLOR = (24, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

MOVERATE = 10  # how fast the player moves
BOUNCERATE = 6  # how fast the player bounces
BOUNCEHEIGHT = 30  # how high the player bounces
MAXHEALTH = 3  # how much health the player starts with

NUMGRASS = 80  # number of grass objects in the active area
LEFT = 'left'
RIGHT = 'right'

POSITION_X = []
POSITION_Y = []

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, SMALLFONT, GRASSIMAGES, L_WARRIOR_IMG, R_WARRIOR_IMG, POMEGRANATE_TREE, TREE_1, TREE_2, POMEGRANATE

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load('resources/gameicon.png'))
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Pomegranate Tree')
    BASICFONT = pygame.font.Font('resources/freesansbold.ttf', 32)
    SMALLFONT = pygame.font.Font('resources/freesansbold.ttf', 23)

    # load the image files
    L_WARRIOR_IMG = pygame.image.load('resources/warrior.png')
    R_WARRIOR_IMG = pygame.transform.flip(L_WARRIOR_IMG, True, False)
    POMEGRANATE_TREE = pygame.image.load('resources/tree_pom.png')
    TREE_1 = pygame.image.load('resources/tree1.png')
    TREE_2 = pygame.image.load('resources/tree2.png')
    POMEGRANATE = pygame.image.load('resources/pomegranate.png')
    GRASSIMAGES = []
    for i in range(1, 5):
        GRASSIMAGES.append(pygame.image.load('resources/grass%s.png' % i))

    while True:
        runGame()

def runGame():
    # set up variables for the start of a new game
    gameOverMode = False  # if the player has lost
    gameOverStartTime = 0  # time the player lost
    winMode = False  # if the player has won

    # create the surfaces to hold game text
    gameOverSurf = BASICFONT.render('Game Over', True, RED)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)

    gameOverSurf2 = BASICFONT.render('(Press "r" to restart.)', True, RED)
    gameOverRect2 = gameOverSurf2.get_rect()
    gameOverRect2.center = (HALF_WINWIDTH, HALF_WINHEIGHT + 30)

    pomeSurf = SMALLFONT.render('You Have Found the Actual Pomegranate Tree', True, RED)
    pomeRect = pomeSurf.get_rect()
    pomeRect.center = (HALF_WINWIDTH, 50)

    hintSurf = BASICFONT.render('Move, Go Find the "DAKI" !', True, GRASSCOLOR)
    hintRect = hintSurf.get_rect()
    hintRect.center = (HALF_WINWIDTH, 100)

    # random position
    position_x = random.randint(0, 640)
    position_y = random.randint(0, 480)

    grassObjs = []  # stores all the grass objects in the game

    # stores the player object:
    playerObj = {'surface': pygame.transform.scale(L_WARRIOR_IMG, (35, 35)),
                 'facing': LEFT,
                 'size': 35,
                 'x': 200,
                 'y': 240,
                 'bounce': 0,
                 'health': MAXHEALTH}

    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False

    # start off with some random grass images on the screen
    for i in range(15):
        grassObjs.append(makeNewGrass(position_x, position_y))
        grassObjs[i]['x'] = random.randint(0, WINWIDTH)
        grassObjs[i]['y'] = random.randint(0, WINHEIGHT)

    while True:  # main game loop

        # add more grass & squirrels if we don't have enough.
        while len(grassObjs) < NUMGRASS:
            grassObjs.append(makeNewGrass(position_x, position_y))

        # draw the background
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(hintSurf, hintRect)
        DISPLAYSURF.blit(POMEGRANATE_TREE, (500, 100))
        DISPLAYSURF.blit(TREE_1, (500, 200))
        DISPLAYSURF.blit(TREE_2, (510, 300))

        # draw all the grass objects on the screen
        for gObj in grassObjs:
            gRect = pygame.Rect((gObj['x'],
                                 gObj['y'],
                                 gObj['width'],
                                 gObj['height']))
            DISPLAYSURF.blit(GRASSIMAGES[gObj['grassImage']], gRect)

        # draw the player

        if not gameOverMode:
            playerObj['rect'] = pygame.Rect((playerObj['x'],
                                             playerObj['y'] - getBounceAmount(playerObj['bounce'], BOUNCERATE,
                                                                              BOUNCEHEIGHT),
                                             playerObj['size'],
                                             playerObj['size']))
            DISPLAYSURF.blit(playerObj['surface'], playerObj['rect'])

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    moveDown = False
                    moveUp = True
                elif event.key in (K_DOWN, K_s):
                    moveUp = False
                    moveDown = True
                elif event.key in (K_LEFT, K_a):
                    moveRight = False
                    moveLeft = True
                    if playerObj['facing'] != LEFT:  # change player image
                        playerObj['surface'] = pygame.transform.scale(R_WARRIOR_IMG,
                                                                      (playerObj['size'], playerObj['size']))
                    playerObj['facing'] = LEFT
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                    if playerObj['facing'] != RIGHT:  # change player image
                        playerObj['surface'] = pygame.transform.scale(L_WARRIOR_IMG,
                                                                      (playerObj['size'], playerObj['size']))
                    playerObj['facing'] = RIGHT
                elif winMode and event.key == K_r:
                    return

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    moveLeft = False
                elif event.key in (K_RIGHT, K_d):
                    moveRight = False
                elif event.key in (K_UP, K_w):
                    moveUp = False
                elif event.key in (K_DOWN, K_s):
                    moveDown = False

                elif event.key == K_ESCAPE:
                    terminate()

        if not gameOverMode:
            # actually move the player
            if moveLeft:
                playerObj['x'] -= 5
                POSITION_X.append(int(playerObj['x']))
            if moveRight:
                playerObj['x'] += 5
                POSITION_X.append(int(playerObj['x']))
            if moveUp:
                playerObj['y'] -= 5
                POSITION_Y.append(int(playerObj['y']))
            if moveDown:
                playerObj['y'] += 5
                POSITION_X.append(int(playerObj['x']))

            if (moveLeft or moveRight or moveUp or moveDown) or playerObj['bounce'] != 0:
                playerObj['bounce'] += 1

            if playerObj['bounce'] > BOUNCERATE:
                playerObj['bounce'] = 0  # reset bounce amount

            if (playerObj['x'] - 450 >= 10 and playerObj['x'] - 450 <= 30) and (playerObj['y'] - 165 <= 5):
                DISPLAYSURF.blit(POMEGRANATE, (490, 150))
                # DISPLAYSURF.blit(pomeSurf, pomeRect)
                pomegranate_introduction()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def getBounceAmount(currentBounce, bounceRate, bounceHeight):
    # Returns the number of pixels to offset based on the bounce.
    # Larger bounceRate means a slower bounce.
    # Larger bounceHeight means a higher bounce.
    # currentBounce will always be less than bounceRate
    return int(math.sin((math.pi / float(bounceRate)) * currentBounce) * bounceHeight)

def getRandomOffCameraPos(camerax, cameray, objWidth, objHeight):
    # create a Rect of the camera view
    cameraRect = pygame.Rect(camerax, cameray, WINWIDTH, WINHEIGHT)
    while True:
        x = random.randint(camerax - WINWIDTH, camerax + (2 * WINWIDTH))
        y = random.randint(cameray - WINHEIGHT, cameray + (2 * WINHEIGHT))
        # create a Rect object with the random coordinates and use colliderect()
        # to make sure the right edge isn't in the camera view.
        objRect = pygame.Rect(x, y, objWidth, objHeight)
        if not objRect.colliderect(cameraRect):
            return x, y

def makeNewGrass(camerax, cameray):
    gr = {}
    gr['grassImage'] = random.randint(0, len(GRASSIMAGES) - 1)
    gr['width'] = GRASSIMAGES[0].get_width()
    gr['height'] = GRASSIMAGES[0].get_height()
    gr['x'], gr['y'] = getRandomOffCameraPos(camerax, cameray, gr['width'], gr['height'])
    gr['rect'] = pygame.Rect((gr['x'], gr['y'], gr['width'], gr['height']))
    return gr

# menu
pygame.mixer.init()

# define colors
red = (205, 55, 0)
green = (107, 142, 35)
blue = (74, 112, 139)
yellow = (204, 153, 0)
grey = (138, 138, 138)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 255, 200)
bright_yellow = (255, 255, 0)
bright_grey = (153, 153, 153)
black = (0, 0, 0)

gameDisplay = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0, 32)

background_introduction = pygame.image.load("resources/background_introduction.jpg").convert()
introduction_text = pygame.image.load("resources/introduction_text.png").convert()
background_menu = pygame.image.load("resources/background_menu.jpg").convert()
background_achievement = pygame.image.load("resources/background_achievement.jpg").convert()

achievement_pomegranate = pygame.image.load("resources/achievement_pomegranate.png").convert_alpha()

# handle_quit()
def quitmenu():
    pygame.quit()
    quit()

def quitfunction():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitmenu()

# background music
def menu_music():
    background_music_ogg = "resources/Hangout.ogg"
    pygame.mixer.music.load(background_music_ogg)
    pygame.mixer.music.play(-1)

def menu_music_pause():
    pygame.mixer.music.pause()

def menu_music_unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False

def pomegranate_music_buttons():
    pomegranate_button("Music", 30, 30, 50, 20, grey, bright_grey, 10, menu_music_unpause)
    pomegranate_button("Pause", 100, 30, 50, 20, grey, bright_grey, 10, menu_music_pause)

# text display
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def pomegranate_text(fontsize, string, a, b):
    Text = pygame.font.SysFont("comicsansms", fontsize)
    TextSurf, TextRect = text_objects(string, Text)
    TextRect.center = (a, b)
    gameDisplay.blit(TextSurf, TextRect)

# button function
def pomegranate_button(msg, x, y, w, h, ic, ac, fontsize, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    pomegranate_text(fontsize, msg, (x + (w / 2)), (y + (h / 2)))

# display introduction, menu, achievement etc.
def pomegranate_introduction():
    introduction = True
    while introduction:
        quitfunction()
        gameDisplay.blit(background_introduction, (0, 0))
        gameDisplay.blit(introduction_text, (60, 130))
        pomegranate_text(50, "Introduction", HALF_WINWIDTH, QUARTILE_WINHEIGHT)

        pomegranate_button("Menu", 460, 240, 130, 50, green, bright_green, 20, pomegranate_menu)
        pomegranate_button("Back", 460, 320, 130, 50, blue, bright_blue, 20, runGame)
        pomegranate_button("Quit", 460, 400, 130, 50, red, bright_red, 20, quitmenu)

        pomegranate_music_buttons()

        pygame.display.update()

def pomegranate_menu():
    menu = True
    while menu:
        quitfunction()
        gameDisplay.blit(background_menu, (0, 0))
        pomegranate_text(50, "Menu", HALF_WINWIDTH, QUARTILE_WINHEIGHT)

        pomegranate_button("Start Game!", 245, 200, 150, 50, green, bright_green, 20, question1)
        pomegranate_button("Achievement", 255, 400, 130, 50, yellow, bright_yellow, 20, achievement)
        pomegranate_button("Quit", 460, 400, 130, 50, red, bright_red, 20, quitmenu)
        pomegranate_button("Introduction", 50, 400, 130, 50, blue, bright_blue, 20, pomegranate_introduction)
        pomegranate_music_buttons()

        pygame.display.update()

def display_pomegranate_image(coordinates):  # display pomegranate image in Achievement
    # @param input coordinates: e.g [(150,220), (350,220)] or [(350,220),]
    for c in coordinates:
        gameDisplay.blit(achievement_pomegranate, c)

def achievement():
    achievement = get()
    menu_achievement = True
    while menu_achievement:
        quitfunction()
        gameDisplay.blit(background_achievement, (0, 0))
        pomegranate_text(50, "Achievement", HALF_WINWIDTH, QUARTILE_WINHEIGHT)

        pomegranate_button("Menu", 460, 320, 130, 50, green, bright_green, 20, pomegranate_menu)
        pomegranate_button("Quit", 460, 400, 130, 50, red, bright_red, 20, quitmenu)
        pomegranate_music_buttons()

        if achievement == 0:
            pomegranate_text(25, "Oops! You have nothing here...", 350, 220)
        elif achievement == 1:
            display_pomegranate_image([(220, 220)])
            pomegranate_text(25, "You have 1 pomegranate!", 320, 180)
        elif achievement == 2:
            display_pomegranate_image([(150, 220), (350, 220)])
            pomegranate_text(25, "Congratulations! You have 2 pomegranates!", 300, 180)
        else:
            print("Achievement value is wrong!")
            quitmenu()

        pygame.display.update()
        
# play music
menu_music()

"""set up for the images and texts"""

# set up the window
SCREEN_SIZE = (640, 480)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
# pictures
game_background = pygame.image.load("resources/game_background.png").convert()  # background image
mouse_cursor = pygame.image.load("resources/warrior.png").convert_alpha()  # mouse cursor
background_win = pygame.image.load("resources/background_win.png").convert()  # background image
background_lose = pygame.image.load("resources/background_lose.png").convert()

font = pygame.font.SysFont("arial", 32)  # front

# texts that will appear on the screen
text_surface_question1 = font.render("Which one is the meaning of 'Addakhat'?", False, (255, 128, 0))  # question1
text_surface_feed = font.render("feed", False, (255, 128, 0))  # choose1 in question1
text_surface_grab = font.render("grab", False, (255, 128, 0))  # choose2 in question1

text_surface_win = font.render("Congratulations! You got it right!", False, (255, 0, 0))  # win_words
text_surface_wrong = font.render("Oops! That's not right.", False, (255, 0, 0))  # loose_words
text_surface_reminder = font.render("Click to go back to menu.", False, (255, 0, 0))

text_surface_question2 = font.render("Which one is the Akkusative form?", False, (255, 128, 0))  # question1
text_surface_dawey = font.render("dawey", False, (255, 128, 0))  # choose1 in question2
text_surface_daweya = font.render("daweya", False, (255, 128, 0))  # choose2 in question2
text_surface_nth = font.render("", False, (0, 0, 0))

text_surface_final1 = font.render("You have won two pomegranates in the game!", False, (255, 0, 0))  # final words win
text_surface_final2 = font.render("You have not enough pomegranates to pass here!", False,
                                  (255, 0, 0))  # final words loose

# sound effects
effect_sound = pygame.mixer.Sound("resources/effect_sound.wav")
lose_sound = pygame.mixer.Sound("resources/lose_sound.wav")
win_sound = pygame.mixer.Sound("resources/win_sound.wav")

def mouse_figure():  # change the mouse cursor to a figure
    x_mouse, y_mouse = pygame.mouse.get_pos()
    pygame.mouse.set_visible(False)
    x_mouse -= mouse_cursor.get_width() / 2
    y_mouse -= mouse_cursor.get_height() / 2
    screen.blit(mouse_cursor, (x_mouse, y_mouse))
    pygame.display.update()

def exit():  # catch the exit move
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def question1():
    global achievement1
    achievement1 = 0  # set the variable to record achievement

    while True:  # the game loop
        # exit option
        exit()
        # the background and texts for question1
        screen.blit(game_background, (0, 0))
        screen.blit(text_surface_question1, (70, 362))
        screen.blit(text_surface_feed, (82, 128))
        screen.blit(text_surface_grab, (466, 128))
        pygame.display.update()
        # change the mouse to figure
        mouse_figure()
        # catch the buttondown move
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                effect_sound.play()
                x_mouse, y_mouse = pygame.mouse.get_pos()

                # if click the right answer
                if x_mouse <= 320 and y_mouse <= 200:
                    # change the background and texts
                    achievement1 += 1
                    question2()
                # if click the wrong answer
                elif x_mouse >= 360 and y_mouse <= 200:
                    achievement1 += 0
                    question2()
                else:
                    question1()

def question2():
    global achievement2
    achievement2 = 0  # set the variable to record achievement
    while True:  # the game loop
        # exit option
        exit()
        # the background and texts for question1
        screen.blit(game_background, (0, 0))
        screen.blit(text_surface_question2, (70, 362))
        screen.blit(text_surface_dawey, (82, 128))
        screen.blit(text_surface_daweya, (466, 128))
        pygame.display.update()
        # change the mouse to figure
        mouse_figure()
        # catch the buttondown move
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                effect_sound.play()
                x_mouse, y_mouse = pygame.mouse.get_pos()
                # if click the right answer
                if x_mouse <= 320 and y_mouse <= 200:
                    # change the background and texts
                    achievement2 += 1
                    final()
                # if click the wrong answer
                elif x_mouse >= 360 and y_mouse <= 200:
                    achievement2 += 0
                    final()
                else:
                    question2()

def get():
    achievement = achievement1 + achievement2
    return achievement

def final():
    while True:
        if get() < 2:
            screen.blit(background_lose, (0, 0))
            screen.blit(text_surface_final2, (70, 362))
            screen.blit(text_surface_nth, (82, 128))
            screen.blit(text_surface_nth, (466, 128))
            pygame.display.update()
            lose_sound.play()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    pygame.mouse.set_visible(True)
                    pomegranate_menu()  # go back the menu

        else:
            screen.blit(background_win, (0, 0))
            screen.blit(text_surface_final1, (70, 362))
            screen.blit(text_surface_nth, (82, 128))
            screen.blit(text_surface_nth, (466, 128))
            win_sound.play()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    pygame.mouse.set_visible(True)
                    quitmenu()  # quit the game

        pygame.display.update()

if __name__ == '__main__':
    main()
