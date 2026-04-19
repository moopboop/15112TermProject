from cmu_graphics import *
import string

def onAppStart(app):
#———TEXT VARS———————————————————————————————————————————————————————————————————
    app.currPos = (0,0)
    app.allowedText = set(string.ascii_letters + string.digits)
    app.text = 'EE*'
    # create string of all tpying, make special character for switching directions to make deleting easier
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
    app.world = [([None] * app.worldCols) for row in range(app.worldRows)]
    app.height = 600
    app.width = 1200
    app.rows, app.cols = 23, 55
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.boardLeft = 25
    app.boardTop = 25
    app.boardWidth = app.width - app.boardLeft * 2
    app.boardHeight = app.height - app.boardTop * 2
    app.cellBorderWidth = 0.5

#———OTHER VARS——————————————————————————————————————————————————————————————————
    app.setMaxShapeCount(5000)
    app.inspectorEnabled = False
    app.stepsPerSecond = 30
    app.steps = 0

class Char:
    def __init__(self, text, pos, color='black', isMoving=False):
        self.text = text
        self.pos = pos
        self.color = color
        self.isMoving = isMoving

def redrawAll(app):
    drawRect(0,0,app.width,app.height,fill=rgb(240,240,240))
    drawBoard(app)

def onStep(app):
    app.steps += 1
    if app.steps%10 == 0:
        app.steps = 0
        app.cursorBlink = not app.cursorBlink

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawCell(app, row, col):
    left, top = getCellLeftTop(app, row, col)
    width, height = getCellSize(app)
    
    # for debugging, draws grid on "esc"
    if app.drawGrid:
        drawRect(left, top, width, height, border='black', 
                 borderWidth=app.cellBorderWidth, fill=None) 
    
    if app.board[row][col] != None:
        cx = left + width//2
        cy = top + height//2
        drawLabel(app.board[row][col], cx, cy, size=18, align='bottom', font='monospace')
    elif (row,col) == app.currPos:
        cx = left + width//2
        cy = top + height//2
        angle = findAngleFromDir(app)
        if app.cursorBlink:
            rectColor, cursColor = rgb(50,50,50), rgb(200,200,200)
        else:
            cursColor, rectColor = rgb(50,50,50), rgb(200,200,200)
        drawRect(left, top-(height//3), width, height, fill=rectColor)
        drawLabel('^', cx, cy, size=18, align='bottom', font='monospace', rotateAngle=angle, bold=True, fill=cursColor)

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
        pass
    elif key == 'enter':
        checkDirection(app)
    elif key == 'backspace':
        deleteLastLetter(app)
    elif modifiers + [key] == ['control', 'z']:
        undoDirection(app)
    elif key in app.allowedText:
        addLetter(app, key)

def checkDirection(app):
    prevTwoChars = findLastXLetters(app, 2)
    if prevTwoChars in app.directions:
        app.currDir = prevTwoChars
        app.text += '*'

def findLastXLetters(app, numOfLetters):
    oppositeDirection = findOppositeDirection(app)
    lastXLetters = ''
    currPos = app.currPos
    for _ in range(numOfLetters):
        prevCharRow, prevCharCol = addTuple(currPos, oppositeDirection)
        prevLetter = app.board[prevCharRow][prevCharCol]
        if prevLetter != None:
            lastXLetters = prevLetter + lastXLetters
            currPos = (prevCharRow, prevCharCol)
    print(lastXLetters)    
    return lastXLetters    

def deleteLastLetter(app):
    oppDir = findOppositeDirection(app)
    targetRow, targetCol = addTuple(app.currPos, oppDir)
    if app.board[targetRow][targetCol] != None:
        app.board[targetRow][targetCol] = None
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
        print(app.text)
        print(lastDir)
        print(app.currDir)
    # else, delete up until the '*' 
    else:
        lastDir = app.text.rfind('*')
        lettersToDelete = (len(app.text)-1) - lastDir
        for _ in range(lettersToDelete):
            deleteLastLetter(app)   

def addLetter(app, key):
    currRow, currCol = app.currPos
    targetRow, targetCol = addTuple(app.currPos, app.directions[app.currDir])
    if app.board[targetRow][targetCol] == None:    
        app.board[currRow][currCol] = key
        app.text += key
        app.currPos = targetRow, targetCol

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
    runApp()

main()