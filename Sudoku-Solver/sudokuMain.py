import cv2
import sys
from time import time
import matplotlib.pyplot as plt



from Backtracking import Solver_Backtracking
# from ModifiedBacktracking import Solver_ModifiedBacktracking
from MCMC import Solver_MCMC
from misc import print_puzzle



#Backtracking
# objectGrid = SudokuPuzzle(SudokuEntity())
# objectGrid.initGrid(puzzle)
# Solver_Backtracking(objectGrid.grid)
# objectGrid.printSelf()

#Modified Backtracking
# objectGrid = EnSudokuPuzzle(EnSudokuEntity())
# objectGrid.initGrid(puzzle)
# Solver_ModifiedBacktracking(objectGrid.grid)
# objectGrid.printSelf()



from extractSudoku import extract as extract_img_grid
from cnn import run as create_and_save_Model
from extractDigit import extract_number_image as sudoku_extracted




if __name__ == "__main__":

    def main(image_path, **kwargs):
        # Calling the image_prcoesses.py extract function to get a processed np.array of cells
        image_grid = extract_img_grid(image_path)
        print("Image Grid extracted")

        # note we have alreday created and stored the model but if you want to do that again use the following command
        # create_and_save_Model()

        # Sudoku extract
        sudoku = sudoku_extracted(image_grid)
        print("Extracted and predict digits in the Sudoku")
        print("\nSudoku grid:")
        print_puzzle(sudoku)

        print("Is the grid correct?\n")
        correct_grid = (input() == "yes")
        while not correct_grid:
            print("Row Col Num")
            temp = str.split(input())
            print(temp)
            sudoku[int(temp[0])-1][int(temp[1]) - 1] = int(temp[2])
            print_puzzle(sudoku)
            print("Is the grid correct?\n")
            correct_grid = (input() == "yes")

        print("\nSolving the Sudoku...\n")
        solvable, grid_solved = Solver_MCMC(sudoku, **kwargs)
        if solvable:
            print("Solution found")
            print_puzzle(grid_solved)
        else:
            print("MCMC method failed\n")
            print("Attempting Backtracking")
            solvable, grid_solved = Solver_Backtracking(sudoku)
            if solvable:
                print("Solution found")
                print_puzzle(grid_solved)
            else:
                print("Puzzle is unsolvable.")
    try:
        start_time = time()
        main(image_path = sys.argv[1])
        print("TAT: ", round(time() - start_time, 3))
    except:             #    except IndexError:
        fmt = 'usage: {} image_path'
        print(fmt.format(__file__.split('/')[-1]))
        print('[ERROR]: Image not found')
