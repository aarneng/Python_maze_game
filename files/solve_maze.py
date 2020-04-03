from random import choice
# TODO: fix (problem is most likely with some method somewhere that mixes up the grid's/wall's [x][y])


def get_all_routes_from_square(square, grid, walls):
    ret = []
    my_square = grid.get_grid()[square[0]][square[1]]
    square_up = grid.get_grid()[square[0]][square[1] - 1]
    if not walls.is_there_wall_between(my_square, square_up):
        ret.append([square[0], square[1] - 1])
    square_left = grid.get_grid()[square[0] - 1][square[1]]
    if not walls.is_there_wall_between(my_square, square_left):
        ret.append([square[0] - 1, square[1]])
    if square[1] != grid.get_height() - 1:
        square_down = grid.get_grid()[square[0]][square[1] + 1]
        if not walls.is_there_wall_between(my_square, square_down):
            ret.append([square[0], square[1] + 1])
    if square[0] != grid.get_width() - 1:
        square_right = grid.get_grid()[square[0] + 1][square[1]]
        if not walls.is_there_wall_between(my_square, square_right):
            ret.append([square[0] + 1, square[1]])
    return ret


def get_square_obj(square, grid):
    return grid.get_grid()[square[1]][square[0]]


def current(square_coords, grid):
    return grid.get_grid()[square_coords[0]][square_coords[1]]


def solve_maze(grid, walls, current_square, goal_square):
    current_node = None
    all_active_nodes = []
    paths_from_nodes = {}
    current_route_after_node = []
    final_route = [current_square]
    visited_squares = [current_square]

    print("this is a test", current_square, get_square_obj(current_square, grid).get_coords())
    count = 0

    while current_square != goal_square and count < 100:
        count += 1

        print(final_route)

        routes_from_current_square = get_all_routes_from_square(current_square, grid, walls)

        for square in visited_squares:
            if square in routes_from_current_square:
                routes_from_current_square.remove(square)

        # print("test", current_routes)
        if len(routes_from_current_square) > 1:  # if node
            # print("hep")
            current_square = choice(routes_from_current_square)
            current_route_after_node.append(current_square)
            final_route.append(current_square)
            routes_from_current_square.remove(current_square)
            # remove route to not go there when checking routes from this node

            current_node = get_square_obj(current_square, grid)
            all_active_nodes.append(current_node)
            paths_from_nodes[current_node] = routes_from_current_square

        elif len(routes_from_current_square) == 1 and current_node is not None:
            current_square = routes_from_current_square[0]
            final_route.append(current_square)
            current_route_after_node.append(current_square)

        elif len(routes_from_current_square) == 0:  # if dead end
            # print(current_route_after_node)

            #del(current_route_after_node[0])
            for square in current_route_after_node:
                final_route.remove(square)

            while len(paths_from_nodes[current_node]) == 0:
                all_active_nodes.remove(current_node)
                current_node = all_active_nodes[-1]

            current_square = choice(paths_from_nodes[current_node])
            paths_from_nodes[current_node].remove(current_square)

            """if len(paths_from_nodes[current_node]) == 0:
                all_active_nodes.remove(current_node)"""

            current_route_after_node = [current_square]
            final_route.append(current_square)

        visited_squares.append(current_square)

    return final_route