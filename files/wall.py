from random import randint


class Wall:
    def __init__(self, coords, orientation):
        self.coords = coords
        self.orientation = orientation  # 0 = vertical, 1 = horizontal
        self.active = True if not (randint(0, 10) == 0) else randint(2, 3)
        # solid wall with a 1 / n prob of it being either on groud / ceiling

    def get_activity(self):
        return self.active

    def set_active(self, active=True):
        self.active = active

    def set_inactive(self):
        self.active = False
