"""
CMP1902M Assessment Task 2: Implement the Minesweeper game

•   Minesweeper is a retro single-player puzzle game (Wikipedia). The objective is to find all the
    mines within a grid, based on the help of cues that provide the number of mines in the adjacent
    squares. You can play the game here. For Task 2 you will develop a playable version of the
    game where the user will interact using the terminal as an interface (no GUI is needed).

"""

import random
from time import perf_counter


class Minesweeper:
    """class doctring
    """

    def __init__(self):
        """docstring"""
        self.game_board = []
        self.visible_game_board = []
        self.won = None
        self.difficulty = None
        self.width, self.height, self.mines = None, None, None
        self.levels = {1: (9, 9, 10), 2: (16, 16, 40), 3: (30, 16, 99)}
        self.name = ''
        self.flagged_mines = 0

    def create_board(self):
        """docstring"""

        mines = random.sample(
            range(self.width*self.height), self.mines)
        self.game_board = [[0]*self.width for _ in range(self.height)]
        self.visible_game_board = [
            [' ']*self.width for _ in range(self.height)]

        for mine in mines:
            row, column = mine//self.width, mine % self.height
            self.game_board[row][column] = 'M'
            for key, value in self.check_area((row, column)):
                if value != 'M':
                    self.game_board[key[0]][key[1]] += 1

    def check_area(self, square: tuple):
        """docstring"""
        area = {}
        row, column = square

        top = row == 0
        bottom = row == self.height-1
        left = column == 0
        right = column == self.width-1

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

        letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
        print("\t\t\tMINESWEEPER\n")
        print('      ', end='')
        for _ in range(self.width):
            if _ > 8:
                print(f'{_+1}    ', end='')
            else:
                print(f'{_+1}     ', end='')
        print()
        print('   '+'_'*self.width*6)

        for index, row in enumerate(self.visible_game_board):
            print('   ', end='')
            print('|     '*self.width + '|')
            print(f'{letters[index]}  ', end='')
            for _ in row:
                print(f'|  {_}  ', end='')

            print('|')
            print('   ', end='')
            print('|_____'*self.width + '|')

    def game_play(self):
        """docstring"""
        print(f'There is {self.mines - self.flagged_mines} mines unflagged.')
        action = input('Open(O) or Flag(F)? \n').lower()
        cell = input('Enter Row, Column\n').lower()
        #sanitize data here!
        row, column = ord(cell[0])-97, int(cell[1:])-1
        cell_data = self.game_board[row][column]
        if action == 'o':
            if cell_data == 'M':
                self.visible_game_board = self.game_board
                self.won = False
            else:
                visited = set()

                def show_mines(row, column):
                    # if the cell chosen is 0 then show all the cells around it
                    if cell_data == 0:
                        for key, value in self.check_area((row, column)):
                            # if the cell is 0 and has not been visited then show it and check its neighbors
                            if value == 0 and key not in visited:
                                self.visible_game_board[key[0]][key[1]] = value
                                visited.add(key)
                                show_mines(key[0], key[1])
                            # the cell is not 0 so just show it
                            else:
                                self.visible_game_board[key[0]][key[1]] = value
                    else:
                        self.visible_game_board[row][column] = cell_data
                show_mines(row, column)
                self.visible_game_board[row][column] = cell_data

        if action == 'f':
            if self.visible_game_board[row][column] == 'F':
                self.visible_game_board[row][column] = ' '
            else:
                self.visible_game_board[row][column] = 'F'
            
            if cell_data == 'M':
                self.flagged_mines += 1


        if self.flagged_mines == self.mines:
            self.won = True
    def start(self):
        """docstring"""

        self.name = input(
            '\t\tWelcome to my Minesweeper!! \n\nEnter your name:')
        self.difficulty = int(
        input("\nThe three difficulty's are 9x9(1), 16x16(2), 30x16(3).\nChoose your difficulty:"))
        self.width, self.height, self.mines = self.levels[self.difficulty][0], self.levels[self.difficulty][1], self.levels[self.difficulty][2]
        self.create_board()
        start_time = perf_counter()

        while self.won is None:
            self.print_board()
            self.game_play()

        end_time = perf_counter()

        if self.won:
            print(f'Congratulations {self.name} you have won!')
            record = (f'{self.name}, {self.difficulty}, {round(end_time - start_time, 1)}')
            with open('leaderboard.txt', 'w', encoding='utf-8') as file:
                file.write(record)
        else:
            print(f'You have lost {self.name} better luck next time!')

        print(f"Elapsed time: {round(end_time - start_time, 1)}")
        input('Press enter to exit')


if __name__ == "__main__":
    m = Minesweeper()
    m.start()
