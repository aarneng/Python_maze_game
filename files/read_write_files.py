from grid2 import NewGrid
from test_grid import Walls


def write_file(grid, walls, filename, points):
    if filename == ".txt":
        filename = "mymaze.txt"  # you never know

    with open(filename, "w") as f:
        width = grid.get_width()
        height = grid.get_height()
        f.write(str(width) + " " + str(height) + " " + str(points) + "\n")

        vertical = walls.get_vertical()
        horizontal = walls.get_horizontal()
        grd = grid.get_grid()
        goal_found = False

        for i in range(width):
            # the + 1 in height and width are because the vert. 2d array of walls
            # is of size (w + 1 * h) and hor. arr is (w * h + 1)
            for j in range(height):
                if vertical[j][i].get_activity() == 2:  # ground wall
                    f.write("-")
                elif vertical[j][i].get_activity() == 3:  # ceiling wall
                    f.write("=")
                elif vertical[j][i].get_activity():
                    f.write("_")
                else:
                    f.write(" ")
            f.write("\n")

            for j in range(height + 1):

                if horizontal[j][i].get_activity() == 2:  # ground wall
                    f.write("\\")
                elif horizontal[j][i].get_activity() == 3:  # ceiling wall
                    f.write(";")
                elif horizontal[j][i].get_activity():
                    f.write("/")
                else:
                    f.write(" ")
                if grd[min(height - 1, j)][min(width - 1, i)].get_goal_status() and not goal_found:
                    # to avoid IndexError
                    # grid size is only of size w * h
                    j -= 1
                    f.write("0")
                    goal_found = True
                if grd[min(height - 1, j)][min(width - 1, i)].get_player_status():
                    j -= 1
                    f.write(".")
            f.write("\n")
    return True


def read_file(filename):
    with open(filename) as f:
        dimensions = f.readline()
        while dimensions == "\n":
            dimensions = f.readline()
        dimensions = dimensions.split("\n")[0].split(" ")
        width, height = int(dimensions[0]), int(dimensions[1])
        points = int(dimensions[2])

        ret_grid = NewGrid(width=width, height=height)
        ret_walls = Walls(ret_grid)
        vertical_walls = ret_walls.get_vertical()
        horizontal_walls = ret_walls.get_horizontal()
        for walls in vertical_walls:
            for wall in walls:
                wall.set_active()
        for walls in horizontal_walls:
            for wall in walls:
                wall.set_active()
        # reset walls so that there are no walls that are only on ground / ceiling

        squares = ret_grid.get_grid()
        message = f"File {filename} read succesfully!"
        x, y = 0, 0
        checking_vertical = False
        allowed_chars = ["_", "-", "=", "/", "\\", ";", "0", ".", " "]

        for line in f:
            for char in line.split("\n")[0]:
                if char == "_":
                    pass
                elif char == "-":
                    vertical_walls[x][int(y)].set_active(active=2)
                elif char == "=":
                    vertical_walls[x][int(y)].set_active(active=3)
                elif char == "/":
                    pass
                elif char == "\\":
                    horizontal_walls[x][int(y)].set_active(active=2)
                elif char == ";":
                    horizontal_walls[x][int(y)].set_active(active=3)
                elif char == ".":
                    x -= 1
                    ret_grid.add_player_to_square(x, int(y))
                elif char == "0":
                    x -= 1
                    ret_grid.make_goal(x, int(y))
                else:
                    if char not in allowed_chars:
                        message = f"File {filename} is likely corrupt and/or broken."
                    if checking_vertical and x > 0:
                        ret_walls.remove_wall_between(squares[x][int(y)], squares[x - 1][int(y)])
                    elif not checking_vertical and y > 0:
                        ret_walls.remove_wall_between(squares[x][int(y)], squares[x][int(y) - 1])
                x += 1
            x = 0
            checking_vertical = not checking_vertical
            y += 1 / 2
        return ret_grid, ret_walls, message, points
