"""
CMP1902M Assessment Task 2: Implement the Minesweeper game

•   Minesweeper is a retro single-player puzzle game (Wikipedia). The objective is to find all the
    mines within a grid, based on the help of cues that provide the number of mines in the adjacent
    squares. You can play the game here. For Task 2 you will develop a playable version of the
    game where the user will interact using the terminal as an interface (no GUI is needed).

"""

import time
import random
import traceback
class Minesweeper:
    """class doctring
    """

    def __init__(self):
        """docstring"""
        self.game_board =  []

    def create_board(self, level = 1):
        """docstring"""

        size = 9
        mines = random.sample(range(size**2), 10)
        print(mines)
        self.game_board = [[0]*size for _ in range(size)]
        for mine in mines:
            row, column = mine//9, mine%9
            self.game_board[row][column] = 'M'
            
            area = {}
            # duplicates with corners.
            # check if edge piece and handle.
            try:
                if not ((mine % 9) == 0 or mine == 0): # If its not in the first column.
                    area.update({
                        (row-1, column-1):self.game_board[row-1][column-1], # Top Left
                        (row, column-1):self.game_board[row][column-1], # Middle Left
                        (row+1, column-1):self.game_board[row+1][column-1] # Bottom Left
                        })
                
                if mine > 8: # If not first row.
                    area.update({
                        (row-1, column):self.game_board[row-1][column], # Top Middle
                        (row-1, column+1):self.game_board[row-1][column+1], # Top Right
                        (row-1, column-1):self.game_board[row-1][column-1] # Top Left
                        })
                
                if mine < 72: #If not last row.
                    area.update({
                        (row+1, column+1):self.game_board[row+1][column+1], # Bottom Right
                        (row+1, column):self.game_board[row+1][column], # Bottom Middle
                        (row+1, column-1):self.game_board[row+1][column-1] # Bottom Left
                        })
                
                if not ((mine % 9) == 9 or mine == 8): # if last column
                    area.update({
                        (row,column+1):self.game_board[row][column+1], # Middle Right
                        (row-1, column+1):self.game_board[row-1][column+1], # Top Right
                        (row+1, column+1):self.game_board[row+1][column+1], # Bottom Right
                        })
            except Exception:
                print(mine)
                print(traceback.format_exc())

            
            for key, value in area.items():
                if value != 'M':
                    self.game_board[key[0]][key[1]] +=1
       

    
    def print_board(self):
        """docstring"""

        size = 9

        print("\t\t\tMINESWEEPER")
        print('_'*size*6)
        
        for row in self.game_board:
            print('|     '*size + '|')
            for _ in row:
                
                print(f'|  {_}  ',end='')
            print('|')
            print('|_____'*size + '|')
    
    
    def game_play(self):
        """docstring"""

m = Minesweeper()
m.create_board()
m.print_board()
