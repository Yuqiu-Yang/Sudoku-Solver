from Sudoku_Entity import SudokuEntity
import itertools
from misc import uniqueEle

class EnSudokuEntity(SudokuEntity):
    def __init__(self):
        SudokuEntity.__init__(self)
        self.candidate = set(range(1,10))
    def trivalCandidate(self):
        if(self.entry != 0):
            self.candidate = set()
    def canToEntry(self):
        if(len(self.candidate) == 1):
            self.updateEntry(self.candidate.pop())
    def eliminateCandidate(self, values):
        self.candidate -= values
        

def moObjGridMaker(puzzle):
    objectGrid = [[EnSudokuEntity() for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            objectGrid[i][j].updateEntry(puzzle[i][j])
            objectGrid[i][j].updatePosBlock(i,j)
            objectGrid[i][j].trivalCandidate()
    return objectGrid


def forwardChecking(objGrid):
    hasNewEntry = False
    # Check Rows
    for i in range(9):
        rowValues = set()
        tempIndex = set(range(9))
        for j in range(9):
             if(objGrid[i][j].entry != 0):
                 rowValues.add(objGrid[i][j].entry)
                 tempIndex -= set(j)
        for j in tempIndex:
            objGrid[i][j].eliminateCandidate(rowValues)
            objGrid[i][j].canToEntry()
            if(objGrid[i][j].entry != 0):
                hasNewEntry = True
            elif(len(objGrid[i][j].candidate) == 0):
                return False, hasNewEntry
                
    # Check Columns
    for j in range(9):
        colValues = set()
        tempIndex = set(range(9))
        for i in range(9):
             if(objGrid[i][j].entry != 0):
                 colValues.add(objGrid[i][j].entry)
                 tempIndex -= set(i)
        for i in tempIndex:
            objGrid[i][j].eliminateCandidate(colValues)
            objGrid[i][j].canToEntry()
            if(objGrid[i][j].entry != 0):
                hasNewEntry = True
            elif(len(objGrid[i][j].candidate) == 0):
                return False, hasNewEntry
    # Check Blocks
    for i in range(3):
        for j in range(3):
            blockValues = set()
            for k in range(3*i, 3*i + 3):
                for l in range(3*j, 3*j + 3):
                    if(objGrid[k][l].entry != 0):
                        blockValues.add(objGrid[k][l].entry)
            for k in range(3*i, 3*i + 3):
                for l in range(3*j, 3*j + 3):
                    if(objGrid[k][l].entry == 0):
                        objGrid[k][l].eliminateCandidate(blockValues)
                        objGrid[k][l].canToEntry()
                        if(objGrid[k][l].entry != 0):
                            hasNewEntry = True
                        elif(len(objGrid[k][l].candidate) == 0):
                            return False, hasNewEntry
    # Check Unique Candidates
    # Row Unique Check
    for i in range(9):
        tempList = []
        tempIndex = set()
        for j in range(9):
            if(objGrid[i][j].entry == 0):
                tempList.extend(list(objGrid[i][j].candidate))
                tempIndex.add(j)
        uniCan = uniqueEle(tempList)
        for j in tempIndex:
            tempSet = (objGrid[i][j].candidate) & uniCan
            if(len(tempSet) != 0):
                objGrid[i][j].updateEntry(tempSet.pop())
                objGrid[i][j].trivalCandidate()
                hasNewEntry = True
    # Column Unique Check
    for j in range(9):
        tempList = []
        tempIndex = set()
        for i in range(9):
            if(objGrid[i][j].entry == 0):
                tempList.extend(list(objGrid[i][j].candidate))
                tempIndex.add(i)
        uniCan = uniqueEle(tempList)
        for i in tempIndex:
            tempSet = (objGrid[i][j].candidate) & uniCan
            if(len(tempSet) != 0):
                objGrid[i][j].updateEntry(tempSet.pop())
                objGrid[i][j].trivalCandidate()
                hasNewEntry = True
    # Block Unique Check
    for i in range(3):
        for j in range(3):
            tempList = []
            for k in range(3*i, 3*i + 3):
                for l in range(3*j, 3*j + 3):
                    if(objGrid[k][l].entry == 0):
                        tempList.extend(list(objGrid[k][l].candidate))
            uniCan = uniqueEle(tempList)
            for k in range(3*i, 3*i + 3):
                for l in range(3*j, 3*j + 3):
                    tempSet = (objGrid[k][l].candidate) & uniCan
                    if(len(tempSet) != 0):
                        objGrid[k][l].updateEntry(tempSet.pop())
                        objGrid[k][l].trivalCandidate()
                        hasNewEntry = True
    return True, hasNewEntry


def lookAhead(objGrid):
    while True:
        solvable, hasNewEntry = forwardChecking(objGrid)
        if not solvable:
            return False
        if not hasNewEntry:
            return True
        
def find_next_empty(objGrid):
    for i in range(9):
        for j in range(9):
            if(objGrid[i][j].entry == 0):
                return objGrid[i][j].pos
    return [-1,-1]

       
def Solver_ModifedBacktracking(objGrid):
    position = find_next_empty(objGrid)
    if(position[0] == -1):
        return True
    
    for entry in objGrid[position[0]][position[1]].candidate:
        
        
        if(Solver_ModifedBacktracking(objGrid)):
            return True
        objGrid[position[0]][position[1]].candidate.eliminateCandidate(set(entry))
        objGrid[position[0]][position[1]].updateEntry(0)
    return False
    
    
    
    

