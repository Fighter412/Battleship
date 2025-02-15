import turtle
import random

'''

Second redisign of classic game of battleship.

Structure:
Subprograms
Main

'''

# Subprograms

def draw(board):
    largest = 0
    for row in board:
        for item in row:
            if int(item) > largest: largest = int(item)
    #largest = 100
    turtle.tracer(False)
    S = turtle.Screen()
    S.setup(600, 600)
    T = turtle.Turtle()
    T.color("deeppink")
    for i in range(10):
        T.penup()
        T.goto(i*50-235, 260)
        T.pendown()
        T.write(i+1, move=False, align="left", font=("courier", 16, "normal"))
    for i in range(10):
        T.penup()
        T.goto(-280, -i*50+212)
        T.pendown()
        T.write(chr(i+97), move=False, align="left", font=("courier", 16, "normal"))
    T.left(90)
    #turtle.update()
    for i in range(10):
        for j in range(10):
            T.penup()
            T.goto(-250+50*i, 200-50*j)
            T.pendown()
            T.color(convert(int(board[i][j])/largest), convert(int(board[i][j])/largest))
            T.begin_fill()
            for k in range(4):
                T.forward(50)
                T.right(90)
            T.end_fill()

def convert(shade):
    if shade == 1:
        return("#FFFF00")
    elif shade == 0:
        return("#A00000")
    value = int(shade*255)
    hexVal = "#"+format(value, "02X")*3
    return(hexVal)

def find(board, ships_remaining): # Ships_remaining: [5, 0, 0, 3, 2]
    probabilities = [[0 for X in range(10)] for Y in range(10)]
    for ship in range(5):
        for rotation in range(2):
            for row in range(10):
                for square in range(10):
                    if ships_remaining[ship] != 0:
                        if (rotation == 0 and square <= 10-ships_remaining[ship]) or (rotation == 1 and row <= 10-ships_remaining[ship]):
                            possible = True
                            for i in range(ships_remaining[ship]):
                                if rotation == 0:
                                    if board[row][square+i] != "...":
                                        possible = False
                                else:
                                    if board[row+i][square] != "...":
                                        possible = False
                            if possible:
                                for i in range(ships_remaining[ship]):
                                    if rotation == 0:
                                        probabilities[row][square+i] += 1
                                    else:
                                        probabilities[row+i][square] += 1
    for i in range(10):
        for j in range(10):
            if (i+j)%2 == 0:
                probabilities[i][j]=0
    largest = 0
    for row in probabilities:
        for item in row:
            if int(item) > largest: largest = int(item)
    highest = []
    for i in range(10):
        for j in range(10):
            if int(probabilities[i][j]/largest) == 1:
                highest.append([i, j])
    a = highest[random.randint(0, len(highest)-1)]
    return(a)

# Main program

ship = 0
rotation = 0
lastShotHit = False
lengths = [[5, 4, 3, 3, 2]  for i in range(4)] # User, currcomp, prevcomp, aliveships
c1, c2, c3, c4 = "white", "silver", "gray", "deeppink"
tempy = tempx = 10
hits = []
misses = []
shipKilled = False
startPos = [[] for i in range(2)]

