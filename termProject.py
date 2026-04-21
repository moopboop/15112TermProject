from cmu_graphics import *
import string
import random

def onAppStart(app):
#———TEXT VARS———————————————————————————————————————————————————————————————————
    app.currPos = (14,32)
    app.allowedText = set(string.ascii_letters + string.digits)
    app.text = 'EE*'
    app.directions = {'NW':(-1,-1), 'NN':(-1, 0), 'NE':(-1, 1), 
                      'WW':( 0,-1),               'EE':( 0, 1), 
                      'SW':( 1,-1), 'SS':( 1, 0), 'SE':( 1, 1)}
    app.currDir = 'EE' #start by typing to the right
    app.lastChar = app.secLastChar = None
    app.lastCharPos = app.secLastCharPos = None
    app.cursorBlink = False
    
#———BOARD VARS——————————————————————————————————————————————————————————————————
    app.drawGrid = False
    app.worldRows, app.worldCols = 1000, 1000
    app.boardDefault = None
    app.world = [([app.boardDefault] * app.worldCols) for row in range(app.worldRows)]
    app.rows, app.cols = 30, 65
    app.topLeftCol = app.topLeftRow = 0
    calculateVisibleBoard(app, app.topLeftRow, app.topLeftCol)
    app.boardLeft = 25
    app.boardTop = 25
    app.boardWidth = app.width - app.boardLeft * 2
    app.boardHeight = app.height - app.boardTop * 2
    app.cellBorderWidth = 0.5

#———EXTERNAL VARS———————————————————————————————————————————————————————————————
    # LINES 34-36 ATTRIBUTION: medium.com/codex/how-to-open-view-files-in-python-e77e3e9d3f1d
    app.photoPath = r'/Users/martinbaker/Documents/GitHub/15112TermProject/secretImages/'
    app.photos = {'KOZ', 'SAN', 'YUD', 'HAR'}
    app.selectedPhoto = r'/Users/martinbaker/Documents/GitHub/15112TermProject/secretImages/KOZ.jpg'
    app.backgroundOpacity = 100

#———SYS VARS————————————————————————————————————————————————————————————————————
    app.setMaxShapeCount(5000)
    app.inspectorEnabled = False
    app.stepsPerSecond = 30
    app.steps = 0

class Char:
    def __init__(self, text, color='black', isMoving=False):
        self.text = text
        self.color = color
        self.isMoving = isMoving

    def __repr__(self):
        return f'Char({self.text})'    

    def move(self, shift):
        if not self.isMoving:
            return
        letterCase = ord('a') if self.text.islower() else ord('A')
        alphaIndex = ord(self.text) - letterCase
        self.text = chr((alphaIndex + shift) % 26 + letterCase)

def calculateVisibleBoard(app, rowOffset, colOffset):
    app.board = []
    for i in range(app.rows):
        rowList = []
        for j in range(app.cols):
            rowList.append(app.world[rowOffset + i][colOffset + j])
        app.board.append(rowList)    

def redrawAll(app):
    drawImage(app.selectedPhoto, 0, 0)
    drawRect(0, 0, app.width, app.height, fill=rgb(240,240,240), 
             opacity=app.backgroundOpacity)
    drawBoard(app)

