import pygame

from grid import Grid
from square import Square

width, height = 900, 500
GAME_NAME = 'Minesweeper'
FPS = 60
DEFAULT_ROWS = 10
DEFAULT_COLUMNS = 20
DEFAULT_MINES = 25

run = True
game_active = True
pygame.init()
WIN = pygame.display.set_mode((width, height))
WIN_rect = WIN.get_rect()
pygame.display.set_caption(GAME_NAME)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def uncover_adjacent_squares(row, column):
    for row_modifier in modifiers:
        for column_modifier in modifiers:
            row_index = row + row_modifier
            column_index = column + column_modifier
            try:
                if row_index >= 0 and column_index >= 0 and (row, column) != (row_index, column_index):
                    print(f'Adjacent square: {square_grid[row_index][column_index]}')
                    adjacent_square = square_grid[row_index][column_index]
                    if adjacent_square.texture_key == 'C':
                        print(f'Uncovered adjacent square: {square_grid[row_index][column_index]}')
                        adjacent_square.texture_key = current_grid.grid[row_index][column_index]
                        if adjacent_square.texture_key == '0':
                            uncover_adjacent_squares(adjacent_square.row, adjacent_square.column)
            except IndexError:
                pass


def lose_game():
    for row_index, row in enumerate(current_grid.grid):
        for column_index, column in enumerate(row):
            if column == 'X':
                square_grid[row_index][column_index].texture_key = 'X'


def draw_window():
    if game_active:  # game board
        WIN.fill(BLACK)

        square_group.draw(board)
        square_group.update()
        WIN.blit(board, board_rect)

        pygame.display.update()
    else:  # menu screen
        WIN.fill(WHITE)
        pygame.display.update()


square_group = pygame.sprite.Group()
square_grid = []

modifiers = [-1, 0, 1]

WIN.fill(BLACK)
board = pygame.Surface((width - 100, height - 100))
board_rect = board.get_rect(center=((width / 2), (height / 2)))
for row in range(DEFAULT_ROWS):
    y = row * (board_rect.height / DEFAULT_ROWS)
    square_grid.append([])
    for column in range(DEFAULT_COLUMNS):
        x = column * (board_rect.width / DEFAULT_COLUMNS)
        square = Square(x, y, int(board_rect.width / DEFAULT_COLUMNS), row, column)
        board.blit(square.image, square.rect)
        square_group.add(square)
        square_grid[row].append(square)


clock = pygame.time.Clock()

while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                buttons = pygame.mouse.get_pressed()
                x = x - board_rect.left
                y = y - board_rect.top
                pos = x, y
                print(f'mousedown at ({x}, {y})')


                # bad search, make binary
                for row_index, row in enumerate(square_grid):
                    if row[0].rect.top <= y < row[0].rect.bottom:
                        for column_index, square in enumerate(row):
                            if square.rect.left <= x < square.rect.right:
                                try:
                                    if buttons[0] and square.texture_key != 'F':
                                        square.texture_key = current_grid.grid[square.row][square.column]
                                        if square.texture_key == '0':
                                            uncover_adjacent_squares(square.row, square.column)
                                        elif square.texture_key == 'X':
                                            lose_game()

                                    elif buttons[2]:
                                        square.texture_key = 'F'
                                    break
                                except NameError:
                                    initial_tile = (square.row, square.column)
                                    current_grid = Grid(DEFAULT_COLUMNS, DEFAULT_ROWS, DEFAULT_MINES, initial_tile)
                                    print(current_grid)
                                    square.texture_key = current_grid.grid[square.row][square.column]
                                    if square.texture_key == '0':
                                        uncover_adjacent_squares(square.row, square.column)
                                    break

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True

        draw_window()
pygame.quit()
