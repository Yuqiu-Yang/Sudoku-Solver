import itertools
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
        self.grid = [[SukokuEntityType for i in range(9)] for j in range(9)]
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
    
    
    
