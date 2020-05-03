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


def solve_maze(grid, walls, current_squar, goal_squar, show_all=False):
    """
    using recursive search, find the goal
    :param grid: grid object
    :param walls: walls at grid
    :param current_squar: square from which to start search
    :param goal_squar: square upon which we want to end up on
    :param show_all: save all the routes to show the animation of the search algorithm
    :return: the route to take to the goal, all routes that were tested if show_all
    """
    goal_square = [i for i in goal_squar[::-1]]
    current_square = [i for i in current_squar[::-1]]
    all_routes = []

    def solve(route, show_animation=False):
        neighbours = get_all_routes_from_square(route[-1], grid, walls)
        # route[-1] is current_square
        if show_animation:
            all_routes.append(route)
            # Professor: Noooo you can't just save all the paths and call that an animation
            # Think of the of the memory!!
            # me: haha saving all paths to show an animation goes brrr
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
            return solve(route, show_animation=show_animation)
        else:  # if node
            for i in range(len(neighbours)):
                temp = [i for i in route]
                temp.append(neighbours[i])  # doesn't work if using route.append
                ans = solve(temp, show_animation=show_animation)
                if not ans:
                    pass
                else:
                    return ans
    final_route = [current_square]
    final_route = solve(final_route, show_animation=show_all)
    return final_route, all_routes
