"""
CMP1902M Assessment Task 2: Implement the Minesweeper game

•   Minesweeper is a retro single-player puzzle game (Wikipedia). The objective is to find all the
    mines within a grid, based on the help of cues that provide the number of mines in the adjacent
    squares. You can play the game here. For Task 2 you will develop a playable version of the
    game where the user will interact using the terminal as an interface (no GUI is needed).

"""

import random


class Minesweeper:
    """class doctring
    """

    def __init__(self):
        """docstring"""
        self.game_board = []
        self.visible_game_board = []
    def create_board(self):
        """docstring"""

        size = 9
        mines = random.sample(range(size**2), 10)
        print(mines)
        self.game_board = [[0]*size for _ in range(size)]
        self.visible_game_board = [[' ']*size for _ in range(size)]
        for mine in mines:
            row, column = mine//9, mine % 9
            self.game_board[row][column] = 'M'
            area = {}

            top = mine < 9
            bottom = mine > 71
            left = (mine % 9) == 0 or mine == 0
            right = (mine % 9) == 8 or mine == 8

            # could be put in seperate function! - although is not recalled so idk.
            if not top:
                area[(row-1, column)] = self.game_board[row -
                                                        1][column]  # Top Middle

                if not right:
                    area[(row-1, column+1)] = self.game_board[row -
                                                              1][column+1]  # Top Right

                if not left:
                    area[(row-1, column-1)] = self.game_board[row -
                                                              1][column-1]  # Top Left

            if not bottom:
                area[(row+1, column)] = self.game_board[row +
                                                        1][column]  # Bottom Middle

                if not right:
                    area[(row+1, column+1)] = self.game_board[row +
                                                              1][column+1]  # Bottom Right

                if not left:
                    area[(row+1, column-1)] = self.game_board[row +
                                                              1][column-1]  # Bottom Left

            if not left:
                # Middle Left
                area[(row, column-1)] = self.game_board[row][column-1]

            if not right:
                # Middle Right
                area[(row, column+1)] = self.game_board[row][column+1]

            for key, value in area.items():
                if value != 'M':
                    self.game_board[key[0]][key[1]] += 1

    def print_board(self):
        """docstring"""

        size = 9
        letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
        print("\t\t\tMINESWEEPER\n")
        print('      ',end='')
        for _ in range(size):
            print(f'{_+1}     ',end='')
        print()
        print('   '+'_'*size*6)

        for index, row in enumerate(self.visible_game_board):
            print('   ',end='')
            print('|     '*size + '|')
            print(f'{letters[index]}  ',end='')
            for _ in row:
                print(f'|  {_}  ', end='')

            print('|')
            print('   ',end='')
            print('|_____'*size + '|')

    def game_play(self):
        """docstring"""
        action = input('Open(O) or Flag(F)? \n').lower()
        cell = input('Enter Row, Column\n').lower()
        cell = ord(cell[0])-97,int(cell[1])-1
        if action == 'o':
            if self.game_board[cell[0]][cell[1]] == 'M':
                print('you lose!')
                return False

            else:
                self.visible_game_board[cell[0]][cell[1]] = str(self.game_board[cell[0]][cell[1]])
                return True
        if action == 'f':
            print('yipee')

if __name__ == "__main__":
    m = Minesweeper()
    m.create_board()
    m.print_board()
    while m.game_play():
            m.print_board()
