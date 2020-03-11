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
