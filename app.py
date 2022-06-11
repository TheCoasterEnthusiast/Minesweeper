import pygame

from typing import Dict

from grid import Grid
from square import Square
from storage import get_scores, write_new_score, get_question_deque

pygame.font.init()

# Default configuration
width, height = 900, 500
GAME_NAME = 'Minesweeper'
modifiers = [-1, 0, 1]
letters = ['a', 'b', 'c', 'd']
FPS = 60
DEFAULT_ROWS = 10
DEFAULT_COLUMNS = 20
DEFAULT_MINES = 30
hearts = 3
current_mines = DEFAULT_MINES
start_time = 0
pause_time = 0
pause_start_time = 0
pause_end_time = 0
score = 0
current_question = Dict
game_started = False
win = False
question = False
question_answered = False
lose_game = False

run = True
game_active = False
pygame.init()
WIN = pygame.display.set_mode((width, height))
WIN_rect = WIN.get_rect()
pygame.display.set_caption(GAME_NAME)
icon = pygame.image.load('assets/bomb_icon.png')
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (110, 110, 110)
LIGHT_GRAY = (160, 160, 160)
LIGHT_BLUE = (3, 211, 252)
LIGHT_GREEN = (172, 255, 128)
LIGHT_RED = (245, 81, 81)

# Fonts
BIG_FONT = pygame.font.SysFont("helvetica", 40)
MEDIUM_FONT = pygame.font.SysFont("helvetica", 30)
SMALL_FONT = pygame.font.SysFont("helvetica", 20)
SUPER_SMALL_FONT = pygame.font.SysFont("helvetica", 14)

# Starting screen
background = pygame.image.load('assets/title.png').convert_alpha()
instructions_text = SMALL_FONT.render("Press space to play!", True, BLACK)

# Game screen
time_text = MEDIUM_FONT.render("0 sec", True, WHITE)
time_text_rect = time_text.get_rect(center=(WIN_rect.width * .25, 27))
time_frame_rect = pygame.Rect(time_text_rect.left - 3, 13, time_text_rect.width + 6, 44)
pause_text = MEDIUM_FONT.render("0 sec", True, WHITE)
pause_text_rect = pygame.Rect(time_text_rect.left - 3, 13, time_text_rect.width + 6, 44)

heart_icon = pygame.image.load('assets/heart.png').convert_alpha()
heart_icon = pygame.transform.smoothscale(heart_icon, (40, 40))
left_heart_icon_rect = heart_icon.get_rect(center=((WIN_rect.width / 2) - 20, 25))

mine_frame_rect = pygame.Rect((WIN_rect.width * .75) - 75, 3, 105, 44)
mine_icon = pygame.image.load('assets/bomb_icon.png').convert_alpha()
mine_icon = pygame.transform.smoothscale(mine_icon, (40, 40))
mine_icon_rect = mine_icon.get_rect(center=((WIN_rect.width * .75) - 50, 25))
mine_num_text = MEDIUM_FONT.render(str(current_mines), True, WHITE)
mine_num_text_rect = mine_num_text.get_rect(center=(WIN_rect.width * .75, 27))

# win screen
win_rect = pygame.Rect(325, 75, 250, 350)
win_text = BIG_FONT.render("You Win!", True, BLACK)
win_text_rect = win_text.get_rect(center=(WIN_rect.width / 2, (WIN_rect.height / 2) - 125))
continue_text = SMALL_FONT.render("(Press space to continue)", True, BLACK)
continue_text_rect = continue_text.get_rect(center=(WIN_rect.width / 2, (WIN_rect.height / 2) + 155))

# question screen
question_rect = pygame.Rect(113, 75, WIN_rect.width * .75, 340)
answer_a_rect = pygame.Rect(133, 115, 635, 50)
answer_b_rect = pygame.Rect(133, 180, 635, 50)
answer_c_rect = pygame.Rect(133, 245, 635, 50)
answer_d_rect = pygame.Rect(133, 310, 635, 50)
box_list = [answer_a_rect, answer_b_rect, answer_c_rect, answer_d_rect]
box_dict = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D'
}
box_a_clicked = False
box_b_clicked = False
box_c_clicked = False
box_d_clicked = False
box_clicked_list = [box_a_clicked, box_b_clicked, box_c_clicked, box_d_clicked]
question_continue_text = SUPER_SMALL_FONT.render("(Press enter to continue)", True, BLACK)
question_continue_text_rect = question_continue_text.get_rect(top=answer_d_rect.bottom + 10, left=answer_d_rect.left + 400)

# lose screen
lose_text_big = MEDIUM_FONT.render('You lose!', True, BLACK)
lose_text_big_rect = lose_text_big.get_rect(center=(WIN_rect.width / 2, (WIN_rect.height / 2) - 125))
lose_text = SMALL_FONT.render('Better luck next time!', True, BLACK)
lose_text_rect = lose_text.get_rect(center=(WIN_rect.width / 2, (WIN_rect.height / 2)))


