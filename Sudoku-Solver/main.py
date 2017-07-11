from Backtracking import objGridMaker
from Backtracking import Solver_Backtracking
from misc import print_puzzle
puzzle=[[0,0,0,0,3,4,0,0,0],
      [0,0,0,0,1,0,9,6,0],
      [3,0,0,0,0,7,2,0,0],
      [6,0,0,2,0,0,1,7,0],
      [2,0,4,1,0,0,0,9,0],
      [0,8,0,0,0,0,4,0,2],
      [0,0,0,7,0,0,8,0,0],
      [0,7,0,0,6,0,0,0,0],
      [1,0,3,0,0,0,0,0,0]]



objectGrid = objGridMaker(puzzle)





print_puzzle(puzzle) 
Solver_Backtracking(objectGrid)

for i in range(9):
    for j in range(9):
        puzzle[i][j] = objectGrid[i][j].entry
        
print_puzzle(puzzle)






