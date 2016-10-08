# Conway's Game of Life in Python
# Author: Andrew Braunlich

from time import sleep
import os
import sys
import curses



#initialize the curses screen
stdscr = curses.initscr()

def main():

    #screen initialization cont'd
    curses.noecho()
    curses.cbreak()

    #read in the file from std input and gather appropriate settings data
    f = sys.stdin.read()
    runData = readFile(f)

    #setup the board and set delay & duration
    board = runData[0]
    delay = runData[1]
    duration = runData[2]

    #For the number of input generations, display, take a step, and sleep
    for i in range(duration):
        disp(board, i)
        board = onestep(board)
        sleep(delay)

    #close curses & clear the screen, printing the final board at the end
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    clearscreen()
    printBoard(board)

#disp(board, gen): a function for displaying the current state of the game
#board- the board that contains the cells
#gen- the current generation
def disp(board, gen):
    #generate the extra data and print it
    countPair = cellCount(board)
    stdscr.addstr(0,0,"Generation: "+str(gen)+"  Dead Cells: "+str(countPair[0])+"  Live Cells: "+str(countPair[1]))
    stdscr.addstr(1,0,"+"+len(board[0])*"-"*3+"+")

    #val represents the current line for curses- the stdscr.addstr calls write
    #to specific coordinates
    val = 2
    for i in range(len(board)):
        temp = "|"
        for j in range(len(board[0])):
            temp+= str(board[i][j])*3
        temp = temp.replace("0"," ").replace("1",u"\u2588")
        stdscr.addstr(val,0,temp+"|")
        val+=1
    stdscr.addstr(val,0,"+"+len(board[0])*"-"*3+"+")

    #update the screen
    stdscr.refresh()

#readFile(filename): reads the contents of the input file and builds the board &
#gathers the extra necessary data
#filename- deprecated name, in reality now contains the actual contents of the file
#because input is now through stdin.
#returns: a tuple containing the board, delay setting, and duration setting
def readFile(filename):
    lines = filename.split("\n")
    duration = eval(lines[0].split()[1])
    delay = eval(lines[1].split()[1])
    x,y = eval(lines[2].split()[1])
    lines = lines[3:]
    board = createBoard(x,y)
    for i in range(len(lines)):
        curr = lines[i]
        for j in range(len(curr)-1):
            board[i][j] = eval(curr[j])
    return (board,delay,duration)

#onestep(board)- takes one step of the game
#board- the board that contains the cells
#creates a hard copy of the board, and executes the rules of the game on each
#cell, updating their values as necessary
#returns: the copy of the board
def onestep(board):
    copy = []
    for i in range(len(board)):
        copy.append([])
        for j in range(len(board[0])):
            copy[i].append(board[i][j])

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]==1:
                copy[i][j]=0
                if bringDeath(board,i,j):
                    copy[i][j]=1
            else:
                copy[i][j]=0
                if createLife(board,i,j):
                    copy[i][j]=1

    return copy


#bringDeath(board,x,y)- determines if a given cell should die
#board- the board that contains the cells
#x,y- the x and y coordinates of the cell
#returns- True if the sum of its neighbors is between 3 and 2 inclusive, False otherwise
def bringDeath(board, x, y):
    sum = neighborSum(board,getNeighbors(x,y,len(board),len(board[0])))
    return not (sum>3 or sum<2)

#createLife(board,x,y)- determines if a given cell should be born
#board- the board that contains the cells
#x,y- the x and y coordinates of the cell
#returns- True if the sum of its neighbors is 3, otherwise False
def createLife(board, x, y):
    sum = neighborSum(board,getNeighbors(x,y,len(board),len(board[0])))
    return sum==3

#neighborSum(board,pairs)
#board- the board that contains the cells
#pair- list of coordinates surrounding a particular cell
#returns- the sum of all surrounding cells
def neighborSum(board, pairs):
    sum = 0
    for pr in pairs:
        sum+=board[pr[0]][pr[1]]
    return sum

#getNeighbors(x,y,width,height)- generates a list of coordinate pairs that surround x,y
#x,y- the x,y coordinates of the board being looked at
#width- the width of the board
#height- the height of the board
def getNeighbors(x, y, width, height):
    yCoords = []
    xCoords = []
    for i in range(3):
        yCoords.append(y-1)
    for i in range(2):
        yCoords.append(y)
    for i in range(3):
        yCoords.append(y+1)
    for i in range(3):
        xCoords.append(x-1)
        if i!=1:
            xCoords.append(x)
        xCoords.append(x+1)

    pairList = []
    #adjust the x, y values as necessary if they exceed board limits
    #create a list of pairs of coords to return
    #range is yCoords because yCoords = xCoords, and a variable loojs nicer than 8
    for i in range(len(yCoords)):
        if yCoords[i]<0:
            yCoords[i]+=height
        if yCoords[i]>height-1:
            yCoords[i]-=height
        if xCoords[i]<0:
            xCoords[i]+=width
        if xCoords[i]>width-1:
            xCoords[i]-=width
        pairList.append((xCoords[i],yCoords[i]))

    return pairList

#cellCount(board)- returns a pair of the # of living cells and dead cells for
# a given game state
#board- the board that contains the cells
def cellCount(board):
    sumDead = 0
    sumLive = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]==0:
                sumDead+=1
            else:
                sumLive+=1
    return (sumDead,sumLive)


#Taken from http://stacjoverflow.com/a/16975035
def clearscreen():
    os.system('cls' if os.name=='nt' else 'clear')



#printBoard(board)- old, unused method for printing the board, not using curses
#board- the board that contains the cells
def printBoard(board):
    countPair = cellCount(board)
    print("Dead Cells: "+str(countPair[0])+"  Live Cells: "+str(countPair[1]))
    print("+"+len(board[0])*"-"*3+"+")
    for i in range(len(board)):
        temp = "|"
        for j in range(len(board[0])):
            temp+= str(board[i][j])*3
        temp = temp.replace("0"," ").replace("1",u"\u2588")
        print(temp+"|")
    print("+"+len(board[0])*"-"*3+"+")

#createBoard(width,height)- creates an empty board of dimensions width and height
#width- the width of the board to be created
#height- the height of the board to be created
def createBoard(width,height):
    board = []
    for i in range(width):
        row = []
        for j in range(height):
            row.append(0)
        board.append(row)
    return board




main()
