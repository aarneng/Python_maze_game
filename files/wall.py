from random import randint


class Wall:
    def __init__(self, coords, orientation):
        self.coords = coords
        self.orientation = orientation  # 0 = vertical, 1 = horizontal
        self.active = True if not (randint(0, 30) == 0) else randint(2, 3)

    def get_activity(self):
        return self.active

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False
