import sys

import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE
from checkers.game import Game
from checkers.minimax.algorithm import minimax

FPS = 60
showThinking = False  # Setting this to True will show the game's thinking process
difficulty = 3  # 1 = Easy, 2 = Normal, 3 = Advanced, 4 = Expert

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), difficulty, WHITE, game, showThinking)
            game.ai_move(new_board)

        # Better way to visualize the winner on the terminal
        if game.winner() is not None:
            print("The winner is: ")
            if game.winner() == (255, 255, 255):
                print("White")
            else:
                print("Red")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.time.delay(500)  # Delay before closing game
    pygame.quit()


main()
