from cmu_graphics import *
from char import *
import string

class EnvironmentItem:
    def __init__(self, string, charGroups, charColors, charMovingLists):
        self.string = string
        self.charGroups = charGroups
        self.charColors = charColors
        self.charMovingLists = charMovingLists

        self.item = self.strTo2DList(self.string)

    def strTo2DList(self, str):
        newList = list()
        for line in str.splitlines():
            newListRow = list()
            for c in line:
                if c in string.whitespace:
                    newListRow.append(None)
                else:
                    for charGroupIndex in range(len(self.charGroups)):
                        charGroup = self.charGroups[charGroupIndex]
                        if c in charGroup:
                            color, movingList = self.charColors[charGroupIndex], self.charMovingLists[charGroupIndex]
                            newListRow.append(Char(c, color=color, movingList=movingList))
            newList.append(newListRow)  
        return newList