import math
import numpy
from copy import deepcopy
from Sudoku_Entity import TSudokuPuzzle

    
def Solver_MCMC(puzzle, t = 10, alpha = 0.999):
    # Initialize the puzzle grid
    objGrid = TSudokuPuzzle()
    objGrid.initGrid(puzzle)
    objGrid.initSolve()
    for i in range(9):
        objGrid.updateRowCost(i)
        objGrid.updateColCost(i)
    objGrid.updateTotCost()
    objGrid.printSelf()
    
    while objGrid.totCost != 0:
        for i in range(9):
            if(objGrid.blockFixed[i]):
                continue
            
            sample1, sample2 = objGrid.randomSelect(i)
            objGrid.swap(sample1,sample2)
  
            objGrid.updateRowCost(sample1[0])
            objGrid.updateRowCost(sample2[0])
            objGrid.updateColCost(sample1[1])
            objGrid.updateColCost(sample2[1])
            tempTotCost = deepcopy(objGrid.totCost)
            objGrid.updateTotCost()
            if(tempTotCost < objGrid.totCost):
                #if the result is worse
                temp = numpy.random.uniform()
                if(temp >= math.exp(-abs(tempTotCost - objGrid.totCost)/t)):
                    # if does not accept
                    objGrid.swap(sample1,sample2)
                    objGrid.updateRowCost(sample1[0])
                    objGrid.updateRowCost(sample2[0])
                    objGrid.updateColCost(sample1[1])
                    objGrid.updateColCost(sample2[1])
                    objGrid.updateTotCost()
        t *= alpha
    objGrid.printSelf("trialEntry")
    
    for i in range(9):
        for j in range(9):
            objGrid.grid[i][j].becomeReal()
    
    objGrid.printSelf()
    
            
    
            

        
        
        
