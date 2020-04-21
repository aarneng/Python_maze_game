from random import choice, randint


def construct_maze(grid, my_walls, inactive_neighbours, show_animation, player_square):
    """
    edits grid('s walls) to make a maze
    using randomised prim's algorithm.
    Initially, all the squares in the grid have walls between them.
    The algorithm initially chooses the inactive square (0,0), and makes that square active.
    it then checks all the inactive squares next to that square, and adds them to a list.
    it then chooses a random square from that list, makes it active, and removes the wall between those two squares.
    it then checks all the inactive squares around the new square, and adds them to the inactive squares list,
    as long as the square isn't already in the list.
    the process goes on as long as there are inactive squares.
    """

    while inactive_neighbours:  # inactive_neighbours not empty
        new_square = choice(inactive_neighbours)
        inactive_neighbours.remove(new_square)
        new_square.set_active()

        c_x = new_square.get_coords()[0]
        c_y = new_square.get_coords()[1]

        active_neighbours = grid.get_active_neighbours(c_x, c_y)

        passage_to = choice(active_neighbours)
        my_walls.remove_wall_between(new_square, passage_to)

        new_inactives = grid.get_inactive_neighbours(c_x, c_y)

        for neighbor in new_inactives:
            if neighbor not in inactive_neighbours:
                inactive_neighbours.append(neighbor)
        if show_animation:
            maze_ready = not inactive_neighbours
            difficulty = 2
            goal_x = randint(int(grid.get_width() / difficulty), grid.get_width() - 1)
            goal_y = randint(int(grid.get_height() / difficulty), grid.get_height() - 1)
            grid.make_goal(goal_x, goal_y)
            grid.add_player_to_square(player_square[0], player_square[1])
            return grid, my_walls, maze_ready, inactive_neighbours, new_square.get_coords()

    maze_ready = not inactive_neighbours
    difficulty = 2
    goal_x = randint(int(grid.get_width() / difficulty), grid.get_width() - 1)
    goal_y = randint(int(grid.get_height() / difficulty), grid.get_height() - 1)
    grid.make_goal(goal_x, goal_y)
    grid.add_player_to_square(player_square[0], player_square[1])

    return grid, my_walls, maze_ready, inactive_neighbours, [-100, -100]
