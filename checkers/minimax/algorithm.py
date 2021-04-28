from copy import deepcopy
import random

import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)


# Implementation of the minimax algorithm
# It is given the position of the current piece, depth and the current state of the game
# to determine the value and store it in the possible moves it can make.
def minimax(position, depth, max_player, game, showThinking):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        currentMax = maxEval
        best_move = []
        # This loop grabs all available moves and evaluates them and adds them to best_move array
        for move in get_all_moves(position, WHITE, game, showThinking):
            evaluation = minimax(move, depth - 1, False, game, showThinking)[0]
            maxEval = max(maxEval, evaluation)
            if currentMax < maxEval:
                currentMax = maxEval
                best_move.clear()
            if maxEval == evaluation:
                best_move.append(move)
        rand = random.randint(0, max(0, len(best_move) - 2))  # Chooses one of the best moves at random
        if len(best_move) == 0:
            return maxEval, None
        else:
            return maxEval, best_move[rand]
    else:
        minEval = float('inf')
        currentMin = minEval
        best_move = []
        for move in get_all_moves(position, RED, game, showThinking):
            evaluation = minimax(move, depth - 1, True, game, showThinking)[0]
            minEval = min(minEval, evaluation)
            if currentMin > minEval:
                currentMin = minEval
                best_move.clear()
            if minEval == evaluation:
                best_move.append(move)
        rand = random.randint(0, max(0, len(best_move) - 1))  # Chooses one of the best moves at random
        if len(best_move) == 0:
            return minEval, None
        else:
            return minEval, best_move[rand]


def get_all_moves(board, color, game, showThinking):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            if showThinking:
                draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)

    return moves


def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(50)
