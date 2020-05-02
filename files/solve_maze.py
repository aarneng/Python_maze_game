def get_square_obj(square, grid):
    return grid.get_grid()[square[1]][square[0]]


def get_all_routes_from_square(square, grid, walls):
    ret = []
    max_height = grid.get_height() - 1
    max_width = grid.get_width() - 1
    other_square = [square[0], square[1] - 1]  # square above original

    if not walls.is_there_wall_between(square, other_square, using_coords=True):
        ret.append(other_square)

    if not square[1] >= max_height:  # to not clip through / cause an error
        other_square = [square[0], square[1] + 1]  # square below original
        if not walls.is_there_wall_between(square, other_square, using_coords=True):
            ret.append(other_square)

    other_square = [square[0] - 1, square[1]]  # square to the left
    if not walls.is_there_wall_between(square, other_square, using_coords=True):
        ret.append(other_square)

    if not square[0] >= max_width:  # to not clip through / cause an error
        other_square = [square[0] + 1, square[1]]  # square to the right
        if not walls.is_there_wall_between(square, other_square, using_coords=True):
            ret.append(other_square)

    return ret





def solve_maze(grid, walls, current_squar, goal_squar):
    goal_square = [i for i in goal_squar[::-1]]
    current_square = [i for i in current_squar[::-1]]

    def solve(route):
        neighbours = get_all_routes_from_square(route[-1], grid, walls)
        # route[-1] is current_square
        for square in route:
            if square in neighbours:
                neighbours.remove(square)

        if goal_square in neighbours:
            route.append(goal_square)
            return route

        if len(neighbours) == 0:  # if dead end
            return False
        if len(neighbours) == 1:
            route.append(neighbours[0])
            return solve(route)
        else:  # if node
            for i in range(len(neighbours)):
                temp = [i for i in route]
                temp.append(neighbours[i])  # doesn't work if using route.append
                ans = solve(temp)
                if not ans:
                    pass
                else:
                    return ans
    final_route = [current_square]
    final_route = solve(final_route)
    return final_route
