# Conway's Game of Life in Python
# Author: Andrew Braunlich

from time import sleep
import os
import sys
import curses

f = input("filename: ")

stdscr = curses.initscr()

def main():
    #x = width
    #y = height


    curses.noecho()
    curses.cbreak()


    runData = readFile(f)
    board = runData[0]
    delay = runData[1]
    duration = runData[2]
    for i in range(duration):
        #clearscreen()
        disp(board, i)
        board = onestep(board)
        sleep(delay)
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    clearscreen()
    printBoard(board)

def disp(board, gen):
    countPair = cellCount(board)
    stdscr.addstr(0,0,"Generation: "+str(gen)+"  Dead Cells: "+str(countPair[0])+"  Live Cells: "+str(countPair[1]))
    stdscr.addstr(1,0,"+"+len(board[0])*"-"*3+"+")
    val = 2
    for i in range(len(board)):
        temp = "|"
        for j in range(len(board[0])):
            temp+= str(board[i][j])*3
        temp = temp.replace("0"," ").replace("1",u"\u2588")
    #    temp = temp.replace("1",u"\u2588")
        stdscr.addstr(val,0,temp+"|")
        val+=1
    stdscr.addstr(val,0,"+"+len(board[0])*"-"*3+"+")
    stdscr.refresh()

def readFile(filename):
    inp = open(filename,"r")
    lines = inp.readlines()
    duration = eval(lines[0].split()[1])
    delay = eval(lines[1].split()[1])
    x,y = eval(lines[2].split()[1])
    lines = lines[3:]
    print(lines)
    board = createBoard(x,y)
    for i in range(len(lines)):
        curr = lines[i]
        for j in range(len(curr)-1):
            board[i][j] = eval(curr[j])
    return (board,delay,duration)


def onestep(board):
    copy = []
    for i in range(len(board)):
        copy.append([])
        for j in range(len(board[0])):
            copy[i].append(board[i][j])

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]==1:
                test = bringDeath(board,i,j)
                if test:
                    copy[i][j]=1
                else:
                    copy[i][j]=0
            else:
                test = createLife(board,i,j)
                if test:
                    copy[i][j]=1
                else:
                    copy[i][j]=0
    return copy

#determine which cells to jill
def bringDeath(board, x, y):
    sum = neighborSum(board,getNeighbors(x,y,len(board),len(board[0])))
    return not (sum>3 or sum<2)

#determine which cells to create
def createLife(board, x, y):
    sum = neighborSum(board,getNeighbors(x,y,len(board),len(board[0])))
    return sum==3

#get the sum of all neighbor cells
def neighborSum(board, pairs):
    sum = 0
    for pr in pairs:
        sum+=board[pr[0]][pr[1]]
    return sum

#get a list of all cells which are neighbors to the current cell being loojed at
def getNeighbors(x, y, width, height):
    yCoords = []
    xCoords = []
    #create two lists of what the surrounding x, y values should be
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


#Tajen from http://stacjoverflow.com/a/16975035
def clearscreen():
    os.system('cls' if os.name=='nt' else 'clear')




def printBoard(board):
    countPair = cellCount(board)
    bigstr = ""
    bigstr+= "Dead Cells: "+str(countPair[0])+"  Live Cells: "+str(countPair[1])+"\n"
    bigstr+="+"+len(board[0])*"-"*3+"+\n"
    for i in range(len(board)):
        temp = "|"
        for j in range(len(board[0])):
            temp+= str(board[i][j])*3
        temp = temp.replace("0"," ").replace("1",u"\u2588")
    #    temp = temp.replace("1",u"\u2588")
        bigstr+=temp+"|\n"
    bigstr+="+"+len(board[0])*"-"*3+"+\n"
    print(bigstr,end="\r")



def printBoard2(board):
    countPair = cellCount(board)
    print("Dead Cells: "+str(countPair[0])+"  Live Cells: "+str(countPair[1]))
    print("+"+len(board[0])*"-"*3+"+")
    for i in range(len(board)):
        temp = "|"
        for j in range(len(board[0])):
            temp+= str(board[i][j])*3
        temp = temp.replace("0"," ").replace("1",u"\u2588")
    #    temp = temp.replace("1",u"\u2588")
        print(temp+"|")
    print("+"+len(board[0])*"-"*3+"+")


def createBoard(x,y):
    board = []
    for i in range(x):
        row = []
        for j in range(y):
            row.append(0)
        board.append(row)
    return board

main()
