import lab
import pygame
from copy import deepcopy
import traceback
import time


def main():
    gameState = init()
    gameLoop(gameState)


def init():
    """Initialize setting"""
    try:
        menumap = lab.openmap("menu.txt")
        pCoords = lab.atplace(menumap, '@')

        gameState = {
            "playerX": pCoords[1],
            "playerY": pCoords[0],
            "map": menumap,
            "won": False,
            "difficulty": "easy",
            "menu": True,
            "auto": False
            }
        return gameState
    except Exception as e:
        print(f"initialization failure!\nDetails:{e}")
        exit()


def changeState(gameState, difficulty, level, restart=False):
    """Sets gameState between menu and game level"""
    gameState["map"] = lab.openmap(level)
    pCoords = lab.atplace(gameState["map"], '@')
    gameState["playerY"] = pCoords[0]
    gameState["playerX"] = pCoords[1]
    gameState["difficulty"] = difficulty
    gameState["won"] = False
    if restart:
        gameState["menu"] = True
    else:
        gameState["menu"] = False


def move(dir, gameState):
    """ Moves player character by 1 tile in the given direction """
    maze = gameState["map"]
    playerY = gameState["playerY"]
    playerX = gameState["playerX"]
    dir = direction(dir)
    if maze[playerY+dir[0]][playerX+dir[1]] != 'X':
        maze[playerY][playerX] = ' '
        playerX += dir[1]
        playerY += dir[0]
        if maze[playerY][playerX] == "O":
            gameState["won"] = True
        maze[playerY][playerX] = '@'

    gameState["playerY"] = playerY
    gameState["playerX"] = playerX

    return gameState


def addFogOfWar(gameState):
    """Hides map elements outside of the player's vision range"""
    if gameState["difficulty"] == "hard":
        hardmap = deepcopy(gameState["map"])
        for lines in range(1, 79):
            for columns in range(1, 24):
                hardmap[columns][lines] = " "
        for x in range(-2, 4):
            for y in range(-2, 4):
                try:
                    if gameState["playerY"]-y >= 0: # Without this check it passes negative nums as an index and displays tiles on the bottom of the screen
                        hardmap[gameState["playerY"]-y][gameState["playerX"]-x] = gameState["map"][gameState["playerY"]-y][gameState["playerX"]-x]
                except Exception:
                    pass
        return hardmap
    elif gameState["difficulty"] == "easy" or gameState["difficulty"] == "auto":
        return gameState["map"]


def direction(dir):
    """Converts direction to vector"""
    if dir == "up":
        return -1, 0
    elif dir == "down":
        return 1, 0
    elif dir == "left":
        return 0, -1
    elif dir == "right":
        return 0, 1
    else:
        return 0, 0


def gameLoop(gameState):
    """Main game loop: reading inputs, calling display function"""
    running = True
    lastWon = False
    try:
        pygame.init()
        pygame.font.init()
        clock = pygame.time.Clock()
        while running:
            clock.tick(12)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if gameState["auto"]:
                autoPlay(gameState)
            else:
                pressed = pygame.key.get_pressed()
                if not gameState["won"]:
                    if pressed[pygame.K_UP]:
                        gameState = move("up", gameState)
                    if pressed[pygame.K_DOWN]:
                        gameState = move("down", gameState)
                    if pressed[pygame.K_LEFT]:
                        gameState = move("left", gameState)
                    if pressed[pygame.K_RIGHT]:
                        gameState = move("right", gameState)
                if pressed[pygame.K_SPACE]:
                    changeState(gameState, "easy", "menu.txt", True)
                drawMap(gameState, pygame)

            if not lastWon and gameState["won"]:
                playSound("victory")

            menuOptions(gameState)
            lastWon = gameState["won"]

    except Exception as e:
        print(f"Something went wrong..\n{e}")
        print(traceback.format_exc())


def menuOptions(gameState):
    """Initiates different game states"""
    if gameState["menu"]:
        option = stepOnChar(gameState)
        if option == "exit":
            exit()
        elif option == "hard":
            playSound(option)
            changeState(gameState, "hard", "map.txt")
        elif option == "easy":
            playSound(option)
            changeState(gameState, "easy", "map.txt")
        elif option == "auto":
            gameState["auto"] = True
            playSound(option)
            changeState(gameState, "auto", "map.txt")


def drawMap(gameState, pygame):
    """Converts the map to polygons and renders them on the main window"""
    scale = 20
    font = pygame.font.SysFont("ubuntumono", scale)
    map = addFogOfWar(gameState)
    black = (0, 0, 0)
    display_surface = pygame.display.set_mode(((len(map[0])-1)*scale,
                                              len(map) * scale))
    display_surface.fill((255, 255, 255))

    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == "X":
                pygame.draw.rect(display_surface, black,
                                 (scale*col, scale*row, scale, scale)
                                 )
            elif map[row][col] == "O" and not gameState["menu"]:
                pygame.draw.rect(display_surface,
                                 (255, 0, 255),
                                 (scale * col, scale * row, scale, scale)
                                 )
            elif map[row][col] == "@":
                pygame.draw.rect(display_surface,
                                 (255, 0, 0),
                                 (scale*gameState["playerX"],
                                  scale*gameState["playerY"],
                                  scale,
                                  scale)
                                 )
            else:
                text_surface = font.render(map[row][col], True,  (0, 0, 0))
                display_surface.blit(text_surface, (scale * col, scale * row))
    pygame.display.update()
    pygame.display.flip()


def stepOnChar(gameState):
    """Determines whether the player is on a menu trigger tile"""
    try:
        # qPlace = lab.atplace(gameState["map"], "Q")
        # ePlace = lab.atplace(gameState["map"], 'E')
        # hPlace = lab.atplace(gameState["map"], "H")
        # raise Exception(gameState["playerY"])
        if gameState["playerY"] == 18 and gameState["playerX"] == 30:
            return "exit"
        elif gameState["playerY"] == 12 and gameState["playerX"] == 49:
            return "easy"
        elif gameState["playerY"] == 18 and gameState["playerX"] == 49:
            return "hard"
        elif gameState["playerY"] == 12 and gameState["playerX"] == 30:
            return "auto"
    except Exception:
        print(traceback.format_exc())


def playSound(sound):
    """Plays a soundeffect"""
    # pygame.mixer.pre.init(frequency=44100, size=-16, channels=8, buffer=4096)
    pygame.mixer.init()
    soundLibrary = {}
    soundLibrary["victory"] = pygame.mixer.Sound('tada.wav')
    soundLibrary["easy"] = pygame.mixer.Sound('startlevel.wav') 
    soundLibrary["hard"] = pygame.mixer.Sound('evil.wav')
    soundLibrary["auto"] = pygame.mixer.Sound('startlevel.wav')
    pygame.mixer.Sound.play(soundLibrary[sound], loops=0)


def autoPlay(gameState):
    """Automatic solution from a pre-made textfile"""
    with open("solution.txt", "r") as solution:
        dirlist = solution.readlines()
        for dir in dirlist:
            gameState = move(dir.rstrip(), gameState)
            drawMap(gameState, pygame)
            time.sleep(0.1)
    gameState["auto"] = False


if __name__ == "__main__":
    main()
