"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

#This is the initial state of the board with all the cells empty
def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# This function returns the player who has to play next by counting the number of X's and O's on the board and returning the player with less number of moves and keeping X as the first player
def player(board):
    counterx = 0
    countery = 0
    ecounter = 0
    for i in range (len(board)):
        for j in range (len(board)):
            if board[i][j] == X:
                counterx +=1
            elif board[i][j] == O:
                countery +=1

    if counterx > countery :
        return O
    else:
        return X
# This function returns the set of all possible actions (i, j) available on the board by checking if the cell is empty or not and returning the set of empty cells
def actions(board):
    a = set()
    for i in range (len(board)):
        for j in range (len(board)):
            if board[i][j] == EMPTY:
                a.add((i,j))
    if len(a) == 0:
        return 1
    else:
        return a

# This function returns the board that results from making move (i, j) on the board by making a deepcopy of the board and then checking if the cell is empty or not and then making the move
def result(board, action):
    a = deepcopy(board)
    i= action[0] 
    j = action[1]

    if a[i][j] != EMPTY:
        raise NameError('Invalid action')
    else:
        a[i][j] = player(board)
    return a

# This function returns True if X has won the game, False if O has won the game, or None if the game has not yet been won by checking the rows, columns and diagonals


def winner(board):
    for i in range (len(board)):
        if board[i][0] == board[i][1] == board[i][2] == X:
            return X
        elif board[i][0] == board[i][1] == board[i][2] == O:
            return O
        elif board[0][i] == board[1][i] == board[2][i] == X:
            return X
        elif board[0][i] == board[1][i] == board[2][i] == O:
            return O
    if board[0][0] == board[1][1] == board[2][2] == X:
        return X
    elif board[0][0] == board[1][1] == board[2][2] == O:
        return O
    elif board[0][2] == board[1][1] == board[2][0] == X:
        return X
    elif board[0][2] == board[1][1] == board[2][0] == O:
        return O
    else:
        return None
# This function returns True if the game is over, False otherwise by checking if the board is full or if there is a winner
def terminal(board):
    if winner(board) == X or winner(board) == O:
        return True
    else:
        for i in range (len(board)):
            for j in range (len(board)):
                if board[i][j] == EMPTY:
                    return False
        return True
# This function returns the utility of the board by checking if the winner is X or O or if it is a tie and returning the utility accordingly
def utility(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0
# This function returns the optimal action for the current player on the board by checking if the board is terminal or not and then calling the max_value and min_value functions accordingly
def max_value(board):
        if terminal(board) == True:
            return utility(board)
        v = -math.inf
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v
def min_value(board):
        if terminal(board) == True:
            return utility(board)
        v = math.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v
def minimax(board):
    if terminal(board) == True:
        return None
    elif player(board) == X:
        plays =[]
        for action in actions(board):
            plays.append([ min_value(result(board, action)) , action])
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1]
    elif player(board) == O:
        plays =[]
        for action in actions(board):
            plays.append([ max_value(result(board, action)) , action])
        return sorted(plays, key=lambda x: x[0], reverse=False)[0][1]
            
            
