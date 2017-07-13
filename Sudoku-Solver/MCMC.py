import math
from Sudoku_Entity import SudokuEntity
from Sudoku_Entity import SudokuPuzzle

class TSudokuEntity(SudokuEntity):
    def __init__(self):
        SudokuEntity.__init__(self)
        self.trialEntry = 0
        self.fixed = False
    def updateFixed(self):
        if(self.entry != 0):
            self.fixed = True
            self.trialEntry = self.entry
    def updateTrial(self, newTrial):
        self.trialEntry = newTrial
    def becomeReal(self):
        self.updateEntry(self.trialEntry)
        self.fixed = True
        
class TSudokuPuzzle(SudokuPuzzle):
    def __init__(self):
        SudokuPuzzle.__init__(self,TSudokuEntity())
        self.cost = math.inf
    def initGrid(self, puzzle):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].updateEntry(puzzle[i][j])
                self.grid[i][j].updatePosBlock(i,j)
                self.grid[i][j].updateFixed()         
    def initSolve(self):
        pass        
    def cost(self):
        pass
    def randomSelect(self):
        pass
    def swap(self):
        pass
        
        
        
        
