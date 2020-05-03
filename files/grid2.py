from square import Square


class NewGrid:
    def __init__(self, width=10, height=10):
        """ creates a list of size w * h"""
        self.height = height
        self.width = width
        self.grid = [[Square([i, j]) for i in range(width)] for j in range(height)]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_grid(self):
        return self.grid

    def get_inactive_square(self):
        for sublist in self.grid:
            for square in sublist:
                if not square.get_active():
                    return square
        return False

    def is_square_active(self, x, y):
        return self.grid[y][x].get_active()

    def get_square(self, coords):
        return self.grid[coords[1]][coords[0]]

    def set_active(self, x, y):
        self.grid[y][x].set_active()

    def get_inactive_neighbours(self, x, y):
        x, y = y, x
        n = []
        if x > 0:  # avoid IndexErrors
            i = self.grid[x - 1][y]
            if not i.get_active():
                n.append(i)

        if y > 0:
            i = self.grid[x][y - 1]
            if not i.get_active():
                n.append(i)

        if x < self.height - 1:
            i = self.grid[x + 1][y]
            if not i.get_active():
                n.append(i)

        if y < self.width - 1:
            i = self.grid[x][y + 1]
            if not i.get_active():
                n.append(i)
        return n

    def get_active_neighbours(self, x, y):
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

        if x < self.height - 1:
            i = self.grid[x + 1][y]
            if i.get_active():
                n.append(i)

        if y < self.width - 1:
            i = self.grid[x][y + 1]
            if i.get_active():
                n.append(i)
        return n

    def make_goal(self, x, y):
        try:
            self.grid[x][y].set_goal()
        except IndexError:
            self.grid[y][x].set_goal()
        # If it works, it's ain't stupid… right?

    def add_player_to_square(self, x, y):
        self.grid[x][y].set_player()

    def remove_player_from_square(self, x, y):
        self.grid[x][y].unset_player()
