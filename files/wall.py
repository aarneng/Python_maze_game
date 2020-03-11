class Wall:
    def __init__(self, between):
        self.between = between
        self.active = None

    def get_surrounding_squares(self):
        """ eg (10.5, 4)"""
        b = self.between
        if isinstance(b[0], float):
            return [[int(b[0]), b[1]], [[int(b[0]) + 1, b[1]]]]
        return [[b[0], int(b[1])], [[b[0], int(b[1]) + 1]]]

    def set_active(self):
        self.active = True
