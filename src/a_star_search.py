"""
Author: Oscar Nolen
Course: ITCS 6150

This program implements A* search for the 8 puzzle problem
"""

import heapq
import copy

directions = {
    'up': (-1, 0),
    'left': (0, -1),
    'right': (0, 1),
    'down': (1, 0)
}

"""
- This function runs a star search with a priority queue
- Priority is assigned by f(grid) = step_cost(grid) + heuristic(grid, goal)
- Solution path is stored via child-parent relationships in dictionary
- Step costs are stored per 8 puzzle state in a dictionary
- If path is found, solution path, nodes generated, and nodes expanded are returned
- If no path is found, only nodes generated and nodes expanded are returned
"""
def a_star(start, goal, heuristic):
    visited = set()
    pq = []
    path_tracker = {}  # stores child-parent relationships
    step_count = {}  # stores step count
    nodes_generated = 1
    nodes_expanded = 0

    visited.add(gridToStrSeq(start))
    step_count[gridToStrSeq(start)] = 0
    heapq.heappush(pq, (0, start))

    while pq:
        grid = heapq.heappop(pq)[1]
        nodes_expanded += 1

        if grid == goal:  # goal check
            return solution_path(grid, start, path_tracker), nodes_generated, nodes_expanded

        for new_grid in get_moves(grid):
            if gridToStrSeq(new_grid) not in visited:
                step_count[gridToStrSeq(new_grid)] = step_count[gridToStrSeq(grid)] + 1  # increments step count
                f_val = step_count[gridToStrSeq(new_grid)] + heuristic(new_grid, goal)

                visited.add(gridToStrSeq(new_grid))
                heapq.heappush(pq, (f_val, new_grid))
                path_tracker[gridToStrSeq(new_grid)] = gridToStrSeq(grid)  # stores child-parent
                nodes_generated += 1

    return nodes_generated, nodes_expanded


"""
- This function returns the solution path when the goal state is found.
- We backtrack through the dictionary, starting from the goal state until we see the start state.
- We then returned a reversed version of the sequence to maintain the correct path order
"""
def solution_path(grid, start, tracker):
    path = []
    gridStrSeq = gridToStrSeq(grid)
    startStrSeq = gridToStrSeq(start)

    if grid == start:  # if start and goal grid are same
        return []

    path.append(grid)

    while gridStrSeq != startStrSeq:  # iterate backwards until start grid
        parent_strSeq = tracker[gridStrSeq]
        path.append(strSeqToGrid(parent_strSeq))
        gridStrSeq = parent_strSeq

    path.reverse()
    return path


"""
- This function finds the 0 tile given an 8 puzzle state
"""
def find_zero(grid):
    size = len(grid)

    for row in range(size):
        for col in range(size):
            if grid[row][col] == 0:
                return row, col


"""
- This function calculates the manhattan heuristic for an 8 puzzle state, given the goal state
"""
def man_heuristic(grid, goal):
    size = len(grid)
    man_dist = 0

    for row in range(size):
        for col in range(size):
            val = grid[row][col]

            if val != 0:
                for goal_row in range(size):
                    if val in goal[goal_row]:
                        goal_col = goal[goal_row].index(val)
                        man_dist += abs(row - goal_row) + abs(col - goal_col)
                        break

    return man_dist

"""
- This function calculates the number of misplaced tiles for an 8 puzzle state, given the goal state
"""
def tile_heuristic(grid, goal):
    size = len(grid)
    wrong_tiles = 0

    for row in range(size):
        for col in range(size):
            if grid[row][col] != 0 and grid[row][col] != goal[row][col]:
                wrong_tiles += 1

    return wrong_tiles


"""
- This function returns all possible move states, given a current 8 puzzle state
"""
def get_moves(grid):
    row, col = find_zero(grid)
    new_grids = []

    for dr, dc in directions.values():
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:  # check if indices are in-bounds
            new_grid = copy.deepcopy(grid)
            new_grid[row][col], new_grid[new_row][new_col] = new_grid[new_row][new_col], new_grid[row][col]

            new_grids.append(new_grid)

    return new_grids


"""
- This function converts a int sequence to a 2D grid
- For example, [1,2,3,4,5,6,7,8,0] -> [[1,2,3][4,5,6][7,8,0]]
- This is used as a step in handling user input
"""
def seqToGrid(seq):
    grid = [seq[i:i+3] for i in range(0, len(seq), 3)]
    return grid


"""
- This function converts a 2D grid to a string sequence.
- For example, [[1,2,3][4,5,6][7,8,0]] -> '123456780'
- This is used to store the solution path in a dictionary, since arrays are not hashable
"""
def gridToStrSeq(grid):
    size = len(grid)
    seq = []

    for row in range(size):
        for col in range(size):
            seq.append(str(grid[row][col]))

    return ''.join(seq)


"""
- This function converts a string sequence to a 2D grid.
- For example, '123456780' -> [[1,2,3][4,5,6][7,8,0]]
- This is used to in returning solution path from dictionary
"""
def strSeqToGrid(strSeq):
    seq = [int(ch) for ch in strSeq]
    return seqToGrid(seq)


"""
- This function validates grid input for the start and goal grids.
- Checks that input is a sequence corresponding to a valid 8 puzzle state
"""
def isInputValid(strSeq):
    if len(strSeq) != 9:
        return False

    for num in range(9):
        if strSeq.count(str(num)) != 1:
            return False

    return True


"""
- Main function takes input for start and goal grids and runs a star search.
- Grid input is taken as a sequence of numbers (e.g. '123456780') and reformatted as 2D array
- Grid input is additionally validated
"""
def main():
    input1 = input('enter start grid: ')
    if not isInputValid(input1):
        raise Exception('Invalid input: ' + input1)
    input2 = input('enter goal grid: ')
    if not isInputValid(input2):
        raise Exception('Invalid input: ' + input2)
    print('\n')

    startGrid = seqToGrid([int(ch) for ch in input1])
    goalGrid = seqToGrid([int(ch) for ch in input2])

    man_search = a_star(startGrid, goalGrid, man_heuristic)
    if len(man_search) == 2:
        print('NO PATH FOUND WITH MANHATTAN HEURISTIC')
        print('NODES GENERATED: ' + str(man_search[0]))
        print('NODES EXPANDED: ' + str(man_search[1]) + '\n')
    else:
        print('FOUND THE GOAL WITH MANHATTAN HEURISTIC')
        print('NODES GENERATED: ' + str(man_search[1]))
        print('NODES EXPANDED: ' + str(man_search[2]))
        print('SOLUTION PATH:\n')
        for grid in man_search[0]:
            for row in grid:
                print(row)
            print('\n')

    tile_search = a_star(startGrid, goalGrid, tile_heuristic)
    if len(tile_search) == 2:
        print('NO PATH FOUND WITH TILE HEURISTIC')
        print('NODES GENERATED: ' + str(tile_search[0]))
        print('NODES EXPANDED: ' + str(tile_search[1]) + '\n')
    else:
        print('FOUND THE GOAL WITH TILE HEURISTIC')
        print('NODES GENERATED: ' + str(tile_search[1]))
        print('NODES EXPANDED: ' + str(tile_search[2]))
        print('SOLUTION PATH:\n')
        for grid in tile_search[0]:
            for row in grid:
                print(row)
            print('\n')


if __name__ == "__main__":
    main()
