import math
import random
from Sudoku_Entity import SudokuEntity
from Sudoku_Entity import SudokuPuzzle

class TSudokuEntity(SudokuEntity):
    def __init__(self):
        SudokuEntity.__init__(self)
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
        SudokuPuzzle.__init__(self,TSudokuEntity())
        self.rowCost = [math.inf for i in range(9)]
        self.colCost = [math.inf for i in range(9)]
        self.totCost = math.inf
    def initGrid(self, puzzle):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].updateEntry(puzzle[i][j])
                self.grid[i][j].updatePosBlock(i,j)
                self.grid[i][j].updateFixed()         
    def initSolve(self):
        for i in range(9):
            temp = set(range(1, 10))
            for j in range(9):
                tempPos = self.subGrid[i][j]
                tempGrid = self.grid[tempPos[0]][tempPos[1]]
                if(tempGrid.fixed):
                    temp.discard(tempGrid.entry)
            for j in range(9):
                tempPos = self.subGrid[i][j]
                tempGrid = self.grid[tempPos[0]][tempPos[1]]
                if(not tempGrid.fixed):
                    tempGrid.updateTrial(temp.pop())
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
            if(self.gird[tempPos[0]][tempPos[1]].fixed):
                temp.discard(i)
        sampleInd = random.sample(temp, 2)
        return self.subGrid[blockNum][sampleInd[0]], self.subGrid[blockNum][sampleInd[1]]
    def swap(self, sample1, sample2):
        self.grid[sample1[0]][sample1[1]].trialEntry, self.grid[sample2[0]][sample2[1]].trialEntry=self.grid[sample2[0]][sample2[1]].trialEntry, self.grid[sample1[0]][sample1[1]].trialEntry 
    



        
        
        