def openmap(file): #Reads the map.txt file and returns it as grid
    with open(file, "r") as coords:
        map = [[char for char in line] for line in coords]
        return map

def printmap(map): #Prints the whole map as a string
    oneline = []
    for lines in range(len(map)):
        oneline.append(''.join(map[lines]))
        
    string = ''.join(oneline)
    return string

def victory(): #Reads and returns the "Victory text"
    with open("win.txt", "r") as vict:
        text = vict.readlines()
        return text

def atplace(map, char): #Returns the coordinates of the @ symbol
    place = []
    for y in range(len(map)):
        if char in map[y]:
            place.append(y)
            place.append(map[y].index(char))
            break
    return place