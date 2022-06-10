from unittest import TestCase
from grid import Grid

initial_tile = (8, 5)


class TestGrid(TestCase):
    def setUp(self) -> None:
        self.my_grid = Grid(width=10, height=10, mines=15, initial_tile=initial_tile)
        self.initial_row, self.initial_column = initial_tile

    def test_number_of_mines(self):
        total_mines = 0
        for row in self.my_grid.grid:
            for column in row:
                if column == 'X':
                    total_mines += 1
        self.assertEqual(15, total_mines)

    def test_initial_tiles_empty(self):
        total_mines = 0
        modifiers = [-1, 0, 1]
        for row_modifier in modifiers:
            for column_modifier in modifiers:
                row_index = self.initial_row + row_modifier
                column_index = self.initial_column + column_modifier
                try:
                    if self.my_grid.grid[row_index][column_index] == 'X':
                        total_mines += 1
                except IndexError:
                    pass

        self.assertEqual(0, total_mines)

# unit testing
