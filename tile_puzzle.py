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
    def __init__(self, size, grid=None, empty_tile=None):
        self.size = size

        if grid is None:
            self.grid = np.arange(size*size, dtype=np.int8).reshape(size, size)
            self.empty_tile = (0, 0)
        else:
            self.grid = grid
            self.empty_tile = empty_tile


    def move(self, action, verbose=False):
        assert self.legal_move(action), \
            '{} is not a legal move when the empty tile is at {}'.format(action, self.empty_tile)
        other_tile = new_tile_loc(self.empty_tile, action)

        if verbose:
            print('Taking action: {} | empty tile moving from {} -> {}'.format(
                action, self.empty_tile, other_tile))

        self.swap(other_tile, self.empty_tile)
        self.empty_tile = other_tile
        assert self.grid[self.empty_tile] == 0

    def swap(self, loc1, loc2):
        self.grid[loc1], self.grid[loc2] = self.grid[loc2], self.grid[loc1]

    def legal_move(self, action):
        loc = new_tile_loc(self.empty_tile, action)
        return (0 <= loc[0] < self.size) and (0 <= loc[1] < self.size)

    def render(self):
        print(self.grid)

    def legal_moves(self):
        return [a for a in Action if self.legal_move(a)]

    def shuffle(self, moves, verbose=False):
        for _ in range(moves):
            self.random_step(verbose)

    def manhattan_distance(self):
        # Manhattan distance from the current configuration to the solved configuration
        # TODO: maybe inefficient?
        total_dist = 0
        for i in range(self.size):
            for j in range(self.size):
                num = self.grid[i, j]
                true_pos = self.true_pos(num, self.size)
                del_x = abs(true_pos[0] - i)
                del_y = abs(true_pos[1] - j)
                total_dist += (del_x + del_y)

        return total_dist

    @staticmethod
    def true_pos(num, size):
        '''
        Return the solved position(tuple) of the given number
        IE: tile 0 -> (0, 0) for any sized grid
            tile 5 -> (1, 1) for a 4x4 grid
        '''
        return (num // size, num % size)

    def random_step(self, verbose=False):
        '''
        Make a random move
        '''
        action = np.random.choice(self.legal_moves())
        self.move(action, verbose)

    def load_grid(self, grid):
        assert grid.shape[0] == grid.shape[1], 'Grid shape {} is not square!'.format(grid.shape)
        self.size = grid.shape[0]
        self.grid = grid.astype(np.int8)

        loc_zero = np.where(x == 0)
        self.empty_tile = (loc_zero[0][0], loc_zero[1][0])

    def load_vector(self, vector):
        size = int(np.sqrt(len(vector)))
        assert(size * size == len(vector))

        grid = vector.reshape(size, size)
        self.load_grid(grid)

    @staticmethod
    def gen_puzzle(puzzle, action):
        new_grid = puzzle.grid.copy()
        et = puzzle.empty_tile
        delta = CONVERT_ACTION[action]
        other_tile = (et[0] + delta[0], et[1] + delta[1])

        # swap tiles in the new grid
        new_grid[et], new_grid[other_tile] = new_grid[other_tile], new_grid[et]
        return TilePuzzle(puzzle.size, grid=new_grid, empty_tile=other_tile)

    def successors(self):
        moves = self.legal_moves()
        children = []

        for action in moves:
            children.append(TilePuzzle.gen_puzzle(self, action))

        return children

    def done(self):
        for i in range(self.size):
            for j in range(self.size):
                num = self.grid[i, j]
                if self.true_pos(num, self.size) != (i, j): return False

        return True

if __name__ == '__main__':
    size = 4
    puzzle = TilePuzzle(size)
    puzzle.move(Action.D)
    puzzle.move(Action.R)
    for p in puzzle.successors():
        p.render()
        print('=' * 10)