def drawBoard(X, Y, board=False, text=""):
    T=turtle.Turtle()
    T.color("white", "dodgerblue")
    T.penup()
    T.goto(X-len(text)/2*13, Y+300)
    T.pendown()
    T.write(text, move=False, align="left", font=("courier", 16, "normal"))
    T.penup()
    T.goto(X-250, Y+250)
    T.pendown()
    T.begin_fill()
    for i in range(4):
        T.forward(500)
        T.right(90)
    T.end_fill()
    for i in range(5):
        T.forward(500)
        T.right(90)
        T.forward(50)
        T.right(90)
        T.forward(500)
        T.left(90)
        T.forward(50)
        T.left(90)
    T.forward(500)
    T.left(90)
    T.forward(500)
    T.left(90)
    T.forward(500)
    T.left(90)
    for i in range(5):
        T.forward(500)
        T.left(90)
        T.forward(50)
        T.left(90)
        T.forward(500)
        T.right(90)
        T.forward(50)
        T.right(90)
    for i in range(10):
        T.penup()
        T.goto(X+i*50-235, Y+260)
        T.pendown()
        T.write(i+1, move=False, align="left", font=("courier", 16, "normal"))
    for i in range(10):
        T.penup()
        T.goto(X-280, Y-i*50+212)
        T.pendown()
        T.write(chr(i+97), move=False, align="left", font=("courier", 16, "normal"))
    T.left(90)
    #turtle.update()
    if board:
        for i in range(len(board)):
            for j in range(len(board[0])):
                shiptype = board[i][j][0]
                rotation = board[i][j][1]
                status = board[i][j][2]
                if shiptype == "0":
                    A2(X-250+50*j, Y+250-50*i, int(rotation))
                elif shiptype == "1":
                    B2(X-250+50*j, Y+250-50*i, int(rotation))
                elif shiptype == "2":
                    C2(X-250+50*j, Y+250-50*i, int(rotation))
                elif shiptype == "3":
                    S2(X-250+50*j, Y+250-50*i, int(rotation))
                elif shiptype == "4":
                    D2(X-250+50*j, Y+250-50*i, int(rotation))
                if status == "X":#shiptype != "." and status == "X":
                    hit(X-250+50*j, Y+250-50*i)
                elif status == "O":
                    miss(X-250+50*j, Y+250-50*i)
        

def drawShip():
    global state, rotation
    T.penup()
    T.goto(0, 125)
    T.pendown()
    T.color("white", "dodgerblue")
    T.begin_fill()
    for i in range(4):
        T.forward(250)
        T.right(90)
    T.end_fill()
    if ship == 0:
        A1(100-25*rotation, 50-25*rotation)
        A2(125*rotation, 125*rotation, rotation)
    elif ship == 1:
        B1(100-25*rotation, 50-25*rotation)
        B2(25+100*rotation, 100*rotation, rotation)
    elif ship == 2:
        C1(100-25*rotation, 50-25*rotation)
        C2(50+75*rotation, 75*rotation, rotation)
    elif ship == 3:
        S1(100-25*rotation, 50-25*rotation)
        S2(50+75*rotation, 75*rotation, rotation)
    elif ship == 4:
        D1(100-25*rotation, 50-25*rotation)
        D2(75+50*rotation, 50*rotation, rotation)
    elif state == 0:
        state = 1
        rotation = -1
        T.penup()
        T.goto(-25, 287.5)
        T.pendown()
        T.color("navy", "navy")
        T.begin_fill()
        for i in range(4):
            T.forward(575)
            T.right(90)
        T.end_fill()
        drawBoard(300, -50, boards[1], "Opponents Board")

def draw(x, y, polygons, r=0):
    for polygon in polygons:
        T.color(polygon[0][0], polygon[0][1])
        T.penup()
        T.goto(x+50*r+polygon[1][0][r], y+(1-2*r)*polygon[1][0][1-r])
        T.pendown()
        T.begin_fill()
        for i in range(len(polygon[1])-1):
            T.goto(x+50*r+polygon[1][i+1][r], y+(1-2*r)*polygon[1][i+1][1-r])
        T.end_fill()
    #turtle.update()
def A1(x, y):
    polygons = [[[c1, c1], [[10, -17.5], [25, -17.5], [25, -22.5], [10, -22.5]]],
                 [[c1, c1], [[10, -27.5], [25, -27.5], [25, -32.5], [10, -32.5]]],
                 [[c1, c1], [[30, -17.5], [40, -25], [30, -32.5]]]]
    draw(x, y, polygons)  
def B1(x, y):
    polygons = [[[c1, c1], [[10, -17.5], [17.5, -17.5], [12.5, -32.5], [10, -32.5]]],
                [[c1, c1], [[22.5, -17.5], [25, -17.5], [20, -32.5], [17.5, -32.5]]],
                [[c1, c1], [[30, -17.5], [40, -25], [30, -32.5], [25, -32.5]]]]
    draw(x, y, polygons)
