from random import choice


# TODO: fix (problem is most likely with some method somewhere that mixes up the grid's/wall's [x][y])

"""
def solve_maze(grid, walls, current_square, goal_square):

    using tremaux's algoritm: https://www.youtube.com/watch?v=6OzpKm4te-E
    :param grid:
    :param walls:
    :param current_square:
    :param goal_square:
    :return:


    nodes_and_paths = {}
    previous_square = None
    current_node = None
    final_route = [current_square]
    route_after_node = []
    dead_nodes = []
    count = 0
    test = 0
    test2 = 0
    test3 = 0
    test4 = 0
    while current_square != goal_square and count < 50:
        count += 1
        routes = walls.get_all_routes_from_square(grid.get_active_neighbours(square.get_coords()[1], square.get_coords()[0]))

        if previous_square is not None:
            routes.remove(previous_square)

        for square in routes:
            if square in dead_nodes:
                routes.remove(square)

        if len(routes) > 1:
            test += 1
            current_node = current_square
            nodes_and_paths[current_node] = routes
            previous_square = current_square
            current_square = choice(routes)
            route_after_node = [current_square]
            final_route.append(current_square)

        elif current_node is None:
            test2 += 1
            print(current_square.get_coords())
            previous_square = current_square
            current_square = routes[0]
            final_route.append(current_square)

        elif current_node is not None:
            if len(routes) > 0:
                test3 += 1
                previous_square = current_square
                current_square = routes[0]
                route_after_node.append(current_square)
                final_route.append(current_square)
            else:
                test4 += 1
                try:
                    final_route.remove(i for i in route_after_node)
                except ValueError:
                    pass
                if len(route_after_node) == 0:
                    final_route.remove(current_node)
                    dead_nodes.append(current_node)
                    del route_after_node[current_node]
                    if len(nodes_and_paths) == 0:
                        current_node = None
                    previous_square = current_square
                    current_square = final_route[-2]
    for i in final_route:
        print(i.get_coords())
    return final_route
"""


def solve_maze(grid, walls, current_square, goal_square):
    grid = grid.get_grid()
    current_square = grid[current_square[0]][current_square[1]]
    routes = walls.get_all_routes_from_square(current_square)
    visited_squares = []
    while current_square.get_coords() != goal_square:
        current_square = choice(routes)
        visited_squares.append(current_square)
        routes = walls.get_all_routes_from_square(current_square)
        for square in routes:
            if square in visited_squares:
                routes.remove(square)
        tp = [i.get_coords() for i in routes]
        print(current_square.get_coords(), tp)
    print()
    for i in visited_squares:
        print(i.get_coords())
    return visited_squares
