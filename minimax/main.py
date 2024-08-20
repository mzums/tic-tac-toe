import numpy as np
from random import choice
import platform
from os import system

board_size = 3
current_state = np.zeros((board_size, board_size))

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

def game_over(state):
    if (check_winner(state, HUMAN)):
        print('You won!')
        exit()
    elif (check_winner(state, AI)):
        print('AI won!')
        exit()
    elif len(get_possible_moves(state)) == 0:
        print('Draw!')
        exit()

def get_score(state, depth):
    if check_winner(state, AI):
        return 10 - depth
    elif check_winner(state, HUMAN):
        return depth - 10
    else:
        return 0

def minimax(current_state, depth, player):
    if depth == 0 or is_game_over(current_state):
        return (-1, -1), get_score(current_state, depth)

    best_move = (-1, -1)
    
    if player == AI:
        best_score = -1000
        for x, y in get_possible_moves(current_state):
            current_state[x][y] = player
            _, score = minimax(current_state, depth - 1, -player)
            current_state[x][y] = 0
            
            if score > best_score:
                best_score = score
                best_move = (x, y)
    else:
        best_score = 1000
        for x, y in get_possible_moves(current_state):
            current_state[x][y] = player
            _, score = minimax(current_state, depth - 1, AI)
            current_state[x][y] = 0
            
            if score < best_score:
                best_score = score
                best_move = (x, y)

    return best_move, best_score

def AIturn():
    depth = len(get_possible_moves(current_state))

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move, _ = minimax(current_state, 9, AI)
        x, y = move

    current_state[x][y] = AI


def human_turn():
    depth = len(get_possible_moves(current_state))

    if depth == 0 or is_game_over(current_state):
        return
    
    row = -1
    col = -1
    while row < 1 or row > 3 or col < 1 or col > 3:
        try:
            print('Your turn!')
            row = int(input('row (1-3): '))
            col = int(input('column (1-3): '))
            current_state[row-1][col-1] = HUMAN

        except (EOFError, KeyboardInterrupt):
            print('\nBye!')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def display(state):
    for i in range(board_size):
        print('---------------')
        print('|', end='')
        for j in range(board_size):
            if state[i][j] == -1:
                print(' X', end=' ')
            elif state[i][j] == 1:
                print(' O', end=' ')
            else:
                print('  ', end=' ')
            if j < 2: print('||', end='')
        print('|')
    print('---------------')


def clean_terminal():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


if __name__ == '__main__':
    clean_terminal()
    ans = -1

    while ans != 'y' and ans != 'n':
        try:
            ans = input('Do you want to go first? (y/n) ')
            print(ans)

        except (EOFError, KeyboardInterrupt):
            print('\nBye!')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    if ans == 'n':
        while len(get_possible_moves(current_state)) > 0 and not is_game_over(current_state):
            AIturn()
            if (is_game_over(current_state)):
                game_over(current_state)
            display(current_state)
            human_turn()
            if (is_game_over(current_state)):
                game_over(current_state)
    else:
        HUMAN = 1
        AI = -1
        while len(get_possible_moves(current_state)) > 0 and not is_game_over(current_state):
            display(current_state)
            human_turn()
            if (is_game_over(current_state)):
                game_over(current_state)
            AIturn()
            if (is_game_over(current_state)):
                game_over(current_state)

    display(current_state)