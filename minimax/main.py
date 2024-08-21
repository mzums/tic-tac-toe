#!/usr/bin/env python3
import numpy as np
import platform
from os import system
from math import inf


HUMAN = -1
AI = 1
BOARD_SIZE = 3
current_state = np.zeros((BOARD_SIZE, BOARD_SIZE))


def get_possible_moves(state):
    possible_moves = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
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
    elif (check_winner(state, AI)):
        print('AI won!')
    elif len(get_possible_moves(state)) == 0:
        print('Draw!')

    display(current_state)
    exit()


def get_score(state, depth):
    if check_winner(state, AI):
        return 10 - depth
    elif check_winner(state, HUMAN):
        return depth - 10
    else:
        return 0


def minimax(current_state, depth, player, alpha, beta):
    best_move = (-1, -1)
    
    if depth == 0 or is_game_over(current_state):
        return best_move, get_score(current_state, depth)
    
    if player == AI:
        best_score = -inf
        for x, y in get_possible_moves(current_state):
            current_state[x][y] = player
            _, score = minimax(current_state, depth - 1, -player, alpha, beta)
            current_state[x][y] = 0
            
            if score > best_score:
                best_score = score
                best_move = (x, y)

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # Beta cut-off
    else:
        best_score = inf
        for x, y in get_possible_moves(current_state):
            current_state[x][y] = player
            _, score = minimax(current_state, depth - 1, AI, alpha, beta)
            current_state[x][y] = 0
            
            if score < best_score:
                best_score = score
                best_move = (x, y)

            beta = min(beta, best_score)
            if beta <= alpha:
                break  # Alpha cut-off

    return best_move, best_score


def AIturn():
    move, _ = minimax(current_state, 9, AI, -1000, 1000)
    x, y = move
    current_state[x][y] = AI


def human_turn():
    possible_moves = get_possible_moves(current_state)
    depth = len(possible_moves)
    if depth == 0 or is_game_over(current_state):
        return
    
    row, col = -1, -1
    while row < 1 or row > BOARD_SIZE or col < 1 or col > BOARD_SIZE or (row-1, col-1) not in possible_moves:
        row, col = interact(move_question)


def display(state):
    symbols = {-1: 'X', 1: 'O', 0: ' '}
    for i in range(BOARD_SIZE):
        print('---------------')
        print('|', end=' ')
        for j in range(BOARD_SIZE):
            print(symbols[state[i][j]], end=' ')
            if j < 2: print('||', end=' ')
        print('|')
    print('---------------')


def clean_terminal():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def player_turn(player):
    if player == human_turn:
        display(current_state)
    player()
    if (is_game_over(current_state)):
        game_over(current_state)


def game(player1, player2):
    while len(get_possible_moves(current_state)) > 0 and not is_game_over(current_state):
        player_turn(player1)
        player_turn(player2)


def first_question():
    ans = input('Do you want to go first? (y/n) ')
    return ans

def move_question():
    print('Your turn!')
    row = int(input('row (1-3): '))
    col = int(input('column (1-3): '))
    current_state[row-1][col-1] = HUMAN
    return row, col

def interact(func):
    try:
        return func()
    except (EOFError, KeyboardInterrupt):
        print('\nBye!')
        exit()
    except (KeyError, ValueError):
        print('Bad choice')


if __name__ == '__main__':
    clean_terminal()
    ans = -1

    while ans != 'y' and ans != 'n':
        ans = interact(first_question)

    if ans == 'n':
        game(AIturn, human_turn)
    else:
        game(human_turn, AIturn)