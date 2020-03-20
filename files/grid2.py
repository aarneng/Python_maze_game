from square import Square


class NewGrid:
    def __init__(self, width=20, height=20):
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
                if not square.get_active():
                    return square
        return False

    def is_square_active(self, x, y):
        return self.grid[y][x].get_active()

    def set_active(self, x, y):
        self.grid[y][x].set_active()

    def get_inactive_neighbours(self, x, y):
        try:
            x, y = y, x
            n = []
            if x > 0:
                i = self.grid[x - 1][y]
                if not i.get_active():
                    n.append(i)

            if y > 0:
                i = self.grid[x][y - 1]
                if not i.get_active():
                    n.append(i)

            if x < self.width - 1:
                i = self.grid[x + 1][y]
                if not i.get_active():
                    n.append(i)

            if y < self.height - 1:
                i = self.grid[x][y + 1]
                if not i.get_active():
                    n.append(i)
            return n
        except IndexError:
            print(x, y, "error")

    def get_active_neighbours(self, x, y):
        try:
            x, y = y, x
            n = []
            if x > 0:
                i = self.grid[x - 1][y]
                if i.get_active():
                    n.append(i)

            if y > 0:
                i = self.grid[x][y - 1]
                if i.get_active():
                    n.append(i)

            if x < self.width - 1:
                i = self.grid[x + 1][y]
                if i.get_active():
                    n.append(i)

            if y < self.height - 1:
                i = self.grid[x][y + 1]
                if i.get_active():
                    n.append(i)

            print(x, y)
            for square in n:
                print(square.get_coords())
            return n
        except IndexError:
            print("beep boop", x, y)