def C1(x, y):
    polygons = [[[c1, c1], [[11.25, -17.5], [21.25, -17.5], [16.25, -32.5], [11.25, -32.5]]],
                [[c1, c1], [[26.25, -17.5], [29.75, -17.5], [39.75, -25], [29.75, -32.5], [21.25, -32.5]]]]
    draw(x, y, polygons)
def S1(x, y):
    polygons = [[[c1, c1], [[12.5, -17.5], [15, -17.5], [15, -32.5], [12.5, -32.5]]],
                [[c1, c1], [[20, -17.5], [37.5, -25], [20, -32.5]]]]
    draw(x, y, polygons)
def D1(x, y):
    polygons = [[[c1, c1], [[15, -17.5], [35, -25], [15, -32.5]]]]
    draw(x, y, polygons)
def A2(x, y, r):
    polygons = [[[c1, c2], [[40, -12.5], [25, -20], [27.5, -30], [40, -40], [190, -37.5], [200, -35], [225, -32.5], [225, -22.5], [200, -20], [190, -10], [40, -12.5]]],
                [[c1, c3], [[90, -37.5], [140, -36.5], [140, -30.5], [90, -31.5], [90, -37.5]]],
                [[c1, c3], [[30, -20], [189, -12.5]]],
                [[c1, c3], [[30, -30], [197.5, -22.1]]]]
    draw(x, y, polygons, r)
def B2(x, y, r):
    polygons = [[[c1, c2], [[20, -25], [50, -10], [150, -10], [180, -25], [150, -40], [50, -40], [20, -25]]],
                [[c1, c3], [[70, -17.5], [100, -17.5], [115, -25], [100, -32.5], [70, -32.5], [70, -17.5]]]]
    draw(x, y, polygons, r)
    konstants = [0, 77.5, 100]
    if r == 0:
        for k in konstants:
            for i in range(3):
                T.penup()
                T.goto(x+50+k+i*2, y-21-i*2)
                T.pendown()
                T.goto(x+58+k+i*2, y-13-i*2)
            T.penup()
            T.goto(x+42.5+k, y-25)
            T.pendown()
            T.begin_fill()
            T.goto(x+50+k, y-17.5)
            T.goto(x+57.5+k, y-25)
            T.goto(x+50+k, y-32.5)
            T.goto(x+44+k, y-31)
            T.goto(x+42.5+k, y-25)
            T.end_fill()
    else:
        for k in konstants:
            for i in range(3):
                T.penup()
                T.goto(x+29-i*2, y-50-k-i*2)
                T.pendown()
                T.goto(x+37-i*2, y-58-k-i*2)
            T.penup()
            T.goto(x+50-25, y-42.5-k)
            T.pendown()
            T.begin_fill()
            T.goto(x+50-17.5, y-50-k)
            T.goto(x+50-25, y-57.5-k)
            T.goto(x+50-32.5, y-50-k)
            T.goto(x+50-31, y-44-k)
            T.goto(x+50-25, y-42.5-k)
            T.end_fill()
    #turtle.update()
def C2(x, y, r):
    polygons = [[[c1, c2], [[15, -40], [15, -10], [100, -10], [135, -25], [100, -40], [15, -40]]],
                [[c1, c3], [[30, -25], [40, -17.5], [90, -17.5], [105, -25], [90, -32.5], [40, -32.5], [30, -25]]]]
    draw(x, y, polygons, r)
def S2(x, y, r):
    T.penup()
    T.goto(x+120-95*r, y-25-95*r)
    T.color(c2)
    T.dot(30)
    T.goto(x+120-95*r, y-40-95*r)
    T.pendown()
    T.color(c1)
    T.circle(15)
    polygons = [[[c1, c2], [[120, -40], [80, -40], [30, -30], [25, -40], [15, -40], [15, -10], [25, -10], [30, -20], [80, -10], [120, -10]]]]
    draw(x, y, polygons, r)
    T.penup()
    T.goto(x+110-85*r, y-25-85*r)
    T.color(c3)
    T.dot(15)
    T.goto(x+110-85*r, y-32.5-85*r)
    T.pendown()
    T.color(c1)
    T.circle(7.5)
    polygons = [[[c1, c3], [[110, -32.5], [80, -25], [110, -17.5]]]]
    draw(x, y, polygons, r)   
