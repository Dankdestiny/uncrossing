# Uncrossing
A puzzle game where a planar network is generated, and the position of the nodes randomized so that the edges of the network are crossing.
The objective is the drag the nodes to uncross the edges, hence the name. Once all lines are uncrossed, pressing space will generate a harder puzzle.
# Connect 4
Same rules as connect 4. To make a play press 1-7 and a coloured disk will appear in the corresponding column. 
# Cube
An attempt at displaying a 3d object on a screen. Program will behave strangely if the camera faces away from or gets too close to the shape.
WASD moves the position of the camera based on its direction, space moves it upwards. Click and drag to rotate the camera.
# Mastermind
Based on a board game. Upon starting the game the computer will generate 4 randomly coloured circles in a particular order, which are hidden from the user.
The objective is to figure out what the colour and position of the circles is. 
To make a guess, click on a circle on the top unfilled row and press a number from 1-6. Each number corresponds to a 
colour as indicated by the key on the right side of the window. 
Once a row has been filled you can submit your guess. The game will give feedback indicating how close yoru guess is by displaying a number of black and white dots at the end of the row.
Each black dot indicates that a circle was of the correct colour and in the correct position.
Each white dot indicates that a circle was of the correct colour and in the wrong position.
The user has 10 guesses before they lose. Upon winning or losing the game will display the correct solution.
# Roguelike
Work in progress.
This project was an attempt to try and create line of sight in a 2d game. The program creates an environment made of walls and floors. Walls block the users line of sight, but moving around the game space (with WASD) will reveal the map. Performance is currently lacking and there are a number of improvements that can be made. 
# Sudoku Solver
Solves Sudoku puzzles up to those that are rated "hard". Clicking on a square will select it, and entering a number from 1-9 will enter that value into the square. Each time the user input a number the program will eliminate redundant candidates to solve the puzzle.
# Tetris
Follows standard Tetris rules. Up rotates a shape, left/right move it accordingly, down makes it fall faster.
upon filling a row the squares in that row are deleted and the score goes up by 1.
The game speeds up as the score increases.
