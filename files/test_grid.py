from wall import Wall


class Walls:
    def __init__(self, grid):
        self.width = grid.get_width()
        self.height = grid.get_height()
        self.grid = grid
        self.vertical_walls = [[Wall(0, [i, j]) for i in range(self.width + 1)] for j in range(self.height)]
        self.horizontal_walls = [[Wall(1, [i, j]) for i in range(self.width)] for j in range(self.height + 1)]

    def get_wall(self):
        for walls in self.vertical_walls:
            for wall in walls:
                if wall.get_activity() is None:
                    return wall
        # if no vertical wall try horizontal wall
        for walls in self.horizontal_walls:
            for wall in walls:
                if wall.get_activity() is None:
                    return wall
        # else
        return False

    def get_horizontal(self):
        return self.horizontal_walls

    def get_vertical(self):
        return self.vertical_walls

    def remove_wall_between(self, square, other_square):
        self_x = square.get_coords()[0]
        self_y = square.get_coords()[1]
        other_x = other_square.get_coords()[0]
        other_y = other_square.get_coords()[1]

        if self_x - other_x == 0:
            walls = self.horizontal_walls
            if self_y - other_y == 1:
                walls[self_y][self_x].set_inactive()
            else:
                walls[self_y + 1][self_x].set_inactive()
        else:
            walls = self.vertical_walls
            if self_x - other_x == 1:
                walls[self_y][self_x].set_inactive()
            else:
                walls[self_y][self_x + 1].set_inactive()

    def is_there_wall_between(self, square, other_square, using_coords=False):
        """

        :param square:
        :param other_square:
        :return: True if there is wall,
        2 if there is a wall but only on the bottom (so player can jump over it)
        3 if there is a wall but only on top, so player can walk under it
        """
        if not using_coords:
            self_x = square.get_coords()[0]
            self_y = square.get_coords()[1]
            other_x = other_square.get_coords()[0]
            other_y = other_square.get_coords()[1]
        else:
            self_x = square[1]
            self_y = square[0]
            other_x = other_square[1]
            other_y = other_square[0]
        if self_x == 0 and other_x > 1:  # so player can't clip through other wall
            return True
        if self_y == 0 and other_y > 1:
            return True

        if self_x - other_x == 0:
            walls = self.horizontal_walls
            if self_y - other_y == 1:
                return walls[self_y][self_x].get_activity()
            else:
                return walls[self_y + 1][self_x].get_activity()
        else:
            walls = self.vertical_walls
            if self_x - other_x == 1:
                return walls[self_y][self_x].get_activity()
            else:
                return walls[self_y][self_x + 1].get_activity()
"""
    def get_all_routes_from_square(self, square):
        neighbours = self.grid.get_active_neighbours(square.get_coords()[1], square.get_coords()[0])
        ret = []
        for neighbour in neighbours:
            if not self.is_there_wall_between(square, neighbour):
                ret.append(neighbour)
        return ret
"""