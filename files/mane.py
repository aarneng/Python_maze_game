from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
from test_grid import Walls
from grid2 import NewGrid
import maze


def scale_by(x):
    return 2 - 1 / (1 + x / 150)


class Mane(QMainWindow):
    def __init__(self):
        super().__init__()
        self.grid, self.walls = maze.construct_maze(NewGrid(width=5, height=5))
        self.x_offset = 100
        self.y_offset = 100
        self.x_squares = self.grid.get_width()
        self.y_squares = self.grid.get_height()
        self.width = 500 * scale_by(self.x_squares)
        self.height = 500 * scale_by(self.y_squares)
        self.square_size = min(self.width / self.x_squares, self.height / self.y_squares)
        self.toDraw = None

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
        painter = QPainter(self)
        painter.setPen(Qt.black)
        s = self.square_size
        horizontal_walls = self.walls.get_horizontal()
        vertical_walls = self.walls.get_vertical()
        for i in range(len(horizontal_walls)):
            for j in range(len(horizontal_walls[i])):
                if horizontal_walls[i][j].get_activity():
                    painter.drawLine(i * s + 10, j * s + 10, i * s + 10, (j + 1) * s + 10)
        for i in range(len(vertical_walls)):
            for j in range(len(vertical_walls[i])):
                if vertical_walls[i][j].get_activity():
                    painter.drawLine(i * s + 10, j * s + 10, (i + 1) * s + 10, j * s + 10)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Mane()
    sys.exit(App.exec())