def uncover_adjacent_squares(row, column):
    for row_modifier in modifiers:
        for column_modifier in modifiers:
            row_index = row + row_modifier
            column_index = column + column_modifier
            try:
                if row_index >= 0 and column_index >= 0 and (row, column) != (row_index, column_index):
                    adjacent_square = square_grid[row_index][column_index]
                    if adjacent_square.texture_key == 'C':
                        adjacent_square.texture_key = current_grid.grid[row_index][column_index]
                        if adjacent_square.texture_key == '0':
                            uncover_adjacent_squares(adjacent_square.row, adjacent_square.column)
            except IndexError:
                pass


def check_win():
    covered = 0
    for row in square_grid:
        for square in row:
            if square.texture_key == "C" or square.texture_key == "F":
                covered += 1
    return covered == DEFAULT_MINES


def update_time() -> (pygame.Surface, pygame.Rect):
    current_time = pygame.time.get_ticks()
    game_time = (current_time - start_time) - pause_time
    game_time = "{:.2f}".format(game_time / 1000)
    time_text = MEDIUM_FONT.render(f"{game_time} sec", True, WHITE)
    time_text_rect = time_text.get_rect(center=(WIN_rect.width * .25, 27))
    return time_text, time_text_rect, game_time


def update_bomb_num(current_mines: int) -> pygame.Surface:
    return MEDIUM_FONT.render(str(current_mines), True, WHITE)


def update_time_frame_rect(text_rect: pygame.Rect) -> pygame.Rect:
    time_frame_rect = pygame.Rect(text_rect.left - 3, 3, text_rect.width + 6, 44)
    return time_frame_rect


def get_highlight_rect(text_rect: pygame.Rect) -> pygame.Rect:
    highlight_rect = pygame.Rect(text_rect.left - 5, text_rect.top - 4, text_rect.width + 10, text_rect.height + 4)
    return highlight_rect


def hover(rect, i):
    if box_clicked_list[i]:
        if current_question['answer'] == box_dict[i]:
            return LIGHT_GREEN
        else:
            return LIGHT_RED
    else:
        pos = pygame.mouse.get_pos()
        if rect.collidepoint(pos):
            return LIGHT_GRAY
        else:
            return WHITE


def lose_game_func():
    for row_index, row in enumerate(current_grid.grid):
        for column_index, column in enumerate(row):
            if column == 'X':
                square_grid[row_index][column_index].texture_key = 'X'


def draw_window(mine_num_text, score):
    if game_active:  # game board
        WIN.fill(GRAY)

        # draw board
        square_group.draw(board)
        square_group.update()
        WIN.blit(board, board_rect)

        # draw clock
        if game_started and not win and not question and not lose_game:
            player_text, player_text_rect, time = update_time()
            pygame.draw.rect(WIN, LIGHT_GRAY, update_time_frame_rect(player_text_rect), border_radius=10)
            WIN.blit(player_text, player_text_rect)
        else:
            pygame.draw.rect(WIN, LIGHT_GRAY, update_time_frame_rect(pause_text_rect), border_radius=10)
            WIN.blit(pause_text, pause_text_rect)

        # draw hearts
        for i in range(hearts):
            WIN.blit(heart_icon, heart_icon.get_rect(center=(left_heart_icon_rect.x + (i * 40), 25)))

        # draw mine icon and number
        pygame.draw.rect(WIN, LIGHT_GRAY, mine_frame_rect, border_radius=10)
        WIN.blit(mine_icon, mine_icon_rect)
        WIN.blit(mine_num_text, mine_num_text_rect)

        # draw win screen
        if win:
            pygame.draw.rect(WIN, LIGHT_BLUE, win_rect, border_radius=15)
            WIN.blit(win_text, win_text_rect)

            score_text = SMALL_FONT.render(f"Your time: {score} sec", True, BLACK)
            score_text_rect = score_text.get_rect(center=(WIN_rect.width / 2, (WIN_rect.height / 2) - 85))
            WIN.blit(score_text, score_text_rect)

            # draw past scores
            scores = get_scores(n=10)
            for i, play_time in enumerate(scores):
                num = i + 1
                text = SMALL_FONT.render(f'{num}. {scores[i]}', True, BLACK)
                if i == 0:
                    rect = text.get_rect(center=(WIN_rect.width / 2, (WIN_rect.height / 2) - 50))
                    last_rect = rect
                else:
                    rect = text.get_rect(top=last_rect.bottom, left=last_rect.left)
                    last_rect = rect
                if float(play_time) == score:
                    pygame.draw.rect(WIN, WHITE, get_highlight_rect(last_rect), border_radius=10)
                WIN.blit(text, rect)

            # draw continue text
            WIN.blit(continue_text, continue_text_rect)

        # draw question
        elif question:
            pygame.draw.rect(WIN, WHITE, question_rect, border_radius=15)

            question_text = SMALL_FONT.render(current_question['question'], True, BLACK)
            question_text_rect = question_text.get_rect(center=(WIN_rect.width / 2, 100))
            WIN.blit(question_text, question_text_rect)

            pygame.draw.rect(WIN, hover(answer_a_rect, 0), answer_a_rect, border_radius=10)
            pygame.draw.rect(WIN, hover(answer_b_rect, 1), answer_b_rect, border_radius=10)
            pygame.draw.rect(WIN, hover(answer_c_rect, 2), answer_c_rect, border_radius=10)
            pygame.draw.rect(WIN, hover(answer_d_rect, 3), answer_d_rect, border_radius=10)

            for i in letters:
                if i == 'a':
                    answer_text = SMALL_FONT.render(current_question['a'], True, BLACK)
                    answer_text_rect = answer_text.get_rect(left=150, top=130)
                    last_rect = answer_text_rect
                else:
                    answer_text = SMALL_FONT.render(current_question[i], True, BLACK)
                    answer_text_rect = answer_text.get_rect(left=150, top=last_rect.top + 65)
                    last_rect = answer_text_rect
                WIN.blit(answer_text, answer_text_rect)

            if question_answered:
                WIN.blit(question_continue_text, question_continue_text_rect)

        # draw losing screen
        elif lose_game:
            pygame.draw.rect(WIN, LIGHT_GRAY, win_rect, border_radius=15)
            WIN.blit(lose_text_big, lose_text_big_rect)
            WIN.blit(lose_text, lose_text_rect)
            WIN.blit(continue_text, continue_text_rect)

        pygame.display.update()
    else:  # menu screen
        WIN.blit(background, (0, 0))

        WIN.blit(instructions_text, ((WIN_rect.width / 2) - (instructions_text.get_width() / 2), (WIN_rect.height / 2) + 50))
        pygame.display.update()


