import math
import random
import numpy
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
        
    

def Solver_MCMC(puzzle,t):
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
            if(objGrid.blockFixed):
                continue
            
            sample1, sample2 = objGrid.randomSelect(i)
            objGrid.swap(sample1,sample2)
  
            objGrid.updateRowCost(sample1[0])
            objGrid.updateRowCost(sample2[0])
            objGrid.updateColCost(sample1[1])
            objGrid.updateColCost(sample2[1])
            tempTotCost = objGrid.totCost
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
                    objGrid.updateColCost(sample2[2])
                    objGrid.updateTotCost()
            objGrid.printSelf()
            print("the block num is %d" % i)
      
    for i in range(9):
        for j in range(9):
            objGrid.grid[i][j].becomeReal()
    
    objGrid.printSelf()
    
            
    
            

        
        
        
