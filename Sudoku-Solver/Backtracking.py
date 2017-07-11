def row_check(objGrid, row, entry):
    for i in range(9):
        if(objGrid[row][i].entry == entry):
            return False
    return True
        
def col_check(objGrid, col, entry):
    for i in range(9):
        if(objGrid[i][col].entry == entry):
            return False
    return True

def block_check(objGrid, row, col, entry):
    for i in range(row - row%3 , row + 3 - row%3):
        for j in range(col - col%3 , col + 3 - col%3):
            if(objGrid[i][j].entry == entry):
                return False
    return True

def safety_check(objGrid, row, col, entry):
    return (row_check(objGrid, row, entry)) & (col_check(objGrid, col, entry)) & (block_check(objGrid, row, col, entry))



def find_next_empty(objGrid):
    for i in range(9):
        for j in range(9):
            if(objGrid[i][j].entry == 0):
                return objGrid[i][j].pos
    return [-1,-1]

def Solver_Backtracking(objGrid):
    position = find_next_empty(objGrid)
    if(position[0] == -1):
        return True
    
    for entry in range(1,10):
        if(safety_check(objGrid, position[0], position[1], entry)):
            objGrid[position[0]][position[1]].updateEntry(entry)
            
            if(Solver_Backtracking(objGrid)):
                return True
            objGrid[position[0]][position[1]].updateEntry(0)
    return False





