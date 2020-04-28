def get_square_obj(square, grid):
    return grid.get_grid()[square[1]][square[0]]


def get_all_routes_from_square(square, grid, walls):
    ret = []
    max_height = grid.get_height() - 1
    max_width = grid.get_width() - 1
    other_square = [square[0], square[1] - 1]

    if not walls.is_there_wall_between(square, other_square, using_coords=True):
        ret.append(other_square)

    if square[1] != max_height:  # to not clip through / cause an error
        other_square = [square[0], square[1] + 1]  # square below original
        if not walls.is_there_wall_between(square, other_square, using_coords=True):
            ret.append(other_square)

    other_square = [square[0] - 1, square[1]]  # square to the left
    if not walls.is_there_wall_between(square, other_square, using_coords=True):
        ret.append(other_square)

    if square[0] != max_width:  # to not clip through / cause an error
        other_square = [square[0] + 1, square[1]]  # square to the right
        if not walls.is_there_wall_between(square, other_square, using_coords=True):
            ret.append(other_square)

    return ret


append_to_all_routes = True


def solve_maze(grid, walls, current_square, goal_square):
    global append_to_all_routes
    append_to_all_routes = True
    all_routes = []

    def solve(route):
        global append_to_all_routes
        neighbours = get_all_routes_from_square(route[-1], grid, walls)
        # route[-1] is current_square
        for square in route:
            if square in neighbours:
                neighbours.remove(square)

        if goal_square in neighbours:
            route.append(goal_square)
            append_to_all_routes = False
            return route

        all_routes.append(route)

        if len(neighbours) == 0:  # if dead end
            return False
        if len(neighbours) == 1:
            temp = [i for i in route]
            temp.append(neighbours[0])
            return solve(temp)
        else:  # if node
            for i in range(len(neighbours)):
                temp = [i for i in route]
                temp.append(neighbours[i])
                if not solve(temp):
                    pass
                else:
                    temp = [i for i in route]
                    temp.append(neighbours[i])
                    return solve(temp)
    final_route = [current_square]
    final_route = solve(final_route)
    return final_route, all_routes
