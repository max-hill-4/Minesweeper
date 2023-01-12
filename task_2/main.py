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
    """Main singleton class to handle all functions.

    Creates a minesweeper game with 3 difficulty levels using ASCII art 
    in the console.
    """

    def __init__(self):
        """docstring"""
        self.game_board = []
        self.visible_game_board = []
        self.won = None
        self.hint = False
        self.width, self.height, self.mines = None, None, None
        self.name = ''
        self.flagged_mines = 0

    def create_board(self):
        """Sets up gameboard ready for play
        
        Creates 2 empty lists of correct size for visible gameboard
        and actual data values. Random mines are generated and appended to the 
        list, and then cues are calculated for such mine. 
        """

        # Creates list of correct size and range for mines.
        mines = random.sample(range(self.width*self.height), self.mines)
        # Creates 2d list of correct size and fills with 0's.
        self.game_board = [[0]*self.width for _ in range(self.height)]
        # Creates 2d list of correct size and fills with spaces.
        self.visible_game_board = [[' ']*self.width for _ in range(self.height)]

        # Adds mines to game board.
        for mine in mines:
            # Converts 1d list index to 2d list index.
            row, column = mine//self.width, mine % self.height
            self.game_board[row][column] = 'M'
            # Adds 1 to all adjacent squares.
            for key, value in self.check_area((row, column)):
                if value != 'M':
                    self.game_board[key[0]][key[1]] += 1

    def check_area(self, square: tuple):
        """Function to get all squares surrounding location
        
        Used for checking if surrounding area has 0's or bombs nearby.

        Returns:
            A dictionary that contains the location of the square and value
        Args:
            square: tuple that holds the location in the format row,column
        """
        area = {}
        row, column = square

        # Boolean checks to see if square is on edge of board.
        top = row == 0
        bottom = row == self.height-1
        left = column == 0
        right = column == self.width-1
        
        # Checks all adjacent squares and adds them to area dict.
        if not top:
            area[(row-1, column)] = self.game_board[row-1][column]  # Top Middle

            if not right:
                area[(row-1, column+1)] = self.game_board[row-1][column+1]  # Top Right

            if not left:
                area[(row-1, column-1)] = self.game_board[row-1][column-1]  # Top Left

        if not bottom:
            area[(row+1, column)] = self.game_board[row+1][column]  # Bottom Middle

            if not right:
                area[(row+1, column+1)] = self.game_board[row+1][column+1]  # Bottom Right

            if not left:
                area[(row+1, column-1)] = self.game_board[row+1][column-1]  # Bottom Left

        if not left:
            area[(row, column-1)] = self.game_board[row][column-1] # Middle Left

        if not right:
            area[(row, column+1)] = self.game_board[row][column+1] # Middle Right

        return area.items()

    def print_board(self):
        """Outputs board to console
        
        Uses self.width and self.height to work out how many times to 
        print according symbols.
        """

        letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
        print("\t\t\tMINESWEEPER\n")
        print('      ', end='')
        # Prints column numbers.
        for _ in range(self.width):
            # Adds extra space to numbers less than 10.
            if _ > 8:
                print(f'{_+1}    ', end='')
            else:
                print(f'{_+1}     ', end='')
        print()
        print('   '+'_'*self.width*6)
        for index, row in enumerate(self.visible_game_board):
            # Prints row letters.
            print('   ', end='')
            print('|     '*self.width + '|')
            print(f'{letters[index]}  ', end='')
            # Prints row data.
            for _ in row:
                print(f'|  {_}  ', end='')
            print('|')
            print('   ', end='')
            print('|_____'*self.width + '|')

    def game_play(self):
        """Allows for user input and changes game accordingly
        
        Allows for 3 different inputs and reacts accordingly to 
        traditional minesweeper rules.
        """
        print(f'There is {self.mines - self.flagged_mines} mines unflagged.')
        action = input('Open(O) or Flag(F) or Hint(H)? \n').lower()
        if not (action == 'f' or action == 'o' or action == 'h'):
            print('Invalid action. Try again.')
            return
        if action != 'h':
            cell = input('Enter Row, Column\n').lower()
            # Handles unexpected inputs.
            try:
                row, column = ord(cell[0])-97, int(cell[1:])-1
            except ValueError:
                print('Invalid cell. Try again.')
                return
            if row < 0 or row > self.height-1 or column < 0 or column > self.width-1:
                print('Invalid cell. Try again.')
                return
            cell_data = self.game_board[row][column]

        if action == 'o':
            # If the cell chosen is a mine then the game is over.
            if cell_data == 'M':
                self.visible_game_board = self.game_board
                self.won = False
            else:
                visited = set()
                # Recursive function to show all the cells around a 0 cell.
                def show_mines(row, column):
                    # if the cell chosen is 0 then show all the cells around it.
                    if cell_data == 0:
                        # check all the cells around the cell
                        for key, value in self.check_area((row, column)):
                            if value == 0 and key not in visited:
                                self.visible_game_board[key[0]][key[1]] = value
                                visited.add(key)
                                # check the neighbors of the neighbor.
                                show_mines(key[0], key[1])
                            # show it wihout checking its neighbors as not 0.
                            else:
                                self.visible_game_board[key[0]][key[1]] = value
                    else:
                        self.visible_game_board[row][column] = cell_data
                show_mines(row, column)
                self.visible_game_board[row][column] = cell_data

        if action == 'f':
            # If the cell is already flagged then unflag it.
            if self.visible_game_board[row][column] == 'F':
                self.visible_game_board[row][column] = ' '
            else:
                self.visible_game_board[row][column] = 'F'

            # If the cell is a mine then add to the flagged_mines.
            if cell_data == 'M':
                self.flagged_mines += 1

        if action == 'h' and not self.hint:
            self.hint = True
            # Find the first mine and flag it.
            for index, row in enumerate(self.game_board):
                for index2, column in enumerate(row):
                    if column == 'M':
                        self.visible_game_board[index][index2] = 'F'
                        self.flagged_mines += 1
                        return

        if self.flagged_mines == self.mines:
            self.won = True

    def start(self):
        """Called to begin the game
        
        Function that calls the functions to create the game, and also 
        takes data such as name and time to append to the leaderboard file.
        This function also handles the gamestate and when to terminate.
        """

        self.name = input(
            '\t\tWelcome to my Minesweeper!! \n\nEnter your name:')
        try:
            difficulty = int(input("""\nThe three difficulty's are 9x9(1), 16x16(2), 30x16(3).\n
            Choose your difficulty:"""))
        except ValueError:
            print('Please enter a number!')
            self.start()

        levels = {1: (9, 9, 10), 2: (16, 16, 40), 3: (30, 16, 99)}
        self.width, self.height, self.mines = levels[difficulty]
        self.create_board()
        start_time = perf_counter()

        while self.won is None:
            self.print_board()
            self.game_play()

        end_time = perf_counter()

        if self.won:
            print(f'Congratulations {self.name} you have won!')
            record = (
                f'\n{self.name}, {self.width}x{self.height}, {round(end_time - start_time, 1)}')
            with open('leaderboard.txt', 'a', encoding='utf-8') as file:
                file.write(record)
        else:
            print(f'You have lost {self.name} better luck next time!')

        print(f"Elapsed time: {round(end_time - start_time, 1)}")
        input('Press enter to exit')


if __name__ == "__main__":
    m = Minesweeper()
    m.start()
