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
        self.terminate = False

    def create_board(self):
        """docstring"""

        size = 9
        mines = random.sample(range(size**2), 10)
        self.game_board = [[0]*size for _ in range(size)]
        self.visible_game_board = [[' ']*size for _ in range(size)]

        for mine in mines:
            row, column = mine//9, mine % 9
            self.game_board[row][column] = 'M'
            for key, value in self.check_area((row,column), 'M'):
                if value != 'M':
                    self.game_board[key[0]][key[1]] += 1

    def check_area(self, square:tuple, target:str):
        """docstring"""

        print(square)
        area = {}
        row, column = square
        # Its a bit confusing as player uses row 1 and im using row 0 doe. - fix later ennit.
        top = row == 0
        bottom = row == 8
        left = column == 0
        right = column == 8

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

        return area.items()

    def print_board(self):
        """docstring"""

        size = 9
        letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
        print("\t\t\tMINESWEEPER\n")
        print('      ', end='')
        for _ in range(size):
            print(f'{_+1}     ', end='')
        print()
        print('   '+'_'*size*6)

        for index, row in enumerate(self.visible_game_board):
            print('   ', end='')
            print('|     '*size + '|')
            print(f'{letters[index]}  ', end='')
            for _ in row:
                print(f'|  {_}  ', end='')

            print('|')
            print('   ', end='')
            print('|_____'*size + '|')

    def game_play(self):
        """docstring"""
        action = input('Open(O) or Flag(F)? \n').lower()
        cell = input('Enter Row, Column\n').lower()
        row, column = ord(cell[0])-97, int(cell[1])-1
        cell_data = self.game_board[row][column]
        if action == 'o':
            if cell_data == 'M':
                print('you have lost!')
                self.visible_game_board = self.game_board

            else:
                if cell_data == 0:
                    self.check_data()
                self.visible_game_board[row][column] = cell_data
        if action == 'f':
            self.visible_game_board[row][column] = 'F'


if __name__ == "__main__":
    m = Minesweeper()
    m.create_board()
    m.print_board()
    while not m.terminate:
        m.print_board()
        m.game_play()
