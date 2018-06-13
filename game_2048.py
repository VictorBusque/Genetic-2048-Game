import numpy as np
import random
from copy import deepcopy as cp


class Game_2048(object):

    def __init__(self, seed = 22):
        self.random_game = random.Random()
        self.random_game.seed(seed)
        self.steps = 0
        self.board = np.zeros((4,4))
        self.seed = seed
        self.board[self.random_game.randint(0, 3), self.random_game.randint(0, 3)] = 2
        x, y = self.random_game.randint(0, 3), self.random_game.randint(0, 3)
        while (self.board[x,y] == 2): x, y = self.random_game.randint(0, 3), self.random_game.randint(0, 3)
        self.board[x, y] = 2
        self.score = 0

    def __repr__(self):
        return str(self.board)

    def get_score(self):
        return self.score

    def match_ended(self):
        if 0 in self.board: return False
        else:
            for row in range(0, 4):
                for col in range(0,4):
                    cell = self.board[row,col]
                    if self.position_ok(row+1, col):
                        if cell == self.board[row+1,col]: return False
                    if self.position_ok(row-1, col):
                        if cell == self.board[row-1,col]: return False
                    if self.position_ok(row, col+1):
                        if cell == self.board[row,col+1]: return False
                    if self.position_ok(row, col-1):
                        if cell == self.board[row,col-1]: return False
            return True

    def add_random_two(self):
        if not 0 in self.board:
            pass
        else:
            x, y = self.random_game.randint(0, 3), self.random_game.randint(0, 3)
            while (self.board[x,y] != 0): x, y = self.random_game.randint(0, 3), self.random_game.randint(0, 3)
            self.board[x, y] = 2

    def position_ok(self, x, y):
        return (0 <= x <= 3) & (0 <= y <= 3)

    def merge(self, dir):
        off_col = 0; off_row = 0;
        col_limit = list(range(0,4)); row_limit = list(range(0,4));
        if dir == 'left':
            off_col = -1
            col_limit = list(range(1,4))
        elif dir == 'right':
            off_col = 1
            col_limit = list(range(0,3))
        elif dir == 'up':
            off_row = -1
            row_limit = list(range(1,4))
        else:
            off_row = 1
            row_limit = list(range(0,3))
        for col in col_limit:
            for row in row_limit:
                if self.board[row, col] == 0: pass
                elif self.board[row, col] == self.board[row+off_row, col+off_col]:
                    score = self.board[row+off_row, col+off_col] * 2
                    self.board[row+off_row, col+off_col] = score
                    self.score += score
                    self.board[row, col] = 0


    def movement(self, dir):
        off_col = 0; off_row = 0;
        col_limit = list(range(0,4)); row_limit = list(range(0,4));
        if dir == 'left':
            off_col = -1
            col_limit = list(range(1,4))
        elif dir == 'right':
            off_col = 1
            col_limit = list(range(0,3))[::-1]
        elif dir == 'up':
            off_row = -1
            row_limit = list(range(1,4))
        else:
            off_row = 1
            row_limit = list(range(0,3))[::-1]
        for col in col_limit:
            for row in row_limit:
                if self.board[row, col] == 0: pass
                else:
                    aux_row = row+off_row
                    aux_col = col+off_col
                    while self.position_ok(aux_row, aux_col):
                        if self.board[aux_row, aux_col] == 0:
                            self.board[aux_row, aux_col] = self.board[aux_row-off_row, aux_col-off_col]
                            self.board[aux_row-off_row, aux_col-off_col] = 0
                            aux_row+=off_row
                            aux_col+=off_col
                        else: break

    """
        movement:
            [1,0,0,0] -> left
            [0,1,0,0] -> up
            [0,0,1,0] -> down
            [0,0,0,1] -> right
    """
    def move(self, movement):
        if movement[0] == 1: dir = 'left'
        elif movement[1]  == 1: dir = 'up'
        elif movement[2]  == 1: dir = 'down'
        else: dir = 'right'
        prev_score = self.score
        self.merge(dir)
        self.movement(dir)
        if self.match_ended():
            pass
        else:
            self.steps += 1
            self.add_random_two()


    def simulate_game(self, movements):
        for movement in movements:
            if self.match_ended(): break
            else:
                self.move(movement)

