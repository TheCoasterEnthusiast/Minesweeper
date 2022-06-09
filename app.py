import pygame

from grid import Grid
from square import Square

pygame.font.init()

# Default configuration
width, height = 900, 500
GAME_NAME = 'Minesweeper'
FPS = 60
DEFAULT_ROWS = 10
DEFAULT_COLUMNS = 20
DEFAULT_MINES = 30
current_mines = DEFAULT_MINES
start_time = 0
pause_time = 0
pause_start_time = 0
pause_end_time = 0
game_started = False

run = True
game_active = False
pygame.init()
WIN = pygame.display.set_mode((width, height))
WIN_rect = WIN.get_rect()
pygame.display.set_caption(GAME_NAME)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (110, 110, 110)
LIGHT_GRAY = (160, 160, 160)

# Fonts
BIG_FONT = pygame.font.SysFont("helvetica", 40)
SMALL_FONT = pygame.font.SysFont("helvetica", 20)

# Starting screen
instructions_text = SMALL_FONT.render("Press space to play!", True, BLACK)

# Game screen
time_text = BIG_FONT.render("0 sec", True, WHITE)
time_text_rect = time_text.get_rect(center=(WIN_rect.width * .25, 30))
time_frame_rect = pygame.Rect(time_text_rect.left - 3, 3, time_text_rect.width + 6, 44)

mine_frame_rect = pygame.Rect((WIN_rect.width * .75) - 75, 3, 105, 44)
mine_icon = pygame.image.load('assets/bomb_icon.png').convert_alpha()
mine_icon = pygame.transform.smoothscale(mine_icon, (40, 40))
mine_icon_rect = mine_icon.get_rect(center=((WIN_rect.width * .75) - 50, 25))
mine_num_text = BIG_FONT.render(str(current_mines), True, WHITE)
mine_num_text_rect = mine_num_text.get_rect(center=(WIN_rect.width * .75, 30))


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


def update_time() -> (pygame.Surface, pygame.Rect):
    current_time = pygame.time.get_ticks()
    game_time = (current_time - start_time) - pause_time
    game_time = "{:.2f}".format(game_time / 1000)
    time_text = BIG_FONT.render(f"{game_time} sec", True, WHITE)
    time_text_rect = time_text.get_rect(center=(WIN_rect.width * .25, 30))
    return time_text, time_text_rect


def update_bomb_num(current_mines: int) -> pygame.Surface:
    return BIG_FONT.render(str(current_mines), True, WHITE)


def update_time_frame_rect(text_rect: pygame.Rect) -> pygame.Rect:
    time_frame_rect = pygame.Rect(text_rect.left - 3, 3, text_rect.width + 6, 44)
    return time_frame_rect


def lose_game():
    for row_index, row in enumerate(current_grid.grid):
        for column_index, column in enumerate(row):
            if column == 'X':
                square_grid[row_index][column_index].texture_key = 'X'


def draw_window(mine_num_text):
    if game_active:  # game board
        WIN.fill(GRAY)

        square_group.draw(board)
        square_group.update()
        WIN.blit(board, board_rect)

        player_text, player_text_rect = update_time()
        pygame.draw.rect(WIN, LIGHT_GRAY, update_time_frame_rect(player_text_rect), border_radius=10)
        if game_started:
            WIN.blit(player_text, player_text_rect)
        else:
            WIN.blit(time_text, time_text_rect)

        pygame.draw.rect(WIN, LIGHT_GRAY, mine_frame_rect, border_radius=10)
        WIN.blit(mine_icon, mine_icon_rect)
        WIN.blit(mine_num_text, mine_num_text_rect)

        pygame.display.update()
    else:  # menu screen
        WIN.fill(WHITE)

        WIN.blit(instructions_text, ((WIN_rect.width / 2) - (instructions_text.get_width() / 2), (WIN_rect.height / 2) + 50))
        pygame.display.update()


square_group = pygame.sprite.Group()
square_grid = []

modifiers = [-1, 0, 1]


# creates initial board
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
                    pause_start_time = pygame.time.get_ticks()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                buttons = pygame.mouse.get_pressed()
                x = x - board_rect.left
                y = y - board_rect.top
                pos = x, y

                # bad search, make binary
                for row_index, row in enumerate(square_grid):
                    if row[0].rect.top <= y < row[0].rect.bottom:
                        for column_index, square in enumerate(row):
                            if square.rect.left <= x < square.rect.right:
                                try:
                                    # if a non-flag square is clicked, change texture
                                    if buttons[0] and square.texture_key != 'F':
                                        square.texture_key = current_grid.grid[square.row][square.column]
                                        if square.texture_key == '0':
                                            uncover_adjacent_squares(square.row, square.column)
                                        elif square.texture_key == 'X':
                                            lose_game()

                                    elif buttons[2] and square.texture_key != 'F':
                                        square.texture_key = 'F'
                                        current_mines -= 1
                                        mine_num_text = update_bomb_num(current_mines)
                                    elif buttons[2] and square.texture_key == 'F':
                                        square.texture_key = 'C'
                                        current_mines += 1
                                        mine_num_text = update_bomb_num(current_mines)
                                    break
                                except NameError:
                                    initial_tile = (square.row, square.column)
                                    current_grid = Grid(DEFAULT_COLUMNS, DEFAULT_ROWS, DEFAULT_MINES, initial_tile)
                                    print(current_grid)
                                    start_time = pygame.time.get_ticks()
                                    game_started = True

                                    square.texture_key = current_grid.grid[square.row][square.column]
                                    if square.texture_key == '0':
                                        uncover_adjacent_squares(square.row, square.column)
                                    break

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    pause_end_time = pygame.time.get_ticks()
                    if game_started:
                        pause_time += pause_end_time - pause_start_time

    draw_window(mine_num_text)
pygame.quit()
