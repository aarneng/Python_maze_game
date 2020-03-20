from wall import Wall


class Walls:
    def __init__(self, grid):
        self.width = grid.get_width()
        self.height = grid.get_height()
        print(self.width, self.height)
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

        """print(self_x, other_x)
        print(self_y, other_y, "\n")"""

        if self_x - other_x == 0:
            walls = self.horizontal_walls
            if self_y - other_y == 0:
                walls[other_x][other_y + 1].set_inactive()
            else:
                walls[other_x][other_y].set_inactive()
        else:
            walls = self.vertical_walls
            if self_y - other_x == 0:
                walls[other_x + 1][other_y].set_inactive()
            else:
                walls[other_x][other_y].set_inactive()
