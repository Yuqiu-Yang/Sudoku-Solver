import sys
def output(a):
    sys.stdout.write(str(a))
def print_puzzle(puzzle):
    if not puzzle:
        output("No solution")
        return
    for i in range(9):
        for j in range(9):
            cell = puzzle[i][j]
            if cell == 0 or isinstance(cell, set):
                output('.')
            else:
                output(cell)
            if (j + 1) % 3 == 0 and j < 8:
                output(' |')
            if j != 8:
                output(' ')
        output('\n')
        if (i + 1) % 3 == 0 and i < 8:
            output("- - - + - - - + - - -\n")
            
                       
def uniqueEle(testList):
    uniEle = set(testList)
    seen = set()
    for k in testList:
        if(k in seen):
            uniEle.discard(k)
        seen.add(k)
    return uniEle
            
            

