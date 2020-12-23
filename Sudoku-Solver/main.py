# -*- coding: utf-8 -*-

import numpy as np
import kivy

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import cv2
import sys
from time import time
import matplotlib.pyplot as plt

from Backtracking import Solver_Backtracking

from MCMC import Solver_MCMC
from misc import print_puzzle

from extractSudoku import extract as extract_img_grid
from cnn import run as create_and_save_Model
from extractDigit import extract_number_image as sudoku_extracted




Window.size = (1600, 600)


class SudokuSquare(TextInput):
    """A Sudoku Square can only contain one digit"""
    pass


class SudokuGrid(GridLayout):
    """9*9 input Grid."""

    def __init__(self, **kwargs):
        # super(SudokuGrid, self).__init__(cols=3, spacing=[5, 5], **kwargs)
        # self.squares = [[0 for i in range(9)] for j in range(9)]
        # for i in range(9):
        #     subgrid = GridLayout(cols=3)
        #     for j in range(9):
        #         square = SudokuSquare()
        #         subgrid.add_widget(square)
        #         self.squares[i][j] = square
        #     self.add_widget(subgrid)
        super(SudokuGrid, self).__init__(cols=3, spacing=[5, 5], **kwargs)
        self.squares = []
        for i in range(9):
            subgrid = GridLayout(cols=3)
            for j in range(9):
                square = SudokuSquare()
                subgrid.add_widget(square)
                self.squares.append(square)
            self.add_widget(subgrid)

    def to_array(self):
        # grid = [[0 for i in range(9)] for j in range(9)]
        # for i in range(9):
        #     for j in range(9):
        #         square = self.squares[i][j]
        #         if square.text == '':
        #             continue
        #         else:
        #             grid[i][j] = int(square.text)

        user_input = [0 if square.text == '' else int(square.text)
                      for square in self.squares]
        subgrids = np.vsplit(np.array(user_input).reshape(27, 3), 9)
        grid = np.vstack((np.hstack(subgrids[0:3]),
                          np.hstack(subgrids[3:6]),
                          np.hstack(subgrids[6:9])))
        return grid

    def update_from_array(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    grid[i][j] = ""

        grid = np.array(grid)
        subgrids = [np.hsplit(_, 3) for _ in np.vsplit(grid, 3)]
        output_values = np.vstack(subgrids).reshape(1, 81)[0]
        for square, value in zip(self.squares, output_values):
            square.text = str(value)


class SudokuWidget(BoxLayout):
    """Main Widget of the Sudoku App"""
    grid_widget = ObjectProperty(None)
    image_path = StringProperty()


    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        # camera.export_to_png("IMG_{}.png".format(timestr))
        camera.export_to_png("sudoku.png")
        self.image_path = "sudoku.png"
        print("Captured")
    def selected_file(self, *args):
            print("*args=", args,"\n")
            self.image_path = args[1][0]
            print(type(self.image_path))
            print(args[1])
            for arg in args:
                print("arg=", arg)
    def display(self, filename):
        try:
            self.ids.image.source = filename[0]
        except:
            pass
    def extract(self):
        # image_path = 'sudoku3.jpg'
        try:
            image_grid = extract_img_grid(self.image_path)
            print("Image Grid extracted")
            self.grid = sudoku_extracted(image_grid)
            print("Extracted and predict digits in the Sudoku")
            print("\nSudoku grid:")
            print_puzzle(self.grid)
            self.grid_widget.update_from_array(self.grid)
        except:
            fmt = 'usage: {} image_path'
            print(fmt.format(__file__.split('/')[-1]))
            print('[ERROR]: Image not found')

    def solveMCMC(self):
        self.grid = self.grid_widget.to_array()
        solvable, grid_solved = Solver_MCMC(self.grid)
        if solvable:
            self.grid_widget.update_from_array(grid_solved)
        else:
            print("Error")
    def solve(self):
        self.grid = self.grid_widget.to_array()
        solvable, grid_solved = Solver_Backtracking(self.grid)
        if solvable:
            self.grid_widget.update_from_array(grid_solved)
        else:
            print("Error")
    # def _solve(self):
    #     """Recursive solving method based on 2 methods:
    #             - First it finds squares only allowing 1 possibility and fills
    #             them
    #             - Then it bruteforces the remaining squares
    #     """
    #     just_one_more_turn = False  # Hahaha LOL
    #     finished = True  # by default, we assume there is no empty square
    #     brute_needed = {}
    #     print(self.grid)
    #
    #     for r in range(9):  # row index
    #         for c in range(9):  # column index
    #             subgrid = self.grid[(3 * int(r / 3)):(3 * int(r / 3) + 3),
    #                                 (3 * int(c / 3)):(3 * int(c / 3) + 3)]
    #             if self.grid[r, c] == 0:
    #                 finished = False  # there is at least one empty square
    #                 possibilities = [digit for digit in range(1, 10)
    #                                  if (digit not in self.grid[r, :] and
    #                                      digit not in self.grid[:, c] and
    #                                      digit not in subgrid)]
    #                 if len(possibilities) == 1:
    #                     self.grid[r, c] = possibilities[0]
    #                     just_one_more_turn = True
    #                 elif (not brute_needed or
    #                       len(possibilities) <
    #                       len(brute_needed['possibilities'])):  # perfs
    #                     brute_needed['r'] = r
    #                     brute_needed['c'] = c
    #                     brute_needed['possibilities'] = possibilities
    #
    #     if just_one_more_turn:
    #         return self._solve()  # − Luke, this is recursion. − Nooooooo....
    #     else:
    #         if finished:
    #             return finished  # Yeah!
    #         else:  # Here starts BruteforceLand
    #             print('BRUTEFORCE!!!')
    #             r = brute_needed['r']
    #             c = brute_needed['c']
    #             for possibility in brute_needed['possibilities']:
    #                 previous_grid = np.array(self.grid)
    #                 self.grid[r, c] = possibility
    #                 finished = self._solve()
    #                 if finished:
    #                     return finished
    #                 else:
    #                     self.grid = np.array(previous_grid)
    #             # if the loop ends, it means that the grid has no solution
    #             return False
    #
    # def solve(self):
    #     """Method called by the 'Solve it!' button."""
    #     self.grid = self.grid_widget.to_array()
    #     print("self.grid")
    #     print(self.grid)
    #     solved = self._solve()
    #     if solved:
    #         self.grid_widget.update_from_array(self.grid)
    #     else:
    #         print('Error')


class SudokuApp(App):
    """Application"""
    def build(self):
        return SudokuWidget()


if __name__ == '__main__':
    app = SudokuApp()
    app.run()
