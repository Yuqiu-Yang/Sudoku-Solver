from Backtracking import objGridMaker
from Backtracking import Solver_Backtracking
from misc import print_puzzle
puzzle=  [[3,2,0,4,6,0,5,0,0],
          [0,0,5,0,0,0,0,3,6],
          [7,0,0,3,0,0,2,1,0],
          [6,0,0,1,0,4,8,9,5],
          [9,0,0,5,2,7,0,6,1],
          [1,0,3,9,8,0,7,4,2],
          [0,4,0,8,0,0,6,0,0],
          [5,3,1,0,9,2,4,8,7],
          [8,9,0,7,0,0,1,2,3]]



objectGrid = objGridMaker(puzzle)

print_puzzle(puzzle) 
Solver_Backtracking(objectGrid)

for i in range(9):
    for j in range(9):
        puzzle[i][j] = objectGrid[i][j].entry
        
print_puzzle(objectGrid)






