from grid2 import NewGrid
from test_grid import Walls
from maze import construct_maze
from square import Square


def write_file(grid, walls, filename="mymaze.txt"):
    with open(filename, "w") as f:
        width = grid.get_width()
        height = grid.get_height()
        f.write(str(width) + " " + str(height) + "\n")

        vertical = walls.get_vertical()
        horizontal = walls.get_horizontal()
        grd = grid.get_grid()

        for i in range(height):
            for j in range(width):
                if horizontal[i][j].get_activity() == 2:  # ground wall
                    f.write("-")
                elif horizontal[i][j].get_activity() == 3:  # ceiling wall
                    f.write("=")
                elif horizontal[i][j].get_activity():
                    f.write("_")
                else:
                    f.write(" ")
            f.write("\n")

            for j in range(width):
                if vertical[i][j].get_activity() == 2:  # ground wall
                    f.write("\\")
                elif vertical[i][j].get_activity() == 3:  # ceiling wall
                    f.write(";")
                elif vertical[i][j].get_activity():
                    f.write("/")
                else:
                    f.write(" ")

                if grd[i][j].get_goal_status():
                    f.write("0")
                if grd[i][j].get_player_status():
                    f.write(".")
            f.write("\n")


def read_file(filename):
    with open(filename) as f:
        dim = f.readline().split("\n")[0].split(" ")
        width, height = int(dim[0]), int(dim[1])

        ret_grid = NewGrid(width=width, height=height)
        ret_walls = Walls(ret_grid)
        vertical_walls = ret_walls.get_horizontal()
        horizontal_walls = ret_walls.get_vertical()

        for walls in vertical_walls:
            for wall in walls:
                wall.set_active()
        for walls in horizontal_walls:
            for wall in walls:
                wall.set_active()
        # remove walls that are only on ground / ceiling

        squares = ret_grid.get_grid()
        error_message = ""
        x, y = 0, 0
        checking_vertical = False
        allowed_chars = ["_", "-", "=", "/", "\\", ";", "0", "."]
        count = 0
        for line in f:
            x = 0
            count += 1
            for char in line.split("\n")[0]:
                if char == "_":
                    pass
                elif char == "-":
                    horizontal_walls[int(y)][x].set_active(active=2)
                elif char == "=":
                    horizontal_walls[int(y)][x].set_active(active=3)
                elif char == "/":
                    pass
                elif char == "\\":
                    vertical_walls[int(y)][x].set_active(active=2)
                elif char == ";":
                    vertical_walls[int(y)][x].set_active(active=3)
                elif char == ".":
                    x -= 1
                    ret_grid.add_player_to_square(x, int(y))
                elif char == "0":
                    x -= 1
                    ret_grid.make_goal(x, int(y))
                else:
                    if char not in allowed_chars:
                        error_message = "File is likely corrupt.\nCompleting the maze might not be possible."
                    if checking_vertical and x > 0:
                        ret_walls.remove_wall_between(squares[x][int(y)], squares[x - 1][int(y)])
                    elif y >= 1:
                        ret_walls.remove_wall_between(squares[x][int(y)], squares[x][int(y) - 1])
                x += 1
            checking_vertical = not checking_vertical
            y += 1 / 2

        return ret_grid, ret_walls, error_message


#NG = NewGrid()
#NG.set_active(0, 0)
#grid, walls, maze_done, inactive_neighbours = construct_maze(NG, Walls(NG), NG.get_inactive_neighbours(0, 0), False, [0, 0])

#write_file(grid, walls)

read_file("mymaze.txt")
