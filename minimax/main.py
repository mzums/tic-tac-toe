import copy
import numpy as np

board_size = 3
current_state = np.zeros((board_size, board_size))
print(current_state[0][0])

def get_possible_moves(state):
    possible_moves = []
    for i in range(board_size * board_size):
        row = i // board_size
        col = i % board_size
        if (state[row][col] == 0):
            possible_moves.append((row, col))

    return possible_moves

def check_winner(state, action):
    if action == None:
        return False
        
    row, column = action
    
    return (
            np.sum(state[row, :]) == board_size
            or np.sum(state[:, column]) == board_size
            or np.sum(np.diag(state)) == board_size
            or np.sum(np.diag(np.flip(state, axis=0))) == board_size
        )

def dfs(current_state):
    possible_moves = get_possible_moves(current_state)
    print(current_state)
    for move in possible_moves:
        next_state = copy.deepcopy(current_state)
        next_state[move[0]][move[1]] = 1
        if (len(possible_moves) == 0 or check_winner(next_state, move)):
            print() 
            return
        dfs(next_state)


dfs(current_state)
