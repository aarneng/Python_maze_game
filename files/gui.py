from PyQt5 import QtWidgets, QtCore, QtGui


class GUI(QtWidgets.QMainWindow):
    def __init__(self, world, square_size):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())  # QMainWindown must have a centralWidget to be able to add layouts
        self.horizontal = QtWidgets.QHBoxLayout()  # Horizontal main layout
        self.centralWidget().setLayout(self.horizontal)
        self.world = world
        self.square_size = square_size
        self.init_window()
        self.init_buttons()
        #self.gui_exercise = GuiExercise(self.world, self.scene, self.square_size)

        self.add_robot_world_grid_items()
        self.add_robot_graphics_items()
        self.update_robots()

        # Set a timer to call the update function periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_robots)
        self.timer.start(10)  # Milliseconds

    def init_window(self):
        '''
        Sets up the window.
        '''
        self.setGeometry(300, 300, 800, 800)
        self.setWindowTitle('RobotWorld')
        self.show()

        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 700, 700)

        # Add a view for showing the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)
