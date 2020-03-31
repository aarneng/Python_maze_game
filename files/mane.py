from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
from test_grid import Walls
from grid2 import NewGrid
import maze
from solve_maze import solve_maze


def scale_by(x):
    return 2 - 1 / (1 + x / 150)


class Mane(QMainWindow):
    def __init__(self):
        super().__init__()
        self.test = False
        self.grid = NewGrid(width=10, height=10)
        self._grid_inactive_neighbours = self.grid.get_inactive_neighbours(0, 0)
        self.grid.set_active(0, 0)
        self.show_animation = False  # Animation will take a long time for big grids, around (30x30 & +) depending on computer
        self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours = maze.construct_maze(self.grid, Walls(self.grid), self._grid_inactive_neighbours, self.show_animation)
        self.maze_solved = not self.show_animation
        self.my_maze_solution = []
        self.x_offset = 100
        self.y_offset = 100
        self.x_squares = self.grid.get_width()
        self.y_squares = self.grid.get_height()
        self.width = 500 * scale_by(self.x_squares)
        self.height = 500 * scale_by(self.y_squares)
        self.square_size = max(self.width / self.x_squares, self.height / self.y_squares)
        self.toDraw = None

        self.player_is_on_square = [0, 0]
        self.goal_is_on_square = self.get_goal_square()
        self.player_is_on_ground = True

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle("Labyrinth Y2")
        self.setGeometry(self.x_offset, self.y_offset, self.width + 100, self.height + 100)
        self.show()

    def paintEvent(self, event):
        """
        coords: tuple, eg. (5, 2) -> squares, not px
        args: -> dictionary, eg. {
            up: True (wall)
            left: True (wall)
            Right: False (no wall)
            down: True (wall)
        }
        :return: None
        """
        """x_s = self.x_squares
        y_s = self.y_squares
        square_size = min(self.width / x_s, self.height / y_s)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        coords = self.toDraw[0]
        args = self.toDraw[1]"""
        if self.player_is_on_square == self.goal_is_on_square:
            pass
        painter = QPainter(self)
        painter.setPen(Qt.black)
        s = self.square_size
        horizontal_walls = self.walls.get_horizontal()
        vertical_walls = self.walls.get_vertical()
        for i in range(len(horizontal_walls)):
            for j in range(len(horizontal_walls[i])):
                if horizontal_walls[i][j].get_activity():
                    if horizontal_walls[i][j].get_activity() == 3:
                        painter.setPen(Qt.green)
                        painter.drawLine(i * s + 10, j * s + 10, i * s + 10, (j + 1) * s + 10)
                        painter.setPen(Qt.black)
                    elif horizontal_walls[i][j].get_activity() == 2:
                        painter.setPen(Qt.blue)
                        painter.drawLine(i * s + 10, j * s + 10, i * s + 10, (j + 1) * s + 10)
                        painter.setPen(Qt.black)
                    else:
                        painter.drawLine(i * s + 10, j * s + 10, i * s + 10, (j + 1) * s + 10)
        for i in range(len(vertical_walls)):
            for j in range(len(vertical_walls[i])):
                if vertical_walls[i][j].get_activity():
                    if vertical_walls[i][j].get_activity() == 3:
                        painter.setPen(Qt.green)
                        painter.drawLine(i * s + 10, j * s + 10, (i + 1) * s + 10, j * s + 10)
                        painter.setPen(Qt.black)
                    elif vertical_walls[i][j].get_activity() == 2:
                        painter.setPen(Qt.blue)
                        painter.drawLine(i * s + 10, j * s + 10, (i + 1) * s + 10, j * s + 10)
                        painter.setPen(Qt.black)
                    else:
                        painter.drawLine(i * s + 10, j * s + 10, (i + 1) * s + 10, j * s + 10)

        if self.test:
            x = int(self.x_squares/2) + 1
            y = int(self.y_squares / 2)
            painter.drawRect(x * s, y * s, s, s)
            square = self.grid.get_square([x, y])
            for i in self.walls.get_all_routes_from_square(square):
                painter.drawRect(i.get_coords()[0] * s, i.get_coords()[1] * s, s, s)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))

        self.goal_is_on_square = self.get_goal_square()

        goal_x = self.goal_is_on_square[0]
        goal_y = self.goal_is_on_square[1]
        painter.drawRect(goal_x * s + 12, goal_y * s + 12, s / 1.2, s / 1.2)

        """self.player_is_on_square = self.get_player_square()"""
        player_x = self.player_is_on_square[0]
        player_y = self.player_is_on_square[1]

        if self.player_is_on_ground:
            painter.setPen(Qt.yellow)
            painter.setBrush(Qt.yellow)
            painter.drawEllipse(player_x * s + 12, player_y * s + 12, s / 1.2, s / 1.2)  # for fitting
            painter.setPen(Qt.black)
            painter.setBrush(Qt.black)
            painter.drawEllipse(player_x * s + (s / 1.8), player_y * s + (s / 2.5), s / 6, s / 6)
            painter.drawEllipse(player_x * s + (s / 1.3), player_y * s + (s / 2.5), s / 6, s / 6)
            painter.drawArc(player_x * s + (s / 1.7), player_y * s + (s / 1.8), s / 4, s / 6, 180 * 16, 180 * 16)
        else:
            painter.setPen(Qt.yellow)
            painter.setBrush(Qt.yellow)
            painter.drawEllipse(player_x * s + 12, player_y * s + 12, s, s)
            painter.setPen(Qt.black)
            painter.setBrush(Qt.black)
            painter.drawEllipse(player_x * s + (s / 1.8), player_y * s + (s / 2.5), s / 6, s / 6)
            painter.drawEllipse(player_x * s + (s / 1.3), player_y * s + (s / 2.5), s / 6, s / 6)
            painter.drawEllipse(player_x * s + (s / 1.7), player_y * s + (s / 1.8), s / 4, s / 6)
        if self.show_animation and not self.maze_done:
            self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours = maze.construct_maze(self.grid, self.walls, self._grid_inactive_neighbours, self.show_animation)
            self.update()

        if self.maze_solved:
            painter.setPen(Qt.red)
            try:
                prev = self.my_maze_solution[0]
            except IndexError:
                prev = [0, 0]
            for square in self.my_maze_solution:
                painter.drawLine(prev[0] * s + 10 + s/2, prev[1] * s + 10 + s/2, square[0] * s + 10 + s/2,
                                 square[1] * s + 10 + s/2)
                prev = square
            painter.setPen(Qt.black)

    def get_goal_square(self):
        g = self.grid.get_grid()
        for i in range(len(g)):
            for j in range(len(g[i])):
                if g[i][j].get_goal_status():
                    return [i, j]
        return [0, 0]  # else

    def move_up(self):
        square = self.grid.get_grid()[self.player_is_on_square[0]][self.player_is_on_square[1]]
        other_square = self.grid.get_grid()[self.player_is_on_square[0]][self.player_is_on_square[1] - 1]
        ans = self.walls.is_there_wall_between(square, other_square)
        if not ans:
            self.player_is_on_square = [self.player_is_on_square[0], self.player_is_on_square[1] - 1]
            self.update()
        elif ans == 3:
            if self.player_is_on_ground:
                self.player_is_on_square = [self.player_is_on_square[0], self.player_is_on_square[1] - 1]
                self.update()
        elif ans == 2:
            if not self.player_is_on_ground:
                self.player_is_on_square = [self.player_is_on_square[0], self.player_is_on_square[1] - 1]
                self.update()

    def move_left(self):
        square = self.grid.get_grid()[self.player_is_on_square[0]][self.player_is_on_square[1]]
        other_square = self.grid.get_grid()[self.player_is_on_square[0] - 1][self.player_is_on_square[1]]
        ans = self.walls.is_there_wall_between(square, other_square)
        if not ans:
            self.player_is_on_square = [self.player_is_on_square[0] - 1, self.player_is_on_square[1]]
            self.update()
        elif ans == 3:
            if self.player_is_on_ground:
                self.player_is_on_square = [self.player_is_on_square[0] - 1, self.player_is_on_square[1]]
                self.update()
        elif ans == 2:
            if not self.player_is_on_ground:
                self.player_is_on_square = [self.player_is_on_square[0] - 1, self.player_is_on_square[1]]
                self.update()

    def move_down(self):
        if self.player_is_on_square[1] > self.grid.get_height() - 2:
            return
        square = self.grid.get_grid()[self.player_is_on_square[0]][self.player_is_on_square[1]]
        other_square = self.grid.get_grid()[self.player_is_on_square[0]][self.player_is_on_square[1] + 1]
        ans = self.walls.is_there_wall_between(square, other_square)
        if not ans:
            self.player_is_on_square = [self.player_is_on_square[0], self.player_is_on_square[1] + 1]
            self.update()
        elif ans == 3:
            if self.player_is_on_ground:
                self.player_is_on_square = [self.player_is_on_square[0], self.player_is_on_square[1] + 1]
                self.update()
        elif ans == 2:
            if not self.player_is_on_ground:
                self.player_is_on_square = [self.player_is_on_square[0], self.player_is_on_square[1] + 1]
                self.update()

    def move_right(self):
        if self.player_is_on_square[0] > self.grid.get_width() - 2:
            return
        square = self.grid.get_grid()[self.player_is_on_square[0]][self.player_is_on_square[1]]
        other_square = self.grid.get_grid()[self.player_is_on_square[0] + 1][self.player_is_on_square[1]]
        ans = self.walls.is_there_wall_between(square, other_square)
        if not ans:
            self.player_is_on_square = [self.player_is_on_square[0] + 1, self.player_is_on_square[1]]
            self.update()
        elif ans == 3:
            if self.player_is_on_ground:
                self.player_is_on_square = [self.player_is_on_square[0] + 1, self.player_is_on_square[1]]
                self.update()
        elif ans == 2:
            if not self.player_is_on_ground:
                self.player_is_on_square = [self.player_is_on_square[0] + 1, self.player_is_on_square[1]]
                self.update()

    def jump(self):
        self.player_is_on_ground = not self.player_is_on_ground
        self.update()

    def solve_my_maze(self):
        self.maze_solved = True
        self.my_maze_solution = solve_maze(self.grid, self.walls,
                                           self.player_is_on_square,
                                           self.goal_is_on_square)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            self.move_up()
        if event.key() == Qt.Key_A:
            self.move_left()
        if event.key() == Qt.Key_S:
            self.move_down()
        if event.key() == Qt.Key_D:
            self.move_right()
        if event.key() == Qt.Key_Space:
            self.jump()
        if event.key() == Qt.Key_0:
            self.solve_my_maze()
        if event.key() == Qt.Key_T:
            self.test = True
            self.update()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Mane()
    sys.exit(App.exec())
