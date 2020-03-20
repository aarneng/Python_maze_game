from random import choice
from test_grid import Walls


def construct_maze(grid):
    """
    edits grid('s walls) to make a maze
    using randomised prim's algorithm
    """
    my_walls = Walls(grid)
    square = grid.get_inactive_square()
    square.set_active()
    coords = square.get_coords()
    c_x = coords[0]
    c_y = coords[1]
    inactive_neighbours = [i for i in grid.get_inactive_neighbours(c_x, c_y)]
    print(c_x, c_y, inactive_neighbours)
    while inactive_neighbours:  # inactive_neighbours not empty
        new_square = choice(inactive_neighbours)
        inactive_neighbours.remove(new_square)
        new_square.set_active()

        c_x = new_square.get_coords()[0]
        c_y = new_square.get_coords()[1]

        active_neighbours = grid.get_active_neighbours(c_x, c_y)
        passage_to = choice(active_neighbours)
        for_debug = passage_to.get_coords()
        """print(c_x, c_y)
        print(passage_to.get_coords()[0], passage_to.get_coords()[1], "\n")
        """
        my_walls.remove_wall_between(new_square, passage_to)

        new_inactives = grid.get_inactive_neighbours(c_x, c_y)
        # new_inactives = grid.get_inactive_neighbours(20, 10)

        for neighbor in new_inactives:
            if neighbor not in inactive_neighbours:
                inactive_neighbours.append(neighbor)

    return grid, my_walls
