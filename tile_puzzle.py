import numpy as np
from enum import Enum

class Action(Enum):
    '''
    Actions are with respect to the "empty" tile. So Action.U denotes the empty
    tile moving up a slot
    '''
    U = 1
    R = 2
    D = 3
    L = 4

CONVERT_ACTION = {
    Action.U: (-1, 0),
    Action.R: (0, 1),
    Action.D: (1, 0),
    Action.L: (0, -1),
}

def new_tile_loc(tile, action):
    if action not in CONVERT_ACTION:
        raise Exception, '{} is not an action!'.format(action)

    move = CONVERT_ACTION[action]
    other_tile = (tile[0] + move[0], tile[1] + move[1])
    return other_tile

class TilePuzzle(object):
    def __init__(self, size):
        self.size = size
        self.grid = np.arange(size*size, dtype=np.int8).reshape(size, size)
        self.empty_tile = (0, 0)

    def move(self, action):
        assert self.legal_move(action), \
            '{} is not a legal move when the empty tile is at {}'.format(action, self.empty_tile)
        print('Moving the empty tile {}'.format(action))
        other_tile = new_tile_loc(self.empty_tile, action)
        self.swap(other_tile, self.empty_tile)
        self.empty_tile = other_tile

    def swap(self, loc1, loc2):
        self.grid[loc1], self.grid[loc2] = self.grid[loc2], self.grid[loc1]

    def legal_move(self, action):
        loc = new_tile_loc(self.empty_tile, action)
        return (0 <= loc[0] < self.size) and (0 <= loc[1] < self.size)

    def render(self):
        print(self.grid)

    def legal_moves(self):
        return [a for a in Action if self.legal_move(a)]

    def random_shuffle(self, moves):
        for _ in range(moves):
            legal_moves = self.legal_moves()
            action = np.random.choice(legal_moves)
            self.move(action)

if __name__ == '__main__':
    puzzle = TilePuzzle(4)
    puzzle.render()
    puzzle.random_shuffle(2)
    puzzle.render()