square_group = pygame.sprite.Group()
square_grid = []

question_deque = get_question_deque()

WIN.blit(background, (0, 0))
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

                if event.key == pygame.K_RETURN and question_answered:
                    question = False
                    question_answered = False
                    box_clicked_list = [False, False, False, False]

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                buttons = pygame.mouse.get_pressed()
                x = x - board_rect.left
                y = y - board_rect.top
                pos = x, y

                if not win and not question: # disables board interaction during win or question
                    # bad search, make binary
                    for row_index, row in enumerate(square_grid):
                        if row[0].rect.top <= y < row[0].rect.bottom:
                            for column_index, square in enumerate(row):
                                if square.rect.left <= x < square.rect.right:
                                    try:
                                        # if a non-flag square is clicked, change texture
                                        if buttons[0] and square.texture_key == 'C':
                                            square.texture_key = current_grid.grid[square.row][square.column]
                                            if square.texture_key == '0':
                                                uncover_adjacent_squares(square.row, square.column)
                                            elif square.texture_key == 'X':
                                                if hearts:
                                                    hearts -= 1
                                                    question = True
                                                    current_question = question_deque.popleft()
                                                    question_deque.append(current_question)
                                                    pause_text, pause_text_rect, _ = update_time()
                                                else:
                                                    lose_game_func()
                                                    lose_game = True

                                        elif buttons[2] and square.texture_key == 'C':
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
                                        start_time = pygame.time.get_ticks()
                                        pause_time = 0
                                        pause_start_time = 0
                                        pause_end_time = 0
                                        current_mines = DEFAULT_MINES
                                        game_started = True

                                        square.texture_key = current_grid.grid[square.row][square.column]
                                        if square.texture_key == '0':
                                            uncover_adjacent_squares(square.row, square.column)
                                        break
                    if check_win():
                        win = True
                        text, rect, time = update_time()
                        score = float(time)
                        write_new_score(score)

                # if click during question mode, mark box as clicked
                elif question:
                    pos = pygame.mouse.get_pos()
                    for i, box in enumerate(box_list):
                        if box.collidepoint(pos):
                            box_clicked_list[i] = True

                            if current_question['answer'] == box_dict[i]:
                                question_answered = True

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not win and not lose_game:
                    game_active = True
                    pause_end_time = pygame.time.get_ticks()
                    if game_started:
                        pause_time += pause_end_time - pause_start_time

                elif event.key == pygame.K_SPACE and (win or lose_game):
                    win = False
                    game_active = True
                    game_started = False
                    hearts = 3
                    lose_game = False

                    # draw new board
                    square_group = pygame.sprite.Group()
                    square_grid = []

                    question_deque = get_question_deque()

                    WIN.blit(background, (0, 0))
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

                    del current_grid

    draw_window(mine_num_text, score)
pygame.quit()
