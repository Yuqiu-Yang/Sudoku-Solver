import math
import numpy
from copy import deepcopy
from Sudoku_Entity import TSudokuPuzzle


def Solver_MCMC(puzzle, t = 10, alpha = 0.999, n_attempt = 20, n_iter = 50000):
    n_att = 1
    solvable = False
    while (n_att <= n_attempt) and (not solvable):
        # Initialize the puzzle grid
        objGrid = TSudokuPuzzle()
        objGrid.initGrid(puzzle)
        objGrid.initSolve()
        for i in range(9):
            objGrid.updateRowCost(i)
            objGrid.updateColCost(i)
        objGrid.updateTotCost()

        t1 = t
        a = alpha
        n_i = 0
        while (objGrid.totCost != 0) and (n_i <= n_iter):
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
                    thresh = math.exp(-abs(tempTotCost - objGrid.totCost)/t1)
                    if(temp >= thresh):
                        # if does not accept
                        objGrid.swap(sample1,sample2)
                        objGrid.updateRowCost(sample1[0])
                        objGrid.updateRowCost(sample2[0])
                        objGrid.updateColCost(sample1[1])
                        objGrid.updateColCost(sample2[1])
                        objGrid.updateTotCost()
            t1 *= a
            n_i += 1
            # print(str(n_i)+ " " + str(objGrid.totCost))
            solvable = (objGrid.totCost == 0)
        if not solvable:
            n_att += 1
            print("MCMC Chain " + str(n_att))

    if solvable:
        for i in range(9):
            for j in range(9):
                objGrid.grid[i][j].becomeReal()
        return solvable, objGrid.gridToList()
    else:
        return solvable, puzzle
