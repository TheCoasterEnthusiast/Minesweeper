import random


class Grid:
    def __init__(self, width: int, height: int, mines: int, initial_tile: tuple):
        self.grid = []
        self.mines = mines
        probability = self.mines / (width * height)

        for row in range(height):  # populates array with either X or O randomly based on probability
            self.grid.append([])   # that any given tile is a bomb
            for column in range(width):
                if random.random() <= probability and self.mines:
                    self.grid[row].append('X')
                    self.mines -= 1
                else:
                    self.grid[row].append('O')

        self.fill_initial_tile(initial_tile, '0')  # fills initial tile area with '0' placeholder

        while self.mines:  # assigns any mines that have yet to be placed
            for row_index, row in enumerate(self.grid):
                for column_index, column in enumerate(row):
                    if column == 'O' and random.random() <= probability:
                        self.grid[row_index][column_index] = 'X'
                        self.mines -= 1
                    if not self.mines:
                        break
                if not self.mines:
                    break

        self.fill_initial_tile(initial_tile, 'O')  # reverts placeholders to '0'

    def __repr__(self):
        string = ''
        for row in self.grid:
            str_row = f'{str(row)}\n'
            string = f'{string} {str_row}'
        return string

    def fill_initial_tile(self, initial_tile, element: str):
        """Defines area around a given point to a given string"""
        row, column = initial_tile  # ensures initial tile and surrounding tiles aren't a bomb
        modifiers = [-1, 0, 1]
        for row_modifier in modifiers:
            for column_modifier in modifiers:
                row_index = row + row_modifier
                column_index = column + column_modifier
                try:
                    if self.grid[row_index][column_index] == 'X':
                        self.mines += 1
                    self.grid[row_index][column_index] = element
                except IndexError:
                    pass
