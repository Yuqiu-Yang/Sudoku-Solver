from misc import uniqueEle
def forwardChecking(objGrid):
    hasNewInfo = False
    # Check Rows
    for i in range(9):
        rowValues = set()
        tempIndex = set(range(9))
        for j in range(9):
             if(objGrid[i][j].entry != 0):
                 rowValues.add(objGrid[i][j].entry)
                 tempIndex.discard(j)
        for j in tempIndex:
            if(len((objGrid[i][j].candidate) & rowValues)!= 0):
                hasNewInfo = True
            objGrid[i][j].eliminateCandidate(rowValues)
            objGrid[i][j].canToEntry()
            if((len(objGrid[i][j].candidate) == 0)& (objGrid[i][j].entry == 0)):
                return objGrid, False, hasNewInfo

    # Check Columns
    for j in range(9):
        colValues = set()
        tempIndex = set(range(9))
        for i in range(9):
             if(objGrid[i][j].entry != 0):
                 colValues.add(objGrid[i][j].entry)
                 tempIndex.discard(i)
        for i in tempIndex:
            if(len((objGrid[i][j].candidate) & rowValues)!= 0):
                hasNewInfo = True
            objGrid[i][j].eliminateCandidate(colValues)
            objGrid[i][j].canToEntry()
            if((len(objGrid[i][j].candidate) == 0)& (objGrid[i][j].entry == 0)):
                return objGrid, False, hasNewInfo
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
                        if(len((objGrid[i][j].candidate) & rowValues)!= 0):
                            hasNewInfo = True
                        objGrid[k][l].eliminateCandidate(blockValues)
                        objGrid[k][l].canToEntry()
                        if((len(objGrid[i][j].candidate) == 0)& (objGrid[i][j].entry == 0)):
                            return objGrid, False, hasNewInfo
    return objGrid, True, hasNewInfo


def uniqueCheck(objGrid):
    hasNewInfo = True
    hasNewEntry = False
    solvable = True
    while hasNewInfo:
        objGrid, solvable, hasNewInfo = forwardChecking(objGrid)
        if not solvable:
            return objGrid, solvable, hasNewEntry

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
            if(len(tempSet) == 1):
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
            if(len(tempSet) == 1):
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
                    if(len(tempSet) == 1):
                        objGrid[k][l].updateEntry(tempSet.pop())
                        objGrid[k][l].trivalCandidate()
                        hasNewEntry = True
    return objGrid, solvable, hasNewEntry



def lookAhead(objGrid):
    hasNewEntry = True
    while hasNewEntry:
        objGrid, solvable, hasNewEntry = uniqueCheck(objGrid)
        if not solvable:
            return objGrid, solvable


def find_next_empty(objGrid):
    for i in range(9):
        for j in range(9):
            if(objGrid[i][j].entry == 0):
                return objGrid[i][j].pos
    return [-1,-1]


def Solver_ModifiedBacktracking(objGrid):
    objGrid, solvable = lookAhead(objGrid)
    if not solvable:
        return False

    position = find_next_empty(objGrid)
    if(position[0] == -1):
        return True

    for entry in objGrid[position[0]][position[1]].candidate:
        objGrid[position[0]][position[1]].updateEntry(entry)
        if(Solver_ModifiedBacktracking(objGrid)):
            return True
        objGrid[position[0]][position[1]].candidate.eliminateCandidate(set([entry]))
        objGrid[position[0]][position[1]].updateEntry(0)
    return False
