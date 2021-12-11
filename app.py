import pygame

from grid import Grid
from square import Square

width, height = 900, 500
GAME_NAME = 'Minesweeper'
FPS = 60
DEFAULT_ROWS = 10
DEFAULT_COLUMNS = 20
DEFAULT_MINES = 50

run = True
game_active = True
pygame.init()
WIN = pygame.display.set_mode((width, height))
WIN_rect = WIN.get_rect()
pygame.display.set_caption(GAME_NAME)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw_window():
    if game_active:  # game board
        WIN.fill(BLACK)

        #board.fill((255, 0, 0))
        #list = square_group.sprites()
        #board.blit(list[0].image, list[0].rect)
        square_group.draw(board)
        square_group.update()
        WIN.blit(board, board_rect)

        pygame.display.update()
    else:  # menu screen
        WIN.fill(WHITE)
        pygame.display.update()


square_group = pygame.sprite.Group()
square_list = []

WIN.fill(BLACK)
board = pygame.Surface((width - 100, height - 100))
board_rect = board.get_rect(center=((width / 2), (height / 2)))
for row in range(DEFAULT_ROWS):
    y = row * (board_rect.height / DEFAULT_ROWS)
    for column in range(DEFAULT_COLUMNS):
        x = column * (board_rect.width / DEFAULT_COLUMNS)
        square = Square(x, y, int(board_rect.width / DEFAULT_COLUMNS), row, column)
        board.blit(square.image, square.rect)
        square_group.add(square)
        square_list.append(square)


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
                x = x - (board_rect.left - WIN_rect.left)
                y = y - (board_rect.top - WIN_rect.top)
                pos = x, y
                print('mousedown')
                for square in square_list:
                    if square.check_if_clicked_on(pos):
                        try:
                            if buttons[0] and square.texture_key != 'F':
                                square.texture_key = current_grid.grid[square.row][square.column]
                                if square.texture_key == 'X':
                                    pass
                            elif buttons[2]:
                                square.texture_key = 'F'
                        except NameError:
                            initial_tile = (square.row, square.column)
                            current_grid = Grid(DEFAULT_COLUMNS, DEFAULT_ROWS, DEFAULT_MINES, initial_tile)
                            print(current_grid)
                            square.texture_key = current_grid.grid[square.row][square.column]
                            break

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True

        draw_window()
pygame.quit()




grid = Grid(DEFAULT_COLUMNS, DEFAULT_ROWS, DEFAULT_MINES, (1, 1))
print(grid)
