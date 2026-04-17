from cmu_graphics import *

def onAppStart(app):
#———TEXT VARS———————————————————————————————————————————————————————————————————
    app.currPos = (0,0)
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
    app.rows, app.cols = 40, 110
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.boardLeft = 25
    app.boardTop = 25
    app.boardWidth = app.width - app.boardLeft * 2
    app.boardHeight = app.height - app.boardTop * 2
    app.cellBorderWidth = 0.5

#———OTHER VARS——————————————————————————————————————————————————————————————————
    app.setMaxShapeCount(5000)
    app.stepsPerSecond = 30
    app.steps = 0

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
        drawLabel(app.board[row][col], cx, cy, size=12, align='bottom', font='monospace')
    elif (row,col) == app.currPos:
        cx = left + width//2
        cy = top + height//2
        angle = findAngleFromDir(app)
        if app.cursorBlink:
            rectColor, cursColor = rgb(50,50,50), rgb(200,200,200)
        else:
            cursColor, rectColor = rgb(50,50,50), rgb(200,200,200)
        drawRect(left, top-(height//3), width, height, fill=rectColor)
        drawLabel('^', cx, cy, size=12, align='bottom', font='monospace', rotateAngle=angle, bold=True, fill=cursColor)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)    

def onKeyPress(app, key):
    if   key == 'escape':
        app.drawGrid = not app.drawGrid
    elif key == 'enter':
        checkDirection(app)
    elif key == 'backspace':
        # delete recent letter
        pass
    elif len(key) == 1:
        currRow, currCol = app.currPos
        app.board[currRow][currCol] = key
        app.currPos = addTuple(app.currPos, app.directions[app.currDir])

def checkDirection(app):
    oppositeDirection = findOppositeDirection(app.directions[app.currDir])
    prevCharRow, prevCharCol = addTuple(app.currPos, oppositeDirection)
    prevPrevCharRow, prevPrevCharCol = addTuple((prevCharRow, prevCharCol), oppositeDirection)
    # if prevChar not in app.board or prevPrevChar not in app.board:
    #     return

    prevTwoChars = app.board[prevPrevCharRow][prevPrevCharCol] + app.board[prevCharRow][prevCharCol]
    print(prevTwoChars)
    if prevTwoChars in app.directions:
        app.currDir = prevTwoChars


def addTuple(tupOne, tupTwo):
    x1, y1 = tupOne
    x2, y2 = tupTwo
    return (x1 + x2, y1 + y2)
    
def findOppositeDirection(dir):
    dx, dy = dir
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