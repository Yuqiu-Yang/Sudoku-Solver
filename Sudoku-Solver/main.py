from pprint import pprint 
import Backtracking

puzzle=[[0,0,0,0,3,4,0,0,0],
      [0,0,0,0,1,0,9,6,0],
      [3,0,0,0,0,7,2,0,0],
      [6,0,0,2,0,0,1,7,0],
      [2,0,4,1,0,0,0,9,0],
      [0,8,0,0,0,0,4,0,2],
      [0,0,0,7,0,0,8,0,0],
      [0,7,0,0,6,0,0,0,0],
      [1,0,3,0,0,0,0,0,0]]

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
        

objectGrid = [[SudokuEntity() for i in range(9)] for j in range(9)]
for i in range(9):
    for j in range(9):
        objectGrid[i][j].updateEntry(puzzle[i][j])
        objectGrid[i][j].updatePosBlock(i,j)


pprint(puzzle) 
Solver_Backtracking(objectGrid)

for i in range(9):
    for j in range(9):
        puzzle[i][j] = objectGrid[i][j].entry
        
pprint(puzzle)






