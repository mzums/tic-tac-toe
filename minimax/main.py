import numpy as np
from random import choice

board_size = 3
current_state = np.array([[0, 0, 0], 
                          [0, 0, 0], 
                          [0, 0, 0]])


HUMAN = -1
AI = 1

def get_possible_moves(state):
    possible_moves = []
    for i in range(board_size):
        for j in range(board_size):
            if state[i][j] == 0:
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
    return [player, player, player] in win_state

def is_game_over(state):
    return check_winner(state, HUMAN) or check_winner(state, AI) or len(get_possible_moves(state)) == 0

def get_score(state, depth):
    if check_winner(state, AI):
        return 10 - depth
    elif check_winner(state, HUMAN):
        return depth - 10
    else:
        return 0

def minimax(current_state, depth, player):
    #print(current_state)
    if depth == 0 or is_game_over(current_state):
        return (-1, -1), get_score(current_state, depth)

    best_move = (-1, -1)
    
    if player == AI:
        best_score = -1000
        for x, y in get_possible_moves(current_state):
            current_state[x][y] = player
            _, score = minimax(current_state, depth - 1, -player)
            current_state[x][y] = 0  # Undo move
            
            if score > best_score:
                best_score = score
                best_move = (x, y)
    else:
        best_score = 1000
        for x, y in get_possible_moves(current_state):
            current_state[x][y] = player
            _, score = minimax(current_state, depth - 1, AI)
            current_state[x][y] = 0  # Undo move
            
            if score < best_score:
                best_score = score
                best_move = (x, y)

    return best_move, best_score

def AIturn():
    possible_moves = get_possible_moves(current_state)
    depth = len(possible_moves)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move, _ = minimax(current_state, 9, AI)
        x, y = move
        print(x, y)

    current_state[x][y] = AI


def human_turn():
    """
    The Human plays choosing a valid move.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    possible_moves = get_possible_moves(current_state)
    depth = len(possible_moves)

    if depth == 0 or is_game_over(current_state):
        return
    
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            current_state[coord[0]][coord[1]] = HUMAN

        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


if __name__ == '__main__':
    possible_moves = get_possible_moves(current_state)
    while len(possible_moves) > 0 and not is_game_over(current_state):
        AIturn()
        print(current_state)
        human_turn()

    print(current_state)