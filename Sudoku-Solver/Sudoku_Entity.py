# Define the basic Sudoku Entity
class SudokuEntity(object):
    def __init__(self):
        self.pos = [-1, -1]
        self.block = 0
        self.entry = 0
    def updateEntry(self, newEntry):
        self.entry = newEntry
    def updatePosBlock(self, row, col):
        self.pos = [row, col]
        self.block = ((row // 3) + 1) + 3 * (col // 3)