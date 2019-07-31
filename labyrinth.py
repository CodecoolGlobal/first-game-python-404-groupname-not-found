import lab
import curses
import pygame
import sys


def main(arg):
    map = lab.openmap("map.txt")
    pCoords = lab.atplace(map)
    gameState = {
        "playerX": pCoords[1],
        "playerY": pCoords[0],
        "map": map,
        "won": False
        }
    if len(arg) >= 2 and arg[1] == "-gui":
        gameGui(gameState)
    else:
        game(gameState)


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
        clock = pygame.time.Clock()
        while running:
            clock.tick(12)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                gameState = move("up", gameState)
            if pressed[pygame.K_DOWN]:
                gameState = move("down", gameState)
            if pressed[pygame.K_LEFT]:
                gameState = move("left", gameState)
            if pressed[pygame.K_RIGHT]:
                gameState = move("right", gameState)
            drawMap(gameState, pygame)

    except Exception as e:
        print(f"Something went wrong..\n{e}")


def game(gameState):
    try:
        screen = curses.initscr()
        curses.cbreak()
        screen.keypad(1)
        curses.noecho()
        key = ''
        screen.addstr(0, 0, lab.printmap(gameState["map"]))
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
            if gameState["won"]:
                text = lab.victory()
                for lines in range(len(text)):
                    screen.addstr(
                                8+lines,
                                (80-len(text[0]))//2, text[lines].rstrip(),
                                curses.A_BLINK+curses.COLOR_BLUE
                                )
            else:
                screen.addstr(0, 0, lab.printmap(gameState["map"]))
            screen.refresh()
    except Exception as e:
        curses.endwin()
        print("Something went wrong!\n%s" % (e))
    curses.endwin()


def drawMap(gameState, pygame):
    map = gameState["map"]
    black = (0, 0, 0)
    display_surface = pygame.display.set_mode(((len(map[0])-1)*15, len(map)*15))
    display_surface.fill((255, 255, 255))
    pygame.draw.rect(display_surface,
                     (255, 0, 0),
                     (15*gameState["playerX"], 15*gameState["playerY"], 15, 15)
                     )
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == "X":
                pygame.draw.rect(display_surface, black, (15*col, 15*row, 15, 15))
            elif map[row][col] == "O":
                pygame.draw.rect(display_surface,
                                 (255, 0, 255), (15 * col, 15 * row, 15, 15)
                                 )
    pygame.display.update()
    return display_surface


if __name__ == "__main__":
    main(sys.argv)