def D2(x, y, r):
    polygons = [[[c1, c2], [[20, -15], [50, -10], [80, -25], [50, -40], [20, -35], [20, -15]]],
                [[c1, c3], [[55, -17.5], [55, -32.5], [30, -25], [55, -17.5]]]]
    draw(x, y, polygons, r)
def hit(x, y):
    polygons = [[[c1, c4], [[5, -37.5], [12.5, -45], [25, -32.5], [37.5, -45], [45, -37.5], [32.5, -25], [45, -12.5], [37.5, -5], [25, -17.5], [12.5, -5], [5, -12.5], [17.5, -25]]]]
    draw(x, y, polygons)
def miss(x, y):
    T.penup()
    T.goto(x+25, y-25)
    T.color(c1, c1)
    T.pendown()
    T.dot(35)

def setupUserBoard():
    T.penup()
    T.goto(-100, 300)
    T.write("BATTLESHIP", move=False, align="left", font=("courier", 25, "normal"))
    drawBoard(-300, -50, text="Your Board")

    T.penup()
    T.goto(350, 60)
    T.pendown()
    T.begin_fill()
    for i in range(2):
        T.forward(200)
        T.right(90)
        T.forward(50)
        T.right(90)
    T.end_fill()
    T.penup()
    T.goto(401, 19)
    T.pendown()
    T.write("Rotate", move=False, align="left", font=("courier", 20, "normal"))

    T.penup()
    T.goto(350, -10)
    T.pendown()
    T.begin_fill()
    for i in range(2):
        T.forward(200)
        T.right(90)
        T.forward(50)
        T.right(90)
    T.end_fill()
    T.penup()
    T.goto(409, -51)
    T.pendown()
    T.write("Place", move=False, align="left", font=("courier", 20, "normal"))

    drawShip()
    turtle.update()
    return([["..." for X in range(10)] for Y in range(10)])

def tempShip(y, x):
    if (rotation == 0 and x+lengths[0][ship] <= 10) or (rotation == 1 and y+lengths[0][ship] <= 10):
        overlapping = False
        if rotation == 0:
            for i in range(lengths[0][ship]):
                if boards[0][y][x+i] != "...":
                    overlapping = True
        else:
            for i in range(lengths[0][ship]):
                if boards[0][y+i][x] != "...":
                    overlapping = True
        if not overlapping:
            board = [[cell for cell in row] for row in boards[0]]
            board[y][x] = "{0}{1}.".format(ship, rotation)
            drawBoard(-300, -50, board)
            global tempy, tempx
            tempy = y
            tempx = x

def placeShip():
    global ship, rotation, tempy, tempx, startPos
    if tempx != 10 and tempy != 10:
        boards[0][tempy][tempx] = "{0}{1}.".format(ship, rotation)
        startPos[1].append([tempx, tempy, rotation])
        for i in range(lengths[0][ship]-1):
            boards[0][tempy+rotation*(i+1)][tempx+(rotation+1)%2*(1+i)] = "{0}..".format(ship+5)
        ship = ship+1
        rotation = 0
        tempy = tempx = 10

