from grid2 import NewGrid
from wall import Wall


class Walls:

    def __init__(self):
        self.width = NewGrid().get_width()
        self.height = NewGrid().get_height()
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
