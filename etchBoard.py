from environmentItemClass import *

etchStr = '''\
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

goldTextChars = set(c for c in "MARTIN'SMAGIC15112ETCHASKETCHSCREEN")
goldColor = rgb(173, 130, 0)

redTextChars = {'+', '-', '|'}
redColor = rgb(150, 0, 0)

salmonTextChars = {'X', '.'}
salmonColor = rgb(184, 176, 152)
# blackColor = rgb(60,60,60)
# grayColor = rgb(150,150,150)

ETCH = EnvironmentItem(etchStr, [goldTextChars, redTextChars, salmonTextChars], 
					  [goldColor, redColor, salmonColor], [[], [], []]).item
