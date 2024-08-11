import numpy as np

class TicTacToe:
    def __init__(self):
        self.row_count = 3
        self.column_count = 3
        self.action_size = self.row_count * self.column_count

    def get_initial_state(self):
        return np.zeros((self.row_count, self.column_count))

    def get_next_state(self, state, action, player):
        row = action //self.column_count
        column = action % self.column_count
        state[row][column] = player
        return state
    
    def get_valid_moves(self, state):
        return (state.reshape(-1) == 0).astype(np.uint8)
    
    def check_win(self, state, action):
        row = action // self.column_count
        column = action % self.column_count
        player = state[row][column]

        return (
            np.sum(state[row, :]) == player * self.column_count
            or np.sum(state[:, column]) == player * self.row_count
            or np.sum(np.diag(state)) == player * self.row_count
            or np.sum(np.diag(np.flip(state, axis=0))) == player * self.row_count
        )
    
    def get_value_and_terminated(self, state, action):
        if self.check_win(state, action):
            return 1, True
        if np.sum(self.get_valid_moves(state)) == 0:
            return 0, True
        return 0, False
    
    def get_opponent(self, player):
        return -player
    
if __name__ == "__main__":
    game = TicTacToe()
    state = game.get_initial_state()
    player = 1

    while True:
        print(state)
        valid_moves = game.get_valid_moves(state)
        print("valid moves", [i for i in range (game.action_size) if valid_moves[i]])
        action = int(input(f"{player}: "))

        if (valid_moves[action] == 0):
            print("Invalid move")
            continue

        state = game.get_next_state(state, action, player)
        value, terminated = game.get_value_and_terminated(state, action)

        if terminated:
            print(state)
            if value == 1:
                print(f"{player} wins!")
            else:
                print("Draw!")
            break

        player = game.get_opponent(player)