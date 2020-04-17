from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit
import sys
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont
from PyQt5.QtMultimedia import QSound, QSoundEffect
from PyQt5.QtCore import Qt, QCoreApplication, QUrl
from test_grid import Walls
from grid2 import NewGrid
import maze
from solve_maze import solve_maze
from read_write_files import write_file, read_file
from random import randint, choice
from time import sleep


def scale_by(x):
    return 2 - 1 / (1 + x / 150)


class Mane(QMainWindow):
    def __init__(self):
        super().__init__()
        self.test = False
        self.grid = NewGrid(width=10, height=10)
        self._grid_inactive_neighbours = self.grid.get_inactive_neighbours(0, 0)
        self.grid.set_active(0, 0)
        self.player_is_on_square = [0, 0]
        self.prev_square = None

        self.show_animation = False  # Animation will take a long time for big grids, around (30x30 & +) depending on computer
        self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours = maze.construct_maze(self.grid, Walls(self.grid), self._grid_inactive_neighbours, self.show_animation, self.player_is_on_square)
        #self.grid, self.walls, self.msg = read_file("mymaze.txt")
        #self.maze_done = True
        #self._grid_inactive_neighbours = []

        self.maze_solved = not self.show_animation
        self.my_maze_solution = []
        self.x_offset = 100
        self.y_offset = 100
        self.x_squares = self.grid.get_width()
        self.y_squares = self.grid.get_height()
        self.width = 500
        self.height = 500
        self.square_size = max(self.width / self.x_squares, self.height / self.y_squares)
        self.toDraw = None
        self.show_menu = True

        self.goal_is_on_square = self.get_goal_square()
        self.player_is_on_ground = True

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle("Labyrinth Y2")
        self.setGeometry(self.x_offset, self.y_offset, self.width + 100, self.height + 100)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.show_menu:
            painter.setFont(QFont("Times", 50))
            painter.drawText(50, 50, "Welcome to my maze!")

            painter.setFont(QFont("Times", 20))

            painter.drawRoundedRect(30, 80, 25, 25, 5, 5)
            painter.drawText(33, 100, "W")
            painter.drawRoundedRect(5, 105, 25, 25, 5, 5)
            painter.drawText(10, 125, "A")
            painter.drawRoundedRect(30, 105, 25, 25, 5, 5)
            painter.drawText(35, 125, "S")
            painter.drawRoundedRect(55, 105, 25, 25, 5, 5)
            painter.drawText(60, 125, "D")

            painter.drawText(100, 125, "Move your character with the WASD keys")

            painter.drawRoundedRect(10, 155, 60, 20, 5, 5)
            painter.drawText(75, 170, "Toggle flight by pressing the spacebar")

            painter.drawText(75, 220, "You can walk under green walls")
            painter.setPen(QPen(Qt.green, 4, Qt.SolidLine))
            painter.drawLine(60, 195, 60, 235)

            painter.setPen(Qt.black)
            painter.drawText(75, 270, "You can fly under blue walls")
            painter.setPen(QPen(Qt.blue, 4, Qt.SolidLine))
            painter.drawLine(60, 245, 60, 285)

            painter.setPen(Qt.black)
            painter.drawText(75, 320, "Press 0 if you're stuck. It'll show you what path to take")
            painter.setFont(QFont("Times", 10))
            painter.drawText(75, 340, "(although some might call this cheating!)")

            painter.setFont(QFont("Times", 20))

            if not self.show_animation:
                painter.drawText(75, 400, "Press the enter key to show the maze's animation")
            else:
                painter.drawText(75, 400, "Animation toggled on!")
                painter.drawText(75, 430, ("Press the enter key to remove the maze's animation"))

            painter.drawText(75, 500, "Left click to start the game")

        else:
            painter.setPen(Qt.black)
            s = self.square_size
            horizontal_walls = self.walls.get_horizontal()
            vertical_walls = self.walls.get_vertical()
            for i in range(len(horizontal_walls)):
                for j in range(len(horizontal_walls[i])):
                    if horizontal_walls[i][j].get_activity():
                        if horizontal_walls[i][j].get_activity() == 3:
                            painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
                            painter.drawLine(i * s + 10, j * s + 10, i * s + 10, (j + 1) * s + 10)
                            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                        elif horizontal_walls[i][j].get_activity() == 2:
                            painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
                            painter.drawLine(i * s + 10, j * s + 10, i * s + 10, (j + 1) * s + 10)
                            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                        else:
                            painter.drawLine(i * s + 10, j * s + 10, i * s + 10, (j + 1) * s + 10)
            for i in range(len(vertical_walls)):
                for j in range(len(vertical_walls[i])):
                    if vertical_walls[i][j].get_activity():
                        if vertical_walls[i][j].get_activity() == 3:
                            painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
                            painter.drawLine(i * s + 10, j * s + 10, (i + 1) * s + 10, j * s + 10)
                            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                        elif vertical_walls[i][j].get_activity() == 2:
                            painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
                            painter.drawLine(i * s + 10, j * s + 10, (i + 1) * s + 10, j * s + 10)
                            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                        else:
                            painter.drawLine(i * s + 10, j * s + 10, (i + 1) * s + 10, j * s + 10)

            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))

            self.goal_is_on_square = self.get_goal_square()

            goal_x = self.goal_is_on_square[0]
            goal_y = self.goal_is_on_square[1]
            painter.drawRect(goal_x * s + 12, goal_y * s + 12, s / 1.2, s / 1.2)

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
                self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours = maze.construct_maze(self.grid,
                                                                                                            self.walls,
                                                                                                            self._grid_inactive_neighbours,
                                                                                                            self.show_animation)
                self.update()

            if self.maze_solved:
                painter.setPen(Qt.red)
                try:
                    prev = self.my_maze_solution[0]
                except IndexError:
                    prev = [0, 0]  # just in case

                for square in self.my_maze_solution:
                    painter.drawLine(prev[0] * s + 10 + s / 2, prev[1] * s + 10 + s / 2, square[0] * s + 10 + s / 2,
                                     square[1] * s + 10 + s / 2)
                    prev = square
                painter.setPen(Qt.black)

            if self.player_is_on_square == self.goal_is_on_square:

                explosion = QSoundEffect()
                explosion.setSource(QUrl("explosion.wav"))
                explosion.play()

                painter.setOpacity(0.7)
                for i in range(100):
                    painter.setBrush(choice([Qt.red, Qt.yellow, Qt.darkRed, Qt.white]))
                    s = randint(2, 250)
                    painter.drawEllipse(randint(0, 400), randint(0, 400), s, s)
                painter.setPen(Qt.black)
                painter.setOpacity(1)
                painter.setFont(QFont("Times", 75))
                painter.drawText(150, 270, "You won!")

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
        wall = self.walls.is_there_wall_between(square, other_square)
        if not wall:
            self.prev_square = self.player_is_on_square
            self.player_is_on_square = [self.player_is_on_square[0], self.player_is_on_square[1] - 1]
        elif wall == 3:
            if self.player_is_on_ground:
                self.prev_square = self.player_is_on_square
                self.player_is_on_square = [self.player_is_on_square[0], self.player_is_on_square[1] - 1]
        elif wall == 2:
            if not self.player_is_on_ground:
                self.prev_square = self.player_is_on_square
                self.player_is_on_square = [self.player_is_on_square[0], self.player_is_on_square[1] - 1]
        else:
            return
        self.grid.remove_player_from_square(self.prev_square[0], self.prev_square[1])
        self.grid.add_player_to_square(self.player_is_on_square[0], self.player_is_on_square[1])
        self.update()

    def move_left(self):
        square = self.grid.get_grid()[self.player_is_on_square[0]][self.player_is_on_square[1]]
        other_square = self.grid.get_grid()[self.player_is_on_square[0] - 1][self.player_is_on_square[1]]
        ans = self.walls.is_there_wall_between(square, other_square)
        if not ans:
            self.prev_square = self.player_is_on_square
            self.player_is_on_square = [self.player_is_on_square[0] - 1, self.player_is_on_square[1]]
        elif ans == 3:
            if self.player_is_on_ground:
                self.prev_square = self.player_is_on_square
                self.player_is_on_square = [self.player_is_on_square[0] - 1, self.player_is_on_square[1]]
        elif ans == 2:
            if not self.player_is_on_ground:
                self.prev_square = self.player_is_on_square
                self.player_is_on_square = [self.player_is_on_square[0] - 1, self.player_is_on_square[1]]
        else:
            return
        self.grid.remove_player_from_square(self.prev_square[0], self.prev_square[1])
        self.grid.add_player_to_square(self.player_is_on_square[0], self.player_is_on_square[1])
        self.update()

    def move_down(self):
        if self.player_is_on_square[1] > self.grid.get_height() - 2:
            return
        square = self.grid.get_grid()[self.player_is_on_square[0]][self.player_is_on_square[1]]
        other_square = self.grid.get_grid()[self.player_is_on_square[0]][self.player_is_on_square[1] + 1]
        wall = self.walls.is_there_wall_between(square, other_square)
        if not wall:
            self.prev_square = self.player_is_on_square
            self.player_is_on_square = [self.player_is_on_square[0], self.player_is_on_square[1] + 1]
        elif wall == 3:
            if self.player_is_on_ground:
                self.prev_square = self.player_is_on_square
                self.player_is_on_square = [self.player_is_on_square[0], self.player_is_on_square[1] + 1]
        elif wall == 2:
            if not self.player_is_on_ground:
                self.prev_square = self.player_is_on_square
                self.player_is_on_square = [self.player_is_on_square[0], self.player_is_on_square[1] + 1]
        else:
            return
        self.grid.remove_player_from_square(self.prev_square[0], self.prev_square[1])
        self.grid.add_player_to_square(self.player_is_on_square[0], self.player_is_on_square[1])
        self.update()

    def move_right(self):
        if self.player_is_on_square[0] > self.grid.get_width() - 2:
            return
        square = self.grid.get_grid()[self.player_is_on_square[0]][self.player_is_on_square[1]]
        other_square = self.grid.get_grid()[self.player_is_on_square[0] + 1][self.player_is_on_square[1]]
        ans = self.walls.is_there_wall_between(square, other_square)
        if not ans:
            self.prev_square = self.player_is_on_square
            self.player_is_on_square = [self.player_is_on_square[0] + 1, self.player_is_on_square[1]]
        elif ans == 3:
            if self.player_is_on_ground:
                self.prev_square = self.player_is_on_square
                self.player_is_on_square = [self.player_is_on_square[0] + 1, self.player_is_on_square[1]]
        elif ans == 2:
            if not self.player_is_on_ground:
                self.prev_square = self.player_is_on_square
                self.player_is_on_square = [self.player_is_on_square[0] + 1, self.player_is_on_square[1]]
        else:
            return

        self.grid.remove_player_from_square(self.prev_square[0], self.prev_square[1])
        self.grid.add_player_to_square(self.player_is_on_square[0], self.player_is_on_square[1])
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
        if event.key() == Qt.Key_Return:
            self.show_animation = not self.show_animation
            self.update()
        if event.key() == Qt.Key_R:
            fn, bl = QInputDialog.getText(self, "Get text", "Filename:", QLineEdit.Normal)
            print(fn)
            write_file(self.grid, self.walls, fn + ".txt")

    def mousePressEvent(self, event):
        self.show_menu = False
        self.update()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Mane()
    sys.exit(App.exec())