def checkShot(X, Y):
    global boards
    global lastShotHit, lastShot, lengths, rotation, state, shipKilled, hits, misses
    gameWon = False
    if boards[1][X][Y][2] == ".":
        if boards[2][X][Y][0] == ".":
            boards[1][X][Y] = boards[1][X][Y][0:2]+"O"
            boards[2][X][Y] = boards[2][X][Y][0:2]+"O"
        else:
            boards[1][X][Y] = boards[1][X][Y][0:2]+"X"
            boards[2][X][Y] = boards[2][X][Y][0:2]+"X"
            lengths[0][int(boards[2][X][Y][0])%5] -= 1 
            if lengths[0][int(boards[2][X][Y][0])%5] == 0:
                shipNumber = int(boards[2][X][Y][0])%5
                startBlock = startPos[0][shipNumber]
                x = startBlock[0]
                y = startBlock[1]
                boards[1][x][y] = boards[2][x][y][0:2]+"X"
        drawBoard(300, -50, boards[1])
        if lengths[0] == [0, 0, 0, 0, 0]:
            win(True)
            gameWon = True
        if not gameWon:
            if (lastShotHit and state == 1) or (state == 2 and not shipKilled):
                state = 2
                shipKilled = False
                X, Y = kill(boards[3], lengths[1], rotation)
            else:
                state = 1
                X, Y = find(boards[3], lengths[1])
            if boards[0][X][Y][0] == ".":
                boards[3][X][Y] = boards[3][X][Y][0:2]+"O"
                boards[0][X][Y] = boards[0][X][Y][0:2]+"O"
                lastShotHit = False
                misses.append([X, Y])
            else:
                boards[3][X][Y] = boards[3][X][Y][0:2]+"X"
                boards[0][X][Y] = boards[0][X][Y][0:2]+"X"
                lengths[1][int(boards[0][X][Y][0])%5] -= 1 
                lastShotHit = True
                hits.append([X, Y])
            for i in range(5):
                if lengths[1][i] == 0 and lengths[2][i] == 1:
                    shipKilled = True
            if shipKilled:
                i = int(boards[0][X][Y][0])%5
                xd = startPos[1][i][1]
                yd = startPos[1][i][0]
                dd = startPos[1][i][2]
                for j in range(lengths[3][i]):
                    hits.remove([xd+j*dd, yd+j*((dd+1)%2)])
                '''T.penup()
                T.goto(-200, -450)
                T.pendown()
                if i == 0:
                    print("Your Aircraft Carrier has been destroyed")
                elif i == 1:
                    print("Your Battleship has been destroyed")
                elif i == 2:
                    print("Your Cruiser has been destroyed")
                elif i == 3:
                    print("Your Submarine has been destroyed")
                elif i == 4:
                    print("Your Destroyer has been destroyed")'''
                state = 1
            for i in range(len(lengths[2])):
                lengths[2][i] = lengths[1][i]
            drawBoard(-300, -50, boards[0])
            if lengths[1] == [0, 0, 0, 0, 0]:
                win(False)

def win(user):
    global registerClick
    registerClick = False
    if user:
        T.penup()
        T.goto(-600, 200)
        T.color("white", "mediumaquamarine")
        T.pendown()
        T.begin_fill()
        for i in range(2):
            T.forward(1200)
            T.right(90)
            T.forward(400)
            T.right(90)
        T.end_fill()
        T.penup()
        T.goto(-425, -60)
        T.pendown()
        T.write("You win! 🎉", move=False, align="left", font=("courier", 100, "normal"))
    else:
        T.penup()
        T.goto(-600, 200)
        T.color("white", "red")
        T.pendown()
        T.begin_fill()
        for i in range(2):
            T.forward(1200)
            T.right(90)
            T.forward(400)
            T.right(90)
        T.end_fill()
        T.penup()
        T.goto(-425, -60)
        T.pendown()
        T.write("Get rekt 😝", move=False, align="left", font=("courier", 100, "normal"))
    turtle.update()

