import lab
import curses
from copy import deepcopy

def main():
    menumap = lab.openmap("menu.txt")
    pCoords = lab.atplace(menumap)

    gameState = {
        "playerX": pCoords[1],
        "playerY": pCoords[0],
        "map": menumap,
        "won": False,
        "difficulty": "easy"
        }
    
    menu(gameState)
    # game(gameState)


def menu(gameState):
    try:
        menu = curses.initscr()
        curses.cbreak()
        menu.keypad(1)
        curses.noecho()
        key = ''
        menu.addstr(0, 0, lab.printmap(gameState["map"]))
        while key != curses.KEY_END:  # End key ends the program
            key = menu.getch()
            menu.refresh()
            if key == curses.KEY_UP:
                gameState = move("up", gameState)
            elif key == curses.KEY_DOWN:
                gameState = move("down", gameState)
            elif key == curses.KEY_LEFT:
                gameState = move("left", gameState)
            elif key == curses.KEY_RIGHT:
                gameState = move("right", gameState)
            menu.addstr(0, 0, lab.printmap(gameState["map"]))
            menu.refresh()
            
            if gameState["playerY"] == 18 and gameState["playerX"] == 30:
                break
            elif gameState["playerY"] == 18 and gameState["playerX"] == 49:
                curses.endwin()
                startgame(gameState, "hard")
            elif gameState["playerY"] == 12 and gameState["playerX"] == 49:
                curses.endwin()
                startgame(gameState, "easy")
    except Exception as e:
        curses.endwin()
        print(f"Something went wrong!\n {e}")
    curses.endwin()

def startgame(gameState, difficulty):
    map = lab.openmap("map.txt")
    pCoords = lab.atplace(map)
    gameState["map"] = map
    gameState["playerY"] = pCoords[0]
    gameState["playerX"] = pCoords[1]
    gameState["difficulty"] = difficulty
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


def addfogofwar(gameState):
    if gameState["difficulty"] == "hard":
        hardmap = deepcopy(gameState["map"])
        for lines in range(1,79):
            for columns in range(1,24):
                hardmap[columns][lines] = " "
        for x in range(-2,4):
            for y in range(-2,4):
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


def game(gameState):  # display and user input
    try:
        screen = curses.initscr()
        curses.cbreak()
        screen.keypad(1)
        curses.noecho()
        key = ''
        screen.addstr(0, 0, lab.printmap(addfogofwar(gameState)))
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
                screen.addstr(0, 0, lab.printmap(addfogofwar(gameState)))
            # screen.refresh()
    except Exception as e:
        curses.endwin()
        print("Something went wrong!\n%s" % (e))
    curses.endwin()


if __name__ == "__main__":
    main()
