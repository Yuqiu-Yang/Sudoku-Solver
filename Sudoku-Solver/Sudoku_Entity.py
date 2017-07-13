import itertools
import sys
from copy import deepcopy
# Define the basic Sudoku Entity Class
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
  
# Define Basic Puzzle Class    
class SudokuPuzzle(object):
    def __init__(self,SukokuEntityType):
        self.grid = [[deepcopy(SukokuEntityType) for i in range(9)] for j in range(9)]
        self.subGrid = []
        # Arranged by row
        for i in range(3):
            for j in range(3):
                temp = list(itertools.product(range(3*i, 3*i +3), range(3*j, 3*j +3)))
                self.subGrid.append(temp)
        del temp
    
    def initGrid(self, puzzle):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].updateEntry(puzzle[i][j])
                self.grid[i][j].updatePosBlock(i,j)
    def output(self, a):
        sys.stdout.write(str(a))
    def printSelf(self,attribute = "entry"):
        for i in range(9):
            for j in range(9):
                cell = getattr(self.grid[i][j],attribute)
                if cell == 0:
                    self.output('.')
                else:
                    self.output(cell)
                if (j + 1) % 3 == 0 and j < 8:
                    self.output(' |')
                if j != 8:
                    self.output(' ')
            self.output('\n')
            if (i + 1) % 3 == 0 and i < 8:
                self.output("- - - + - - - + - - -\n")
    


