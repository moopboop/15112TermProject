from cmu_graphics import *
from charClass import *
from etchBoard import ETCH
from tree import getTree
import string
import random

def onAppStart(app):
#———TEXT VARS———————————————————————————————————————————————————————————————————
    app.localPos = (14,32)
    app.allowedText = set(string.ascii_letters + string.digits)
    app.text = 'EE*'
    app.directionsAndAngles = {'NW':[(-1,-1), 315], 'NN':[(-1, 0),   0], 'NE':[(-1, 1),  45], 
                               'WW':[( 0,-1), 270],                      'EE':[( 0, 1),  90], 
                               'SW':[( 1,-1), 225], 'SS':[( 1, 0), 180], 'SE':[( 1, 1), 135]}
    app.currDir = 'EE' #start by typing to the right
    app.cursorBlink = False
    
#———BOARD VARS——————————————————————————————————————————————————————————————————
    app.drawGrid = False
    app.worldRows, app.worldCols = 1000, 1000
    app.boardDefault = None
    app.world = [([app.boardDefault] * app.worldCols) for row in range(app.worldRows)]
    app.rows, app.cols = 30, 70
    app.topLeftCol = app.topLeftRow = 0
    placeItemsInWorld(app)
    calculateVisibleBoard(app)
    app.boardLeft = 25
    app.boardTop = 25
    app.boardWidth = app.width - app.boardLeft * 2
    app.boardHeight = app.height - app.boardTop * 2
    app.cellBorderWidth = 0.5

#———EXTERNAL VARS———————————————————————————————————————————————————————————————
    # LINES 34-36 ATTRIBUTION: medium.com/codex/how-to-open-view-files-in-python-e77e3e9d3f1d
    app.photoPath = '/Users/martinbaker/Documents/GitHub/15112TermProject/secretImages/'
    app.photos = {'KOZ', 'SAN', 'YUD', 'HAR'}
    app.selectedPhoto = '/Users/martinbaker/Documents/GitHub/15112TermProject/secretImages/KOZ.jpg'
    app.backgroundOpacity = 100

#———SYS VARS————————————————————————————————————————————————————————————————————
    app.setMaxShapeCount(5000)
    app.inspectorEnabled = False
    app.stepsPerSecond = 6
    app.steps = 0

def placeItemsInWorld(app):
    placeTreesInWorld(app)
    placeItemInWorld(app, ETCH, app.topLeftRow, app.topLeftCol)

def placeTreesInWorld(app):
    for row in range(0, app.worldRows-50, 30):
        for col in range(0, app.worldCols-50, 30):
            newRow = row + random.randint(0,20)
            newCol = col + random.randint(0,20)
            tree = getTree(random.randint(1,3))
            if not (newRow < app.rows and newCol < app.cols):
                placeItemInWorld(app, tree, newRow, newCol)

def placeItemInWorld(app, item, worldRow, worldCol, boardReset=False):
    rows, cols = len(item), len(item[0])
    for row in range(rows):
        for col in range(len(item[row])):
            if item[row][col] != None or boardReset:
                insertionRow = row + worldRow
                insertionCol = col + worldCol
                app.world[insertionRow][insertionCol] = item[row][col]

def calculateVisibleBoard(app):
    app.board = []
    for row in range(app.rows):
        rowList = []
        for col in range(app.cols):
            rowList.append(app.world[app.topLeftRow + row][app.topLeftCol + col])
        app.board.append(rowList)

def onStep(app):
    app.steps += 1
    if app.steps % 2 == 0:
        app.cursorBlink = not app.cursorBlink
    if app.backgroundOpacity < 100:
        app.backgroundOpacity += 2

    # after checks, reset after 30 steps (once per sec)
    if app.steps >= 3:
        app.steps = 0
            
