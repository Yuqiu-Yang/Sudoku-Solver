from Backtracking import Solver_Backtracking
from ModifiedBacktracking import Solver_ModifiedBacktracking
from MCMC import Solver_MCMC
from Sudoku_Entity import SudokuEntity
from Sudoku_Entity import SudokuPuzzle
from Sudoku_Entity import EnSudokuEntity
from Sudoku_Entity import EnSudokuPuzzle


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
print_puzzle(puzzle) 


#Backtracking
objectGrid = SudokuPuzzle(SudokuEntity())
objectGrid.initGrid(puzzle)
Solver_Backtracking(objectGrid.grid)
objectGrid.printSelf()

#Modified Backtracking
objectGrid = EnSudokuPuzzle(EnSudokuEntity())
objectGrid.initGrid(puzzle)
Solver_ModifiedBacktracking(objectGrid.grid)
objectGrid.printSelf()

#MCMC
Solver_MCMC(puzzle)













