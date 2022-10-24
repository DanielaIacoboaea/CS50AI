"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def occurrences(board, variable):
    """
    Returns the number of occurrences on the board for
    the variable provided 
    """
    return sum([line.count(variable) for line in board])


def generate_cells_idx(board, variable):
    """
    Returns a set of index pairs(i, j) for each cell 
    that contains the variable 
    """

    # Initialize an empty set
    cells_idx = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == variable:
               cells_idx.add((i,j))

    return cells_idx 



def row_moves(moves):
    """
    Count all the moves made by variable (X or O) horizontally  
    Moves is a set of (i, j) pairs for each cell where the variable made a move  
    """

    # keep track of all lines where the variable made a move
    lines = []

    for move in moves:
        lines.append(move[0])
    
    # if the variable occurs 3 times on one line
    # we found a winner
    if lines.count(0) == 3:
        return True
    if lines.count(1) == 3:
        return True
    if lines.count(2) == 3:
        return True
    
    # otherwise keep playing
    return False


def cols_moves(moves):
    """
    Count all the moves made by variable (X or O) vertically
    Moves is a set of (i, j) pairs for each cell where the variable made a move  
    """

    # keep track of all lines where the variable made a move
    cols = []

    for move in moves:
        cols.append(move[1])
    
    # if the variable occurs 3 times on one column
    # we found a winner
    if cols.count(0) == 3:
        return True
    if cols.count(1) == 3:
        return True
    if cols.count(2) == 3:
        return True
    
    # otherwise keep playing
    return False


def diag_prim_moves(moves):
    """
    Count all the moves made by variable (X or O) for primary diagonal
    Moves is a set of (i, j) pairs for each cell where the variable made a move  
    """

    # check if all primary diagonal coordonates
    # are in the set of the moves received
    diag_prim = {(0,0), (1,1), (2,2)}

    diag_is_in_moves = diag_prim.issubset(moves)

    return diag_is_in_moves



def diag_sec_moves(moves):
    """
    Count all the moves made by variable (X or O) for secondary diagonal
    Moves is a set of (i, j) pairs for each cell where the variable made a move  
    """

    # check if all secondary diagonal coordonates
    # are in the set of the moves received
    diag_sec = {(0,2), (1,1), (2,0)}

    diag_is_in_moves = diag_sec.issubset(moves)

    return diag_is_in_moves


def max_value(board):
    """
    Returns best move and utility value for X (Max) player
    """

    if terminal(board):
        return None, utility(board)
    value = -math.inf
    best_move = None

    # keep track of action that leads to value change 
    # save it in best_move
    for action in actions(board):
        new_move, new_value = min_value(result(board, action))
        if max(value, new_value) is not value:
            value = new_value
            best_move = action
    return best_move, value



def min_value(board):
    """
    Returns best move and utility value for O (Min) player
    """

    if terminal(board):
        return None, utility(board)
    value = math.inf
    best_move = None

    # keep track of action that leads to value change 
    # save it in best_move
    for action in actions(board):
        new_move, new_value = max_value(result(board, action))
        if min(value, new_value) is not value:
            value = new_value
            best_move = action
    return best_move, value



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

    # count turns that have already been taken by each player
    # Cases:
    # 1. Empty board -> Turn: X
    # 2. X has an extra turn -> Turn: O
    # 3. Equal turns -> Turn: X
    count_EMPTY = occurrences(board, EMPTY)
    turns_X = occurrences(board, X)
    turns_O  = occurrences(board, O)

    if count_EMPTY == 9:
        return X
    elif turns_O == turns_X - 1:
        return O
    elif turns_O == turns_X:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_actions = generate_cells_idx(board, EMPTY)

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # create a new state of the board
    new_board_state = deepcopy(board)
    i = action[0]
    j = action[1]
    if not new_board_state[i][j] == EMPTY:
        raise ValueError("Cell is not empty")

    if i < 0 or i > 2:
        raise ValueError("Invalid board index")
    
    if j < 0 or j > 2:
        raise ValueError("Invalid board index")

    # change the cell according to the input action 
    new_board_state[i][j] = player(board)

    return new_board_state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # search the winner of the game based on the state of the game
    count_EMPTY = occurrences(board, EMPTY)
    turns_X = occurrences(board, X)
    turns_O  = occurrences(board, O)

    # empty board -> no winner
    if count_EMPTY == 9:
        return None    
    
    # X and O made less than 3 moves -> game in progress
    if turns_X < 3 and turns_O < 3:
        return None

    # check if X is the winner 
    if turns_X >= 3:
        moves_X = generate_cells_idx(board, X)
        if row_moves(moves_X) or cols_moves(moves_X) or diag_prim_moves(moves_X) or diag_sec_moves(moves_X):
            return X

    # check if O is the winner
    if turns_O >= 3:
        moves_O = generate_cells_idx(board, O)
        if row_moves(moves_O) or cols_moves(moves_O) or diag_prim_moves(moves_O) or diag_sec_moves(moves_O):
            return O

    # don't have a winner for this board state
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # found winner -> board is in terminal state 
    # no winner and no empty cells left for other moves -> board is in terminal state 
    # otherwise, the game can continue
    get_winner = winner(board)
    if get_winner == X or get_winner == O:
        return True
    elif occurrences(board, EMPTY) == 0:
        return True
    else:
        return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    # get the optimal move based on player
    if player(board) == X:
        optimal_move, value = max_value(board)
    else:
        optimal_move, value = min_value(board)

    return optimal_move

