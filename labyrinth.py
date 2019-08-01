import lab
import curses
import pygame
import sys
from copy import deepcopy
import traceback


def main(arg):
    menumap = lab.openmap("menu.txt")
    pCoords = lab.atplace(menumap, '@')

    gameState = {
        "playerX": pCoords[1],
        "playerY": pCoords[0],
        "map": menumap,
        "won": False,
        "difficulty": "easy",
        "menu": True
        }
    if len(arg) >= 2 and arg[1] == "-gui":
        gameGui(gameState)
    else:
        game(gameState)


def startGame(gameState, difficulty, level, restart=False):
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
    """ Moves player character bz 1 tile in the given direction """
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
    if gameState["difficulty"] == "hard":
        hardmap = deepcopy(gameState["map"])
        for lines in range(1, 79):
            for columns in range(1, 24):
                hardmap[columns][lines] = " "
        for x in range(-2, 4):
            for y in range(-2, 4):
                try:
                    hardmap[gameState["playerY"]-y][gameState["playerX"]-x] = gameState["map"][gameState["playerY"]-y][gameState["playerX"]-x]
                except:
                    pass
        return hardmap
    elif gameState["difficulty"] == "easy":
        return gameState["map"]


def direction(dir):  # Converts direction string to vector
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


def gameGui(gameState):  # display and user input
    running = True
    try:
        pygame.init()
        pygame.font.init()
        clock = pygame.time.Clock()
        while running:
            clock.tick(12)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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
                startGame(gameState, "easy", "menu.txt", True)
            drawMap(gameState, pygame)

            if gameState["menu"]:
                option = stepOnChar(gameState)
                if option == "exit":
                    exit()
                elif option == "hard":
                    startGame(gameState, "hard", "map.txt")
                elif option == "easy":
                    startGame(gameState, "easy", "map.txt")



    except Exception as e:
        print(f"Something went wrong..\n{e}")
        print(traceback.format_exc())


def game(gameState):
    try:
        screen = curses.initscr()
        curses.cbreak()
        screen.keypad(1)
        curses.noecho()
        key = ''
        screen.addstr(0, 0, lab.printmap(addFogOfWar(gameState)))
        while key != curses.KEY_END:  # End key ends the program
            key = screen.getch()
            if not gameState["won"]:
                screen.refresh()
                if key == curses.KEY_UP:
                    gameState = move("up", gameState)
                elif key == curses.KEY_DOWN:
                    gameState = move("down", gameState)
                elif key == curses.KEY_LEFT:
                    gameState = move("left", gameState)
                elif key == curses.KEY_RIGHT:
                    gameState = move("right", gameState)

            if gameState["menu"]:
                option = stepOnChar(gameState)
                if option == "exit":
                    curses.endwin()
                    exit()
                elif option == "hard":
                    curses.endwin()
                    startGame(gameState, "hard", "map.txt")
                elif option == "easy":
                    curses.endwin()
                    startGame(gameState, "easy", "map.txt")

            if gameState["won"]:
                text = lab.victory()
                for lines in range(len(text)):
                    screen.addstr(
                                8+lines,
                                (80-len(text[0]))//2, text[lines].rstrip(),
                                curses.A_BLINK+curses.COLOR_BLUE
                                )
            else:
                screen.addstr(0, 0, lab.printmap(addFogOfWar(gameState)))
            # screen.refresh()
    except Exception as e:
        curses.endwin()
        print("Something went wrong!\n%s" % (e))
    curses.endwin()


def drawMap(gameState, pygame):
    scale = 20
    font = pygame.font.SysFont("ubuntumono", scale)
    map = addFogOfWar(gameState)
    black = (0, 0, 0)
    display_surface = pygame.display.set_mode(((len(map[0])-1)*scale, len(map)*scale))
    display_surface.fill((255, 255, 255))
    pygame.draw.rect(display_surface,
                     (255, 0, 0),
                     (scale*gameState["playerX"], scale*gameState["playerY"], scale, scale)
                     )
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == "X":
                pygame.draw.rect(display_surface, black, (scale*col, scale*row, scale, scale))
            elif map[row][col] == "O" and not gameState["menu"]:
                pygame.draw.rect(display_surface,
                                 (255, 0, 255), (scale * col, scale * row, scale, scale)
                                 )
            elif map[row][col] == "@":
                pass
            else:
                text_surface = font.render(map[row][col], True,  (0, 0, 0) )
                display_surface.blit(text_surface, (scale * col, scale * row))
    pygame.display.update()
    pygame.display.flip()
    #return display_surface


def stepOnChar(gameState):
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
    except:
        print(traceback.format_exc())


if __name__ == "__main__":
    main(sys.argv)
