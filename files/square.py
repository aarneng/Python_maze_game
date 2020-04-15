class Square:
    def __init__(self, coords):  # , walls):
        self.coords = coords
        # self.wall_status = walls
        self.active = False
        self.is_goal = False
        self.contains_player = False

    def get_coords(self):
        return self.coords

    #    def get_status(self):
    #        return self.wall_status

    def get_active(self):
        return self.active

    def set_active(self):
        self.active = True

    def set_goal(self):
        self.is_goal = True

    def get_goal_status(self):
        return self.is_goal

    def set_player(self):
        self.contains_player = True

    def unset_player(self):
        self.contains_player = False

    def get_player_status(self):
        return self.contains_player
