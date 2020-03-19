from grid import Walls


class Square:
    def __init__(self, coords):  # , walls):
        self.coords = coords
        # self.wall_status = walls
        self.active = False

    def get_coords(self):
        return self.coords

    #    def get_status(self):
    #        return self.wall_status

    def get_active(self):
        return self.active

    def set_active(self):
        self.active = True

    def remove_wall_between(self, other_square):

        other_x = other_square.get_coords()[0]
        other_y = other_square.get_coords()[1]

        if self.coords[0] - other_x == 0:
            walls = Walls().get_horizontal()
            if self.coords[1] - other_y == 1:
                walls[other_x][other_y + 1].set_inactive()
            else:
                walls[other_x][other_y].set_inactive()
        else:
            walls = Walls().get_vertical()
            if self.coords[0] - other_x == 1:
                walls[other_x + 1][other_y].set_inactive()
            else:
                walls[other_x][other_y].set_inactive()
