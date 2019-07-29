import lab
import curses

playerX = 0  
playerY = 0
won = False


def main():
    global playerX
    global playerY
    map = lab.openmap("map.txt")
    pCoords = lab.atplace(map)
    playerX = pCoords[1]
    playerY = pCoords[0]    
    
    gameState = {
        "playerX": pCoords[1],
        "playerY": pCoords[0],
        "map": map,
        "won": False
        }

    game(gameState)


def move(dir, gameState):  # Moves player character bz 1 tile in the given direction
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


def game(gameState):  # display and user input
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
                    screen.addstr(8+lines, (80-len(text[0]))//2, text[lines].rstrip(), curses.A_BLINK+curses.COLOR_BLUE)
            else:
                screen.addstr(0, 0, lab.printmap(gameState["map"]))
            screen.refresh()
    except:
        curses.endwin()
        print("Terminal is too small")
    curses.endwin()


if __name__ == "__main__":
    main()
