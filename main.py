import pygame
from time import time

from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE
from checkers.game import Game
from checkers.minimax.algorithm import minimax

FPS = 60
########################################################################################################################
# Setting this to True will show the game's thinking process.
# This will slow game progression and is only for cosmetic purposes.
showThinking = False
########################################################################################################################

########################################################################################################################
# WARNING: USE AT YOUR OWN RISK. COMPUTATION TIME WILL GROW EXPONENTIALLY DEPENDING ON THE AMOUNT OF PIECES REMAINING.
# AN AVERAGE COMPUTER MAY NOT BE ABLE TO HANDLE ALL RECURSION CALLS.
# THE AUTHORS OF THIS CODE ARE NOT RESPONSIBLE FOR ANY DAMAGE CAUSED TO COMPUTERS BY ITS EXECUTION.
# Disabling this turns the algorithm into a standard Alpha-Beta Pruning
enableCutoff = True
########################################################################################################################

########################################################################################################################
# Sets the difficulty for the AI. Increased difficulty implies more possibilities analyzed and will cause the AI
# to take more time before performing a move.
# This setting only works when cutoff is enabled (i.e. enableCutoff = True)
# 1 = Easy, 2 = Normal, 3 = Advanced
difficulty = 2
########################################################################################################################


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
            if not enableCutoff:
                time1 = float(time())
                value, new_board = minimax(game.get_board(), game.get_max_depth(), WHITE, game, showThinking)
                if new_board is None:  # This means there is no new board because there are no more plays
                    game.change_turn()  # Changing turn because winner is the opposite player
                    if game.turn == (255, 255, 255):
                        print("The game winner is White")
                    else:
                        print("The game winner is Red")
                    break
            else:
                time1 = float(time())
                value, new_board = minimax(game.get_board(), difficulty + 1, WHITE, game, showThinking)
                if new_board is None:  # This means there is no new board because there are no more plays
                    game.change_turn()  # Changing turn because winner is the opposite player
                    if game.turn == (255, 255, 255):
                        print("The game winner is White")
                    else:
                        print("The game winner is Red")
                    break
            game.ai_move(new_board)
            time2 = float(time())
            print("Time taken: " + str(round(time2 - time1, 3)) + " seconds")
        # Better way to visualize the winner on the terminal
        if game.winner() is not None:
            if game.winner() == (255, 255, 255):
                print("The game winner is White")
            else:
                print("The game winner is Red")
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
