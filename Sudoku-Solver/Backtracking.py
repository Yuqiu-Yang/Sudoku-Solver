from Sudoku_Entity import SudokuEntity
from Sudoku_Entity import SudokuPuzzle

def row_check(objGrid, row, entry):
    #returns true if the row is safe
    for i in range(9):
        if(objGrid[row][i].entry == entry):
            return False
    return True

def col_check(objGrid, col, entry):
    #returns true if the column is safe
    for i in range(9):
        if(objGrid[i][col].entry == entry):
            return False
    return True

def block_check(objGrid, row, col, entry):
    #returns true if the block is safe
    for i in range(row - row%3 , row + 3 - row%3):
        for j in range(col - col%3 , col + 3 - col%3):
            if(objGrid[i][j].entry == entry):
                return False
    return True

def safety_check(objGrid, row, col, entry):
    #returns true if adding the entry is safe
    return (row_check(objGrid, row, entry)) & (col_check(objGrid, col, entry)) & (block_check(objGrid, row, col, entry))



def find_next_empty(objGrid):
    for i in range(9):
        for j in range(9):
            if(objGrid[i][j].entry == 0):
                return objGrid[i][j].pos
    return [-1,-1]

def Solver_Backtracking(puzzle):
    objectGrid = SudokuPuzzle(SudokuEntity())
    objectGrid.initGrid(puzzle)
    position = find_next_empty(objectGrid.grid)
    if(position[0] == -1):
        return True, objectGrid.gridToList()

    for entry in range(1,10):
        if(safety_check(objectGrid.grid, position[0], position[1], entry)):
            objectGrid.grid[position[0]][position[1]].updateEntry(entry)
            solvable, puzzle = Solver_Backtracking(objectGrid.gridToList())
            if(solvable):
                return True, puzzle
            objectGrid.grid[position[0]][position[1]].updateEntry(0)
    return False, puzzle