def redrawAll(app):
    drawImage(app.selectedPhoto, 0, 0)
    drawRect(0, 0, app.width, app.height, fill=rgb(220,220,220), 
             opacity=app.backgroundOpacity)
    drawBoard(app)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawCell(app, row, col):
    def getCellLeftTop(row, col):
        cellWidth, cellHeight = getCellSize()
        cellLeft = app.boardLeft + col * cellWidth
        cellTop = app.boardTop + row * cellHeight
        return (cellLeft, cellTop)

    def getCellSize():
        cellWidth = app.boardWidth / app.cols
        cellHeight = app.boardHeight / app.rows
        return (cellWidth, cellHeight)    

    left, top = getCellLeftTop(row, col)
    width, height = getCellSize()
    cx, cy = left + width//2, top + height//2
    
    # for debugging grid placement
    if app.drawGrid:
        drawRect(left, top, width, height, border='black', 
                 borderWidth=app.cellBorderWidth, fill=None) 

    if app.board[row][col] != app.boardDefault:
        char = app.board[row][col]
        drawLabel(char.text, cx, cy, size=18, align='bottom', 
                  font='monospace', fill=char.color)
        drawRect(left, top-(height//3), width, height, fill=char.color, opacity=5)
        if char.isMoving:
            char.listMove()
    if (row,col) == app.localPos:
        angle = app.directionsAndAngles[app.currDir][1]
        if app.cursorBlink:
            rectColor, cursColor = rgb(50,50,50), rgb(200,200,200)
        else:
            cursColor, rectColor = rgb(50,50,50), rgb(200,200,200)
        drawRect(left, top-(height//3), width, height, fill=rectColor)
        drawLabel('^', cx, cy, size=18, align='bottom', font='monospace', 
                  rotateAngle=angle, bold=True, fill=cursColor)

def onKeyPress(app, key, modifiers):
    if key == '+' and app.rows < 50:
        app.rows += 1
        app.cols += 1
    elif key == '-' and app.rows > 30:
        app.rows -= 1
        app.cols -= 1
    elif key == 'enter':
        checkDirection(app)
        checkPhoto(app)
        checkShake(app)
    elif key == 'backspace':
        deleteLastLetter(app)
    elif modifiers + [key] == ['control', 'z']:
        undoDirection(app)
    # SPECIAL COMMANDS ONLY FOR DEMO
    elif modifiers + [key] == ['control', '1']:
        app.localPos = (app.rows-1, app.cols-1)
    elif modifiers + [key] == ['shift', 'right']:
        moveCanvas(app, 10, 0, True)   
    elif modifiers + [key] == ['shift', 'down']:
        moveCanvas(app, 0, 10, True)        
    elif modifiers + [key] == ['shift', 'up']:
        moveCanvas(app, 0,-10, True)   
    elif modifiers + [key] == ['shift', 'left']:
        moveCanvas(app,-10, 0, True)
    elif len(key) == 1:
        addLetter(app, key)
    app.board = []    
    calculateVisibleBoard(app)     

def checkDirection(app):
    prevTwoChars = app.text[-2:]
    if prevTwoChars in app.directionsAndAngles:
        app.currDir = prevTwoChars
        app.text += '*'

def checkPhoto(app):
    prevThreeChars = app.text[-3:]
    if prevThreeChars in app.photos:
        app.selectedPhoto = app.photoPath + prevThreeChars + '.jpg'
        app.backgroundOpacity = 26

def checkShake(app):
    prevFiveChars = app.text[-5:]
    if prevFiveChars == 'SHAKE':
        # hard coded to the empty space of the etch board, sorry for magic numbers lol        
        blankSlate = [([None] * 59) for row in range(19)]
        placeItemInWorld(app, blankSlate, 4, 3, boardReset=True)

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

def deleteLastLetter(app):
    def findOppositeDirection():
        dx, dy = app.directionsAndAngles[app.currDir][0]
        return (dx * -1, dy * -1)

    oppDir = findOppositeDirection()
    currRow, currCol = app.localPos
    currRow += app.topLeftRow
    currCol += app.topLeftCol
    targetRow, targetCol = addTuple((currRow, currCol), oppDir)
    if app.world[targetRow][targetCol] != app.boardDefault:
        app.world[targetRow][targetCol] = app.boardDefault
        checkPosition(app, targetRow - app.topLeftRow, targetCol - app.topLeftCol, isForward=False)
        app.text = app.text[:-1]

def addLetter(app, key):
    currRow, currCol = app.localPos
    currRow += app.topLeftRow
    currCol += app.topLeftCol
    targetRow, targetCol = addTuple((currRow, currCol), app.directionsAndAngles[app.currDir][0])
    if (targetRow < 0 or targetRow >= app.worldRows or 
        targetCol < 0 or targetCol >= app.worldCols):
        return
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
        checkPosition(app, targetRow - app.topLeftRow, targetCol - app.topLeftCol)

def checkPosition(app, targetRow, targetCol, isForward=True):
    currRow, currCol = app.localPos
    rowLowBound, rowHighBound = 8, app.rows - 8
    colLowBound, colHighBound = 8, app.cols - 8
    moved = False
    if targetRow <= rowLowBound and app.topLeftRow != 0:
        moved = moveCanvas(app, 0, -1, isForward)
    elif targetRow >= rowHighBound and app.topLeftRow != app.worldRows:
        moved = moveCanvas(app, 0, +1, isForward)
    if targetCol <= colLowBound and app.topLeftCol != 0:
        moved = moveCanvas(app, -1, 0, isForward)
    elif targetCol >= colHighBound and app.topLeftCol != app.worldCols:
        moved = moveCanvas(app, +1, 0, isForward)
    
    app.localPos = addTuple(app.localPos, app.directionsAndAngles[app.currDir][0]) if moved else (targetRow, targetCol)

def moveCanvas(app, dCol, dRow, isForward):
    app.topLeftCol += dCol
    app.topLeftRow += dRow
    # bounds checks
    if app.topLeftCol < 0 or app.topLeftCol > app.worldCols - app.cols:
        app.topLeftCol -= dCol
    elif app.topLeftRow < 0 or app.topLeftRow > app.worldRows - app.rows:
        app.topLeftRow -= dRow
    # handle movement    
    else:
        if isForward:
            app.localPos = addTuple(app.localPos, (-dRow, -dCol)) 
        else:
            app.localPos = addTuple(app.localPos, (dRow, dCol)) 
    return True    

def addTuple(tupOne, tupTwo):
    x1, y1 = tupOne
    x2, y2 = tupTwo
    return (x1 + x2, y1 + y2)
    
def main():
    runApp(width=1280, height=720)

main()