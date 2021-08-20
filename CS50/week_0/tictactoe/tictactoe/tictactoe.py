"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None
optimal_action = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    next_player = None
    # No next player if the board is in a terminal state
    if not terminal(board):
        # Enumerating numbers of each player
        for row in board:
            for square in row:
                if square == O:
                    o_count += 1
                elif square == X:
                    x_count += 1
        # Decide who players are based on counts
        if x_count > o_count:
            next_player = O
        else:
            next_player = X
    return next_player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    if not terminal(board):
        for row in board:  # Enumerating numbers of each player
            for square in row:
                if square is EMPTY:
                    moves.add((board.index(row), row.index(square)))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (r, j) on the board.
    """
    new_board = deepcopy(board)
    r, c = action
    if (r < 0 or r > 2) or (c < 0 or c > 2):
        raise
    new_board[r][c] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winning_player = None
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2]:
            winning_player = row[0]
    # Check cols
    for col_index in range(3):
        if board[0][col_index] == board[1][col_index] == board[2][col_index]:
            winning_player = board[0][col_index]
    # Check diags
    if board[0][0] == board[1][1] == board[2][2]:
        winning_player = board[0][0]
    elif board[0][2] == board[1][1] == board[2][0]:
        winning_player = board[0][2]
    return winning_player


def filled(board):
    empty_count = 0
    for row in board:
        for col in row:
            if col == EMPTY:
                empty_count += 1
    return empty_count == 0


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return (winner(board) == X or winner(board) == O) or filled(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)
    if winning_player == X:
        return 1
    elif winning_player == O:
        return -1
    else:  # Draw
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    global optimal_action
    optimal = None
    if not terminal(board):
        if player(board) == O:
            minimise(board)
            optimal = optimal_action
        elif player(board) == X:
            maximise(board)
            optimal = optimal_action
    return optimal


def minimise(board):
    global optimal_action
    if terminal(board):
        return utility(board)
    v = float("inf")
    for action in actions(board):
        temp = v
        v = min(v, maximise(result(board, action)))
        if v != temp:
            optimal_action = action
    return v


def maximise(board):
    global optimal_action
    if terminal(board):
        return utility(board)
    v = float("-inf")
    for action in actions(board):
        temp = v
        v = max(v, minimise(result(board, action)))
        if v != temp:
            optimal_action = action
    return v
