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


NG = NewGrid()
NG.set_active(0, 0)
grid, walls, maze_done, inactive_neighbours = construct_maze(NG, Walls(NG), NG.get_inactive_neighbours(0, 0), False, [0, 0])

write_file(grid, walls)
