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
    
    game(map)

def move(dir, maze): #Moves player character bz 1 tile in the given direction
    global playerY
    global playerX, won
    dir = direction(dir)
    if  maze[playerY+dir[0]][playerX+dir[1]] != 'X':
        maze[playerY][playerX] = ' '
        playerX += dir[1]
        playerY += dir[0]
        if maze[playerY][playerX] == "O":
            won = True
        maze[playerY][playerX]  = '@'        
    return maze

def direction(dir): #Converts direction string to vector 
    if dir == "up":
        return -1,0
    elif dir == "down":
        return 1,0
    elif dir == "left":
        return 0,-1
    elif dir == "right":
        return 0,1
    else:
        return 0,0 


def game(map): #display and user input
    try:
        screen = curses.initscr()
        curses.cbreak() 
        screen.keypad(1)
        curses.noecho()
        key = ''
        screen.addstr(0,0, lab.printmap(map))
        while key != curses.KEY_END: #End key ends the program
            global won
            key = screen.getch()
            if not won:
                screen.refresh()
                if key == curses.KEY_UP:
                    map = move("up",map)
                elif key == curses.KEY_DOWN:
                    map = move("down",map)            
                elif key == curses.KEY_LEFT:
                    map = move("left",map)
                elif key == curses.KEY_RIGHT:
                    map = move("right",map)
                else:
                    pass 
            if won == True:
                text = lab.victory()
                for lines in range(len(text)):
                    screen.addstr(8+lines, (80-len(text[0]))//2, text[lines].rstrip(), curses.A_BLINK+curses.COLOR_BLUE)
            else:
                screen.addstr(0,0, lab.printmap(map))
            screen.refresh()
    except:
        print("Terminal is too small")
    curses.endwin()



if __name__ ==  "__main__":
    main()