def kill(board, ships_remaining, r):
    global hits, misses, rotation, lastShot
    probabilities = [[0 for X in range(10)] for Y in range(10)]
    for ship in range(len(ships_remaining)):
        for rotation in range(2):
            for row in range(10):
                for square in range(10):
                    valid1 = 0
                    valid2 = True
                    if ships_remaining[ship] != 0:
                        a = lengths[3][ship]
                    else: a = 0
                    for segments in range(a):
                        if row+rotation*segments > 9 or square+((rotation+1)%2)*segments > 9:
                            valid2 = False
                        else:
                            box = [row+rotation*segments, square+(rotation+1)%2*segments]
                            if box in hits:
                                valid1 += 1
                            elif board[box[0]][box[1]] != "..." or ([row, square] in misses):
                                valid2 = False
                    if valid1 == len(hits) and valid2:
                        for segments in range(a):
                            probabilities[row+rotation*segments][square+((rotation+1)%2)*segments] += 1
    for i in hits:
        probabilities[i[0]][i[1]] = 0
    largest = 0
    highest = []
    for row in range(len(probabilities)):
        for item in range(len(probabilities[0])):
            if probabilities[row][item] > largest:
                largest = probabilities[row][item]
    if largest == 0:
        for item in hits:
            if item[0] > 0:
                if ([item[0]-1, item[1]] not in misses) and board[item[0]-1][item[1]] == "...":
                    probabilities[item[0]-1][item[1]] += 1
            if item[0] <9:
                if ([item[0]+1, item[1]] not in misses) and board[item[0]+1][item[1]] == "...":
                    probabilities[item[0]+1][item[1]] += 1
            if item[1] > 0:
                if ([item[0], item[1]-1] not in misses) and board[item[0]][item[1]-1] == "...":
                    probabilities[item[0]][item[1]-1] += 1
            if item[1] < 9:
                if ([item[0], item[1]+1] not in misses) and board[item[0]][item[1]+1] == "...":
                    probabilities[item[0]][item[1]+1] += 1
        largest = 0
        highest = []
        for row in range(len(probabilities)):
            for item in range(len(probabilities[0])):
                if probabilities[row][item] > largest:
                    largest = probabilities[row][item]
    for row in range(len(probabilities)):
        for item in range(len(probabilities[0])):
            if probabilities[row][item] == largest:
                highest.append([row, item])
    a = highest[random.randint(0, len(highest)-1)]
    lastShot = a
    return(a)        

def screenClicked(X, Y):
    global rotation
    if registerClick:
        if state == 0:      # Setting up user board
            if 350 <= X < 550:
                if 10 <= Y < 60:
                    rotation = (rotation + 1)%2
                    drawShip()
                if -60 <= Y < -10:
                    placeShip()
                    drawShip()

            if -550 <= X < -50 and -300 <= Y < 200:
                tempShip(int(9-(Y+300)//50), int((X+550)//50))
        elif state >= 1:    # Normal Gameplay
            if 50 <= X < 550 and -300 <= Y < 200:
                checkShot(int(9-(Y+300)//50), int((X-50)//50))
        turtle.update()


def compGenerateBoard():
    global startPos
    board = [[".." for X in range(10)] for Y in range(10)]
    shipDetails = [5, 4, 3, 3, 2]
    for i in range(5):
        length = shipDetails[i]
        available = False
        while not available:
            available = True
            D = random.randint(0, 1) # 0-Horizontal, 1-Vertical
            if D == 0:
                X = random.randint(0, 9-length+1)
                Y = random.randint(0, 9)
            else:
                X = random.randint(0, 9)
                Y = random.randint(0, 9-length+1)
            for j in range(length):
                if board[Y+j*D][X+j*((D+1)%2)] != "..":
                    available = False
        board[Y][X] = "{0}{1}.".format(i, D)
        startPos[0].append([Y, X, D])
        for j in range(1, length):
            board[Y+j*D][X+j*((D+1)%2)] = "{0}..".format(i+5)
    return(board)


# Main

# Setup turtle

turtle.tracer(False)
S = turtle.Screen()
S.setup(1200, 800)
turtle.bgcolor("navy")
T = turtle.Turtle()
T.color("white", "dodgerblue")
T.hideturtle()

# Setup game
rotation = 0        # 0 - Horizontal, 1 - Vertical
board = compGenerateBoard()
registerClick = True
#for line in board:
#    print(line)
boards = [setupUserBoard(),                                         # User board
          [["..." for X in range(10)] for Y in range(10)],          # User POV of computer
          board,                                      # Computer board
          [["..." for X in range(10)] for Y in range(10)]]          # Computer POV of user
''' ... :
. : .(noship)/0/1/2/3/4(shiptype)/5(shipsegment)
. : .(noship)/0(hrz)/1(vrt)
. : .(noaction)/X(hit)/O(miss)
'''

state = 0

#ship = 0

# Start game

S.onclick(screenClicked)

S.mainloop()
#drawShip()
#drawBoard(300, -50, "Opponents Board")
