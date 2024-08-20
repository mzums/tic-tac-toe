import copy
import numpy as np

board_size = 3
current_state = np.zeros((board_size, board_size))
print(current_state[0][0])

HUMAN = -1
AI = 1

def get_possible_moves(state):
    possible_moves = []
    for i in range(board_size):
        for j in range(board_size):
            if (state[i][j] == 0):
                possible_moves.append((i, j))

    return possible_moves

def check_winner(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False
    
def is_game_over(state):
    return check_winner(state, HUMAN) or check_winner(state, AI)

def get_score(state):
    if check_winner(state, AI):
        score = +1
    elif check_winner(state, HUMAN):
        score = -1
    else:
        score = 0

    return score

def minimax(current_state, depth, player):
    possible_moves = get_possible_moves(current_state)
    
    if player == AI:
        best_move = -1, -1
        best_score = -1000000
    else:
        best_move = -1, -1
        best_score = 1000000

    if depth == 0 or is_game_over(current_state):
        score = get_score(current_state)
        #print()
        return (-1, -1), score
    
    for x, y in possible_moves:
        current_state[x][y] = player
        best_move, score = minimax(current_state, depth-1, -player)
        current_state[x][y] = 0
        best_move = x, y

        if player == AI:
            if score > best_score:
                best_score = score
                best_move = x, y
        else:
            if score < best_score:
                best_score = score
                best_move = x, y

    return best_move, best_score

def AIturn():
    move, score = minimax(current_state, 9, AI)
    return move

print(AIturn())
