class Char:
    def __init__(self, text, color, isMoving=False, movingList=[]):
        self.text = text
        self.color = color
        self.isMoving = isMoving
        self.movingList = movingList
        self.movingListIndex = 0

    def __repr__(self):
        return f'Char({self.text})'    

    def listMove(self):
        if not self.isMoving:
            return
        self.text = self.movingList[self.movingListIndex]
        self.movingListIndex += 1
        if self.movingListIndex >= len(self.movingList):
            self.movingListIndex = 0

    def orderedMove(self, shift):
        if not self.isMoving:
            return
        letterCase = ord('a') if self.text.islower() else ord('A')
        alphaIndex = ord(self.text) - letterCase
        self.text = chr((alphaIndex + shift) % 26 + letterCase)