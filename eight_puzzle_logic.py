import random
from A_star import AStarSolver
from BFS import BFSSolver

class EightPuzzleLogic:
    def __init__(self):
        self.tiles = [[None for _ in range(3)] for _ in range(3)]
        self.empty_tile = 0
        self.initialize_puzzle()

    def initialize_puzzle(self):
        # Initialize the puzzle with random numbers
        numbers = list(range(0, 9))
        random.shuffle(numbers)
        idx = 0
        for i in range(3):
            for j in range(3):
                self.tiles[i][j] = numbers[idx]
                idx += 1

    def reset(self):
        # Reset the puzzle with a new random state
        self.initialize_puzzle()
        return self.tiles
    
    def empty_states(self):
        self.tiles = [[-1 for _ in range(3)] for _ in range(3)]


    def set_manual_state(self,i, j, manual_value):
        # Set the puzzle tile based on manually entered values
        self.tiles[i][j] = manual_value

    def get_goal_state(self):
        # Return the goal state of the puzzle
        return ((1, 2, 3), (4, 5, 6), (7, 8, 0))

    def run_a_star(self):
        # Run the A* algorithm
        initial_state = tuple(map(tuple, self.tiles))
        goal_state = self.get_goal_state()
        solution, iterations = AStarSolver.solve_puzzle(initial_state, goal_state)
        return solution, iterations

    def run_bfs(self):
        # Run the BFS algorithm
        initial_state = tuple(map(tuple, self.tiles))
        goal_state = self.get_goal_state()
        solution, iterations = BFSSolver.solve_puzzle(initial_state, goal_state)
        return solution, iterations
