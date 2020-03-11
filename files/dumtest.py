from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Drawing Rectangle"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def paintEvent(self, e):
        x_s = 20
        y_s = 15
        sq_x_size = self.width / x_s
        sq_y_size = self.height / y_s
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 8, Qt.SolidLine))
        painter.drawRect(40, 40, 400, 200)
        """for i in range(x_s):
            for j in range(y_s):
                painter.drawRect(i * sq_x_size, j * sq_y_size,
                                 sq_x_size, sq_y_size)"""
        print("test")


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
