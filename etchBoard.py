from cmu_graphics import *
from char import *
import string

goldText = "MARTIN'SMAGIC15112ETCHASKETCHSCREEN"
goldTextSet = set(c for c in goldText)
goldColor = rgb(186, 160, 41)

redTextSet = {'+', '-', '|'}
redColor = rgb(150, 0, 0)

blackColor = rgb(60,60,60)
grayColor = rgb(150,150,150)

def strTo2DList(str):
	newList = list()
	for line in str.splitlines():
		newListRow = list()
		for c in line:
			if c in string.whitespace:
				newListRow.append(None)
			else:
				if c in goldTextSet:
					color = goldColor
				elif c in redTextSet:
					color = redColor
				elif c == 'X':
					color = blackColor
				elif c == '.':
					color = grayColor
				newListRow.append(Char(c, color=color))
		newList.append(newListRow)	
	return newList

etch = '''\
+---------------------------------------------------------------+
|+----------MARTIN'S-MAGIC-15112-ETCH-A-SKETCH-SCREEN----------+|
||+---------MARTIN'S-MAGIC-15112-ETCH-A-SKETCH-SCREEN---------+||
|||+---------------------------------------------------------+|||
|||                                                           |||
|||                                                           |||
|||                                                           |||
|||                                                           |||
|||                                                           |||
|||                                                           |||
|||                                                           |||
|||                                                           |||
|||                                                           |||
|||                                                          ------------
|||                                                          ------------
|||                                                           |||
|||                                                           |||
|||                                                           |||
|||                                                           |||
|||                                                           |||
|||                                                           |||
|||                                                           |||
|||                                                           |||
|||+XXXXXXX-------------------------------------------XXXXXXX+|||
||XX.......XX---------------------------------------XX.......XX||
|X...........X-------------------------------------X...........X|
|X...........X-------------------------------------X...........X|
|X...........X-------------------------------------X...........X|
|+XX.......XX---------------------------------------XX.......XX+|
+---XXXXXXX-------------------------------------------XXXXXXX---+\
'''

newEtch = strTo2DList(etch)
