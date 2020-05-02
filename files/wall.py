from random import randint


class Wall:
    def __init__(self, coords, orientation, ratio):
        self.coords = coords
        self.orientation = orientation  # 0 = vertical, 1 = horizontal
        self.active = True if not (randint(0, ratio) == 0) else randint(2, 3)
        # a wall defaults to a value of either True, 2 or 3.
        # the boolean True means the wall is active- a value of 2 or 3 means
        # the wall is only on the ground or ceiling. The odds of this happening to a wall are 1/(ratio + 1)
        # Some walls will be set to an inactive status when creating the maze

    def get_activity(self):
        return self.active

    def set_active(self, active=True):
        self.active = active

    def set_inactive(self):
        self.active = False
