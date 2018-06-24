import pdb
from collections import namedtuple
from queue import PriorityQueue
from tile_puzzle import TilePuzzle

GameState = namedtuple('GameState', ['moves', 'state'])

def a_star(game, f_heuristic):
    '''
    game: a tile puzzle. Must have the following functions:
        successors()
        done:
    f_heuristic: a function mapping a game state -> real number
    '''
    to_visit = PriorityQueue()
    curr_state = GameState(0, game) # num moves taken is 0
    to_visit.put((f_heuristic(game), curr_state))

    done = False
    nodes_explored = 0
    min_heuristic = f_heuristic(game)
    sol_moves = None

    while not to_visit.empty():
        curr_fitness, game_state = to_visit.get()
        parent_moves, parent_state = game_state

        nodes_explored += 1
        if curr_fitness < min_heuristic:
            min_heuristic = curr_fitness

        if parent_state.done():
            sol_moves = parent_moves
            break

        # get all successors of the current state.
        # Their fitnesses is moves + heuristic_function(state)
        for child in parent_state.successors():
            child_prio = parent_moves + f_heuristic(child)
            child_state = GameState(parent_moves + 1, child)
            to_visit.put((child_prio, child_state))

    info = {
        'nodes_explored': nodes_explored,
        'min_heuristic': min_heuristic,
        'sol_moves': sol_moves
    }
    return info

if __name__ == '__main__':
    size = 4
    puzzle = TilePuzzle(size)
    puzzle.shuffle(40, verbose=False)
    heuristic = lambda grid: grid.manhattan_distance()

    info = a_star(puzzle, heuristic)
    print(info)
