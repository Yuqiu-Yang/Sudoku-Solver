from pprint import pprint 

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

def Solver(objGrid):
    position = find_next_empty(objGrid)
    if(position[0] == -1):
        return True
    
    for entry in range(1,10):
        if(safety_check(objGrid, position[0], position[1], entry)):
            objGrid[position[0]][position[1]].updateEntry(entry)
            
            if(Solver(objGrid)):
                return True
            objGrid[position[0]][position[1]].updateEntry(0)
    return False


pprint(puzzle) 


Solver(objectGrid)

for i in range(9):
    for j in range(9):
        puzzle[i][j] = objectGrid[i][j].entry
        
pprint(puzzle)
