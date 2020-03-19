from square import Square


class NewGrid:
    def __init__(self, width=20, height=15):
        """ creates a list of size w * h"""
        self.height = height
        self.width = width
        self.grid = [[Square([i, j]) for i in range(width)] for j in range(height)]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_inactive_square(self):
        for sublist in self.grid:
            for square in sublist:
                if not square.get_active:
                    return square
        return False

    def is_square_active(self, x, y):
        return self.grid[y][x].get_active()

    def set_active(self, x, y):
        self.grid[y][x].set_active()

    def get_inactive_neighbours(self, x, y):
        n = []
        if x > 0:
            i = self.grid[x - 1][y]
            if not i:
                n.append(i)
        if y > 0:
            i = self.grid[x][y - 1]
            if not i:
                n.append(i)
        if x < self.width:
            i = self.grid[x + 1][y]
            if not i:
                n.append(i)
        if y < self.height:
            i = self.grid[x][y + 1]
            if not i:
                n.append(i)
        return n

    def get_active_neighbours(self, x, y):
        n = []
        if x > 0:
            i = self.grid[x - 1][y]
            if i:
                n.append(i)
        if y > 0:
            i = self.grid[x][y - 1]
            if i:
                n.append(i)
        if x < self.width:
            i = self.grid[x + 1][y]
            if i:
                n.append(i)
        if y < self.height:
            i = self.grid[x][y + 1]
            if i:
                n.append(i)
        return n
