# Sudoku-Solver

A kivy app that solves a Sudoku puzzle contained in the picture uploaded or taken by the user.

The first part of the algorithm uses OpenCV and a CNN trained on the MINIST dataset to extract the Sudoku puzzle.

The UI is designed so that it's easy for the user to correct any prediction errors.

Finally the algorithm uses Backtracking, Modified-Backtracking, and MCMC to solve the Sudoku puzzle.
