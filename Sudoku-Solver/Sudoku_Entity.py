import itertools
import sys
import math
import random
from copy import deepcopy

# Define the basic Sudoku Entity Class
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

# Define Basic Puzzle Class
class SudokuPuzzle(object):
    def __init__(self,SukokuEntityType):
        self.grid = [[deepcopy(SukokuEntityType) for i in range(9)] for j in range(9)]
        self.subGrid = []
        # Arranged by row
        for i in range(3):
            for j in range(3):
                temp = list(itertools.product(range(3*i, 3*i +3), range(3*j, 3*j +3)))
                self.subGrid.append(temp)
        del temp

    def initGrid(self, puzzle):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].updateEntry(puzzle[i][j])
                self.grid[i][j].updatePosBlock(i,j)
    def output(self, a):
        sys.stdout.write(str(a))
    def printSelf(self,attribute = "entry"):
        for i in range(9):
            for j in range(9):
                cell = getattr(self.grid[i][j],attribute)
                if cell == 0:
                    self.output('.')
                else:
                    self.output(cell)
                if (j + 1) % 3 == 0 and j < 8:
                    self.output(' |')
                if j != 8:
                    self.output(' ')
            self.output('\n')
            if (i + 1) % 3 == 0 and i < 8:
                self.output("- - - + - - - + - - -\n")
    def gridToList(self):
        grid  = [[0 for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                grid[i][j] = self.grid[i][j].entry
        return grid
# Modified Sudoku class
class EnSudokuEntity(SudokuEntity):
    def __init__(self):
        super().__init__()
        self.candidate = set(range(1,10))
    def trivalCandidate(self):
        if(self.entry != 0):
            self.candidate = set()
    def canToEntry(self):
        if(len(self.candidate) == 1):
            self.updateEntry(self.candidate.pop())
    def eliminateCandidate(self, values):
        self.candidate -= values

class EnSudokuPuzzle(SudokuPuzzle):
    def __init__(self,SukokuEntityType):
        super().__init__(SukokuEntityType)
    def initGrid(self, puzzle):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].updateEntry(puzzle[i][j])
                self.grid[i][j].updatePosBlock(i,j)
                self.grid[i][j].trivalCandidate()


# MCMC Sudoku Class
class TSudokuEntity(SudokuEntity):
    def __init__(self):
        super().__init__()
        self.trialEntry = 0
        self.fixed = False
    def updateFixed(self):
        if(self.entry != 0):
            self.fixed = True
            self.trialEntry = self.entry
    def updateTrial(self, newTrial):
        self.trialEntry = newTrial
    def becomeReal(self):
        self.updateEntry(self.trialEntry)
        self.fixed = True

class TSudokuPuzzle(SudokuPuzzle):
    def __init__(self):
        super().__init__(TSudokuEntity())
        self.rowCost = [math.inf for i in range(9)]
        self.colCost = [math.inf for i in range(9)]
        self.totCost = math.inf
        self.blockFixed = [False for i in range(9)]
    def initGrid(self, puzzle):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].updateEntry(puzzle[i][j])
                self.grid[i][j].updatePosBlock(i,j)
                self.grid[i][j].updateFixed()
    def initSolve(self):
        for i in range(9):
            temp = set(range(1, 10))
            tempNFixed = []
            for j in range(9):
                tempPos = self.subGrid[i][j]
                if(self.grid[tempPos[0]][tempPos[1]].fixed):
                    temp.discard(self.grid[tempPos[0]][tempPos[1]].entry)
                else:
                    tempNFixed.append(j)
            if(len(tempNFixed) == 1):
                tempPos = self.subGrid[i][tempNFixed[0]]
                self.grid[tempPos[0]][tempPos[1]].updateTrial(temp.pop())
                self.grid[tempPos[0]][tempPos[1]].becomeReal()
                self.blockFixed[i] = True
            elif(len(tempNFixed) > 1):
                for j in tempNFixed:
                    tempPos = self.subGrid[i][j]
                    tempGrid = self.grid[tempPos[0]][tempPos[1]]
                    if(not tempGrid.fixed):
                        tempGrid.updateTrial(temp.pop())
            else:
                self.blockFixed[i] = True
    def updateRowCost(self,rowNum):
        temp = set(range(1, 10))
        for i in range(9):
            temp.discard(self.grid[rowNum][i].trialEntry)
        self.rowCost[rowNum] = len(temp)
    def updateColCost(self,colNum):
        temp = set(range(1, 10))
        for i in range(9):
            temp.discard(self.grid[i][colNum].trialEntry)
        self.colCost[colNum] = len(temp)
    def updateTotCost(self):
        self.totCost = sum(self.colCost) + sum(self.rowCost)
    def randomSelect(self,blockNum):
        temp = set(range(9))
        for i in range(9):
            tempPos = self.subGrid[blockNum][i]
            if(self.grid[tempPos[0]][tempPos[1]].fixed):
                temp.discard(i)
        sampleInd = random.sample(temp, 2)
        return self.subGrid[blockNum][sampleInd[0]], self.subGrid[blockNum][sampleInd[1]]
    def swap(self, sample1, sample2):
        self.grid[sample1[0]][sample1[1]].updatePosBlock(sample2[0],sample2[1])
        self.grid[sample2[0]][sample2[1]].updatePosBlock(sample1[0],sample1[1])
        self.grid[sample1[0]][sample1[1]].trialEntry, self.grid[sample2[0]][sample2[1]].trialEntry=self.grid[sample2[0]][sample2[1]].trialEntry, self.grid[sample1[0]][sample1[1]].trialEntry
