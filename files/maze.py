from random import choice


def construct_maze(grid):
    """
    edits grid('s walls) to make a maze
    using randomised prim's algorithm
    """
    max_x = grid.get_width()
    max_y = grid.get_heigth()
    square = grid.get_inactive_square()
    square.set_active()
    coords = square.get_coords()
    c_x = coords[0]
    c_y = coords[1]
    inactive_neighbours = [i for i in grid.get_inactive_neighbours(c_x, c_y)]
    while inactive_neighbours:  # inactive_neighbours not empty
        new_square = choice(inactive_neighbours)
        inactive_neighbours.remove(new_square)
        c_x = new_square.get_coords()[0]
        c_y = new_square.get_coords()[1]
        new_inactives = grid.get_inactive_neighbours(c_x, c_y)

        for neighbor in new_inactives:
            if neighbor not in inactive_neighbours:
                inactive_neighbours.append(neighbor)

        new_square.set_active()
        active_neighbours = grid.get_active_neighbours(c_x, c_y)
        passage_to = choice(active_neighbours)






"""
        if not square:
            return
        n = randint(0, 3)  # 0 = top, 1 = left, 2 = right, 3 = bottom

        if n == 0:
            if coords[0] > 0:  # can move up
                # other_square_coords = [coords[0] - 1, coords[1]]
                other_square_active = grid.is_square_active(coords[0] - 1, coords[1])
                if not other_square_active:
                    grid.set_active(coords[0] - 1, coords[1])
"""