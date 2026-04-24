import random

class Char:
    def __init__(self, text, color, movingList=[]):
        self.text = text
        self.color = color
        if random.randint(0,1) == 0:
            self.movingList = movingList + movingList[::-1]
        else:
            self.movingList = movingList 
        # self.movingList = movingList + movingList[::-1]
        if self.movingList != []:
            self.isMoving = True
            self.movingListIndex = self.movingList.index(self.text)
        else:
            self.isMoving = False
            self.movingListIndex = 0

    def __repr__(self):
        return f'Char({self.text}, color={self.color}, movingList={self.movingList})'    

    def listMove(self):
        self.text = self.movingList[self.movingListIndex]
        self.movingListIndex += 1
        if self.movingListIndex >= len(self.movingList):
            self.movingListIndex = 0