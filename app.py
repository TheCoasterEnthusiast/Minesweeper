import pygame

from grid import Grid

width, height = 900, 500
GAME_NAME = 'Minesweeper'
FPS = 60

WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption(GAME_NAME)

WHITE = (255, 255, 255)
GRID = [
    [], [], [], [], [], [], [], [], [], []
]


def generate_map():
    pass


def transform_map():
    pass


def print_map():
    pass


def draw_window():
    print_map()
    transform_map()
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window()
    pygame.quit()


if __name__ == '__main__':
    main()
    grid = Grid(10, 10, 15, (8, 5))
    print(grid)