def onStep(app):
    app.steps += 1
    if app.steps % (app.stepsPerSecond//3) == 0:
        app.cursorBlink = not app.cursorBlink
    if app.backgroundOpacity < 100:
        app.backgroundOpacity += 2

    # after checks, reset after 30 steps (once per sec)
    if app.steps >= 30:
        app.steps = 0
            
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawCell(app, row, col):
    left, top = getCellLeftTop(app, row, col)
    width, height = getCellSize(app)
    cx, cy = left + width//2, top + height//2
    
    # for debugging grid placement
    if app.drawGrid:
        drawRect(left, top, width, height, border='black', 
                 borderWidth=app.cellBorderWidth, fill=None) 

    if app.board[row][col] != app.boardDefault:
        char = app.board[row][col]
        drawLabel(char.text, cx, cy, size=18, align='bottom', 
                  font='monospace', fill=char.color)
        if char.isMoving and app.steps % 3 == 0:
            char.move(5)
    if (row,col) == app.currPos:
        angle = findAngleFromDir(app)
        if app.cursorBlink:
            rectColor, cursColor = rgb(50,50,50), rgb(200,200,200)
        else:
            cursColor, rectColor = rgb(50,50,50), rgb(200,200,200)
        drawRect(left, top-(height//3), width, height, fill=rectColor)
        drawLabel(app.currPos, cx, cy+25, font='monospace')
        drawLabel('^', cx, cy, size=18, align='bottom', font='monospace', 
                  rotateAngle=angle, bold=True, fill=cursColor)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)    

def onKeyPress(app, key, modifiers):
    if key == 'escape':
        # app.drawGrid = not app.drawGrid
        # print(app.text)
        print(f'{app.currPos=}')
        print(f'{app.topLeftRow=}, {app.topLeftCol=}')
        print(f'{app.text=}')
        pass
    # RLUD here for debugging
    elif key == 'right':
        moveCanvas(app, +1, 0)
    elif key == 'left':
        moveCanvas(app, -1, 0)
    elif key == 'up':
        moveCanvas(app, 0,-1)         
    elif key == 'down':
        moveCanvas(app, 0,+1)
    elif key == 'enter':
        checkDirection(app)
        checkPhoto(app)
    elif key == 'backspace':
        deleteLastLetter(app)
    elif modifiers + [key] == ['control', 'z']:
        undoDirection(app)
    # elif key in app.allowedText:
    elif len(key) == 1:
        addLetter(app, key)
    calculateVisibleBoard(app, app.topLeftRow, app.topLeftCol)     

def checkDirection(app):
    # prevTwoChars = findLastXLetters(app, 2)
    prevTwoChars = app.text[-2:]
    if prevTwoChars in app.directions:
        app.currDir = prevTwoChars
        app.text += '*'

def checkPhoto(app):
    prevThreeChars = app.text[-3:]
    if prevThreeChars in app.photos:
        app.selectedPhoto = app.photoPath + prevThreeChars + '.jpg'
        app.backgroundOpacity = 26

## older function of finding previous chars before i had app.text
# def findLastXLetters(app, numOfLetters):
    # oppositeDirection = findOppositeDirection(app)
    # lastXLetters = ''
    # currPos = app.currPos
    # for _ in range(numOfLetters):
    #     prevCharRow, prevCharCol = addTuple(currPos, oppositeDirection)
    #     prevLetter = app.board[prevCharRow][prevCharCol].text
    #     if prevLetter != app.boardDefault:
    #         lastXLetters = prevLetter + lastXLetters
    #         currPos = (prevCharRow, prevCharCol)
    # return lastXLetters    

def deleteLastLetter(app):
    oppDir = findOppositeDirection(app)
    targetRow, targetCol = addTuple(app.currPos, oppDir)
    if app.world[targetRow][targetCol] != app.boardDefault:
        app.world[targetRow][targetCol] = app.boardDefault
        app.currPos = (targetRow, targetCol)
        app.text = app.text[:-1]

def undoDirection(app):
    # '*' is included in text to make it easier to find the last direction change
    # text starts as 'EE*' for easier tracking of starting point, dont delete that!!
    if app.text == 'EE*':
        return
    # if most recent character is '*', change directions immediately
    if app.text[-1] == '*':
        app.text = app.text[:-1]
        lastDir = app.text.rfind('*')
        app.currDir = app.text[lastDir - 2 : lastDir]
    # else, delete up until the '*' 
    else:
        lastDir = app.text.rfind('*')
        lettersToDelete = (len(app.text)-1) - lastDir
        for _ in range(lettersToDelete):
            deleteLastLetter(app)   

def addLetter(app, key):
    currRow, currCol = app.currPos
    currRow += app.topLeftRow
    currCol += app.topLeftCol
    targetRow, targetCol = addTuple(app.currPos, app.directions[app.currDir])
    if app.world[targetRow][targetCol] == app.boardDefault:   
        if key.isdigit():
            red = random.randint(0,255)
            green = random.randint(0,255)
            blue = random.randint(0,255)
            color = rgb(red, green, blue)
        else:
            hue = random.randint(10,40)
            color = rgb(hue, hue, hue)             
        app.world[currRow][currCol] = Char(key, color=color)
        app.text += key
        app.currPos = (targetRow, targetCol)
        # checkPosition(app, targetRow, targetCol)

def checkPosition(app, targetRow, targetCol):
    currRow, currCol = app.currPos
    rowLowBound, rowHighBound = 5, app.rows - 5
    colLowBound, colHighBound = 5, app.cols - 5
    # print(app.currPos)
    # print(f'{newRow=}, {rowLowBound=}, {rowHighBound=}')
    # print(f'{newCol=}, {colHighBound=}, {colHighBound=}')
    if targetRow <= rowLowBound:
        moveCanvas(app, 0, +1)
    elif targetRow >= rowHighBound:
        moveCanvas(app, 0, -1)
    elif targetCol <= colLowBound:
        moveCanvas(app, -1, 0)
    elif targetCol >= colHighBound:
        moveCanvas(app, +1, 0)
    else:
        app.currPos = (targetRow, targetCol)            

def moveCanvas(app, dCol, dRow):
    app.topLeftCol += dCol
    app.topLeftRow += dRow
    if app.topLeftCol < 0 or app.topLeftCol > app.worldCols - app.cols:
        app.topLeftCol -= dCol
    elif app.topLeftRow < 0 or app.topLeftRow > app.worldRows - app.rows:
        app.topLeftRow -= dRow
    else:
        app.currPos = addTuple(app.currPos, (-dRow, -dCol)) 

def addTuple(tupOne, tupTwo):
    x1, y1 = tupOne
    x2, y2 = tupTwo
    return (x1 + x2, y1 + y2)
    
def findOppositeDirection(app):
    dx, dy = app.directions[app.currDir]
    return (dx * -1, dy * -1)
    
def findAngleFromDir(app):
    if   app.currDir == 'NN':    return 0
    elif app.currDir == 'NE':    return 45
    elif app.currDir == 'EE':    return 90
    elif app.currDir == 'SE':    return 135
    elif app.currDir == 'SS':    return 180
    elif app.currDir == 'SW':    return 225
    elif app.currDir == 'WW':    return 270           
    elif app.currDir == 'NW':    return 315
    
def main():
    runApp(width=1280, height=720)

main()