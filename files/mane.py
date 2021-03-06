from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit
import sys
from PyQt5.QtGui import QPainter, QPen, QFont, QColor
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import Qt, QUrl
from test_grid import Walls
from grid2 import NewGrid
import maze
from solve_maze import solve_maze
from read_write_files import write_file, read_file
from random import randint, choice


class Mane(QMainWindow):
    """
    https://www.reddit.com/r/ProgrammerHumor/comments/g7ohlb/front_end_vs_back_end/
    """
    def __init__(self):
        super().__init__()
        self.grid = NewGrid(width=10, height=10)
        self._grid_inactive_neighbours = self.grid.get_inactive_neighbours(0, 0)
        self.grid.set_active(0, 0)
        self.player_is_on_square = [0, 0]
        self.prev_square = None

        self.msg = ""
        self.show_animation = False  # Animation will take a long time for big grids, around (30x30 & +) depending on computer

        self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours, self.the_chosen_one = \
            maze.construct_maze(self.grid, Walls(self.grid), self._grid_inactive_neighbours, self.show_animation,
                                self.player_is_on_square)
        # self.grid, self.walls, self.msg = read_file("mymaze.txt")
        # self.maze_done = True
        # self._grid_inactive_neighbours = []

        self.display_solution = False
        self.x_offset = 100
        self.y_offset = 100
        self.x_squares = self.grid.get_width()
        self.y_squares = self.grid.get_height()
        self.width = 500
        self.height = 500
        self.square_size = min(self.width / self.x_squares, self.height / self.y_squares)
        self.toDraw = None
        self.show_menu = True

        self.goal_is_on_square = self.get_goal_square()
        self.player_is_on_ground = True

        self.my_maze_solution, self.all_answer_routes = solve_maze(self.grid, self.walls, self.player_is_on_square, self.goal_is_on_square)
        self.count = 0
        self.points = len(self.my_maze_solution) + 22

        self.allow_movement = True
        self.file_successful = None

        self.challenge_mode = False
        self.zombie_positions = [[0, self.x_squares - 1], [self.y_squares - 1, 0], [self.y_squares - 1, self.x_squares - 1]] + [[randint(0, self.x_squares - 1), randint(0, self.y_squares - 1)] for i in range(self.x_squares // 10 + self.y_squares // 10)]
        self.previous_zombie_positions = []
        self.player_is_dead = False
        self.challenge_key = [randint(int(self.y_squares / 4 - 1), self.y_squares - 1),
                              randint(int(self.x_squares / 4 - 1), self.x_squares - 1)]
        self.challenge_mode_key_found = False

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle("Labyrinth Y2")
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)  # make background white(er)
        self.setGeometry(self.x_offset, self.y_offset, self.width + 100, self.height + 150)
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

            painter.setPen(Qt.yellow)
            painter.setBrush(Qt.yellow)
            painter.drawEllipse(400, 150, 30, 30)
            painter.setPen(Qt.black)
            painter.setBrush(Qt.black)
            painter.drawEllipse(410, 155, 5, 5)
            painter.drawEllipse(420, 155, 5, 5)
            painter.drawArc(415, 165, 6, 4, 180 * 16, 180 * 16)

            painter.setPen(Qt.yellow)
            painter.setBrush(Qt.yellow)
            painter.drawEllipse(470, 150, 35, 35)
            painter.setPen(Qt.black)
            painter.setBrush(Qt.black)
            painter.drawEllipse(480, 155, 5, 5)
            painter.drawEllipse(490, 155, 5, 5)
            painter.drawEllipse(485, 165, 6, 4)

            painter.drawLine(435, 155, 465, 155)
            painter.drawLine(465, 155, 455, 145)
            painter.drawLine(465, 155, 455, 165)

            painter.drawLine(465, 175, 435, 175)
            painter.drawLine(435, 175, 445, 165)
            painter.drawLine(435, 175, 445, 185)
            # draw the smiley face guy

            painter.drawText(75, 220, "You can walk under green walls")
            painter.setPen(QPen(Qt.green, 4, Qt.SolidLine))
            painter.drawLine(60, 195, 60, 235)

            painter.setPen(Qt.black)
            painter.drawText(75, 270, "You can fly under blue walls")
            painter.setPen(QPen(Qt.blue, 4, Qt.SolidLine))
            painter.drawLine(60, 245, 60, 285)

            painter.setPen(Qt.black)
            painter.drawText(75, 320, "Press 0 if you're stuck. It'll show you what path to take :-)")
            painter.drawText(75, 360, "Alternatively, press 9 if you want to see how the path is found!")
            painter.setFont(QFont("Times", 10))
            painter.drawText(75, 380, "(Although some might call this cheating! This will also reset your points to 0)")

            painter.setPen(Qt.red)
            painter.setFont(QFont("Times", 20))

            if not self.challenge_mode:
                painter.drawText(75, 410, "Press 'C' to play in challenge mode!! (Includes zombies)")
            else:
                painter.drawText(75, 410, "Scared? Press 'C' again to not play in challenge mode :-)")

            painter.setPen(Qt.black)

            painter.drawText(75, 440, f"Maze size is currently {self.grid.get_width()} by {self.grid.get_height()}.")
            painter.drawText(75, 470, "Press the + and - buttons to change the size,")
            painter.drawText(75, 490, "or press I for a custom input and U for a random input")

            if not self.show_animation:
                painter.drawText(75, 520, "Press the enter key to show the maze's animation")
                painter.drawText(75, 550, "(this might take a while)")
            else:
                painter.drawText(75, 520, "Animation toggled on!")
                painter.drawText(75, 550, "Press the enter key to remove the maze's animation")

            painter.drawText(75, 590, "Left click to start the game")
            painter.drawText(75, 620, "Press F to read a file of your choice")
            painter.setFont(QFont("Times", 10))
            painter.drawText(75, 630, "Make sure you have saved it in the right directory!")
        else:
            painter.setPen(Qt.black)

            if not self.challenge_mode:
                painter.setFont(QFont("Times", 18))
                painter.drawText(75, 530, f"Press R at anytime to save your progress onto a file!")

                if self.file_successful:
                    painter.setFont(QFont("Times", 10))
                    painter.drawText(75, 540, f"File saved successfully!")

                if self.msg == "":
                    painter.setFont(QFont("Times", 14))
                    painter.drawText(75, 555, f"Current points: {self.points}")
                else:
                    painter.drawText(75, 550, f"{self.msg}")
                    painter.setFont(QFont("Times", 14))
                    if not self.msg.endswith("Did you type it in correctly?"):
                        #painter.drawText(75, 570, "(Please note that we do not check whether or not "
                        #                          "mazes from files are possible to complete)")
                        painter.drawText(75, 590, f"Current points: {self.points}")
                    else:
                        painter.drawText(75, 570, f"Current points: {self.points}")
                painter.drawText(75, 610, f"Lost? Press 0 to find the way to the goal! (resets points to 0)")
                painter.drawText(75, 630, f"If you want to see how a recursive search "
                                          f"algorithm finds the route to the goal, press 9!")

            else:
                painter.drawText(75, 550, f"No saving or finding solutions in challenge mode! Sorry!")

            s = self.square_size

            # The following code looks janky becuase drawing on PyQt is a pain

            if self.challenge_mode and self.maze_done:
                if any(self.player_is_on_square == i for i in self.zombie_positions) or any(self.player_is_on_square == i for i in self.previous_zombie_positions):
                    painter.setFont(QFont("Times", 34))
                    painter.drawText(50, 300, "you died!")
                    self.player_is_dead = True
                else:
                    def draw_zombie(paintr, pos):
                        painter.setBrush(Qt.green)
                        painter.setPen(Qt.black)
                        paintr.drawEllipse(pos[0] * s + 12, pos[1] * s + 12,s / 1.2, s / 1.2)
                        painter.setBrush(Qt.black)
                        painter.drawEllipse(pos[0] * s + 12, pos[1] * s + (s / 3.5) + 12, s / 5, s / 5)
                        painter.drawEllipse(pos[0] * s + (s / 3.5) + 12, pos[1] * s + (s / 3.5) + 12, s / 5, s / 5)
                        painter.drawLine(12 + pos[0] * s + s/4, 12 + pos[1] * s + s/3, 12 + pos[0] * s + s/2.5, 12 + pos[1] * s + s/6)
                        painter.drawLine(12 + pos[0] * s + s/10, 12 + pos[1] * s + s/6, 12 + pos[0] * s + s/4.5, 12 + pos[1] * s + s/3)
                        painter.setPen(Qt.white)
                        painter.setBrush(Qt.white)
                        painter.drawEllipse(pos[0] * s + 12, pos[1] * s + (s / 1.7) + 12, s / 3, s / 4)
                        painter.setPen(Qt.black)
                        painter.drawLine(pos[0] * s + 12 + s/20, pos[1] * s + (s / 1.7) + 12 + s/20, pos[0] * s + 12 + s/10, pos[1] * s + (s / 1.7) + 12 + s / 10)
                        painter.drawLine(pos[0] * s + 12 + s/10, pos[1] * s + (s / 1.7) + 12 + s / 10, pos[0] * s + 12 + s/8, pos[1] * s + (s / 1.7) + 12)

                    for i in range(len(self.zombie_positions)):
                        draw_zombie(painter, self.zombie_positions[i])
                    self.previous_zombie_positions = self.zombie_positions

                    def get_next_zombie_square(current_square):
                        ret, ignore = solve_maze(self.grid, self.walls, current_square, self.player_is_on_square)
                        return ret[1][::-1]

                    self.zombie_positions = [get_next_zombie_square(i) for i in self.zombie_positions]

                    painter.setBrush(Qt.white)
                    painter.setPen(Qt.black)

            def draw_key(pos, colour):
                painter.setBrush(colour)
                painter.drawEllipse(pos[0] * s + 12 + s / 3, pos[1] * s + 12, s / 2.5, s / 2.5)
                painter.drawRect(pos[0] * s + 12 + s / 2.2, pos[1] * s + 12 + s / 2.6, s / 8, s / 3)
                painter.drawRect(pos[0] * s + 12 + s / 3, pos[1] * s + 12 + s / 2.2, s / 8, s / 15)
                painter.drawRect(pos[0] * s + 12 + s / 3, pos[1] * s + 12 + s / 1.7, s / 8, s / 15)
                painter.setBrush(Qt.white)
                painter.drawEllipse(pos[0] * s + 12 + s / 2.1, pos[1] * s + 12 + s / 20, s / 8, s / 8)

            if self.challenge_mode:
                if self.player_is_on_square == self.challenge_key[::-1]:
                    self.challenge_mode_key_found = True
                if not self.challenge_mode_key_found:
                    draw_key(self.challenge_key[::-1], Qt.yellow)

            if not self.maze_done:
                for i in range(len(self.grid.get_grid())):
                    for j in range(len(self.grid.get_grid()[i])):
                        if not self.grid.get_grid()[i][j].get_active():
                            color = QColor(220, 220, 220)
                            painter.setBrush(color)
                            painter.setPen(color)
                            painter.drawRect(i * s + 11, j * s + 11, s, s)
                painter.setPen(QPen(QColor(150, 120, 150), 3, Qt.SolidLine))
                painter.drawRect(self.the_chosen_one[1] * s + 10, self.the_chosen_one[0] * s + 10, s, s)
                # sleep(1 / (self.x_squares + self.y_squares))
                painter.setPen(Qt.black)
                painter.setBrush(Qt.white)

            horizontal_walls = self.walls.get_horizontal()
            vertical_walls = self.walls.get_vertical()
            for i in range(len(horizontal_walls)):
                for j in range(len(horizontal_walls[i])):
                    if horizontal_walls[i][j].get_activity():
                        if horizontal_walls[i][j].get_activity() == 3:
                            if max(self.x_squares, self.y_squares) <= 15:
                                painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
                            else:
                                painter.setPen(Qt.green)
                            painter.drawLine(i * s + 10, j * s + 10, i * s + 10, (j + 1) * s + 10)
                            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                        elif horizontal_walls[i][j].get_activity() == 2:
                            if max(self.x_squares, self.y_squares) <= 15:
                                painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
                            else:
                                painter.setPen(Qt.blue)
                            painter.drawLine(i * s + 10, j * s + 10, i * s + 10, (j + 1) * s + 10)
                            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                        else:
                            painter.drawLine(i * s + 10, j * s + 10, i * s + 10, (j + 1) * s + 10)
            for i in range(len(vertical_walls)):
                for j in range(len(vertical_walls[i])):
                    if vertical_walls[i][j].get_activity():
                        if vertical_walls[i][j].get_activity() == 3:
                            if max(self.x_squares, self.y_squares) <= 15:
                                painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
                            else:
                                painter.setPen(Qt.green)
                            painter.drawLine(i * s + 10, j * s + 10, (i + 1) * s + 10, j * s + 10)
                            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                        elif vertical_walls[i][j].get_activity() == 2:
                            if max(self.x_squares, self.y_squares) <= 15:
                                painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
                            else:
                                painter.setPen(Qt.blue)
                            painter.drawLine(i * s + 10, j * s + 10, (i + 1) * s + 10, j * s + 10)
                            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                        else:
                            painter.drawLine(i * s + 10, j * s + 10, (i + 1) * s + 10, j * s + 10)
            # Draw walls, some with blue and some with green colors
            # yeah it's kinda ugly

            self.goal_is_on_square = self.get_goal_square()
            if self.goal_is_on_square != [-1, -1]:
                painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
                painter.setBrush(Qt.white)
                goal_x = self.goal_is_on_square[0]
                goal_y = self.goal_is_on_square[1]
                painter.drawRect(goal_x * s + 12, goal_y * s + 12, s / 1.2, s / 1.2)
                if self.challenge_mode and not self.challenge_mode_key_found:
                    painter.setBrush(Qt.gray)
                    painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
                    painter.drawRect(goal_x * s + 12, goal_y * s + 12, s / 1.2, s / 1.2)  # to get a grey square
                    draw_key(self.goal_is_on_square, Qt.black)

            player_x = self.player_is_on_square[0]
            player_y = self.player_is_on_square[1]

            if not self.player_is_dead:
                if self.player_is_on_ground:
                    painter.setPen(Qt.yellow)
                    painter.setBrush(Qt.yellow)
                    painter.drawEllipse(player_x * s + 12, player_y * s + 12, s / 1.2, s / 1.2)
                    painter.setPen(Qt.black)
                    painter.setBrush(Qt.black)
                    painter.drawEllipse(player_x * s + (s / 2.7) + 12, player_y * s + (s / 4) + 12, s / 6, s / 6)
                    painter.drawEllipse(player_x * s + (s / 1.6) + 12, player_y * s + (s / 4) + 12, s / 6, s / 6)
                    painter.drawArc(player_x * s + (s / 2.7) + 12, player_y * s + (s / 2) + 12,
                                    s / 4, s / 6, 180 * 16, 180 * 16)
                else:
                    painter.setPen(Qt.yellow)
                    painter.setBrush(Qt.yellow)
                    painter.drawEllipse(player_x * s + 12, player_y * s + 12, s, s)
                    painter.setPen(Qt.black)
                    painter.setBrush(Qt.black)
                    painter.drawEllipse(player_x * s + (s / 2.7) + 12, player_y * s + (s / 3.5) + 12, s / 5, s / 5)
                    painter.drawEllipse(player_x * s + (s / 1.6) + 12, player_y * s + (s / 3.5) + 12, s / 5, s / 5)
                    painter.drawEllipse(player_x * s + (s / 2.6) + 12, player_y * s + (s / 1.5) + 12, s / 3.5, s / 5)
                    # mouth open vs mouth closes (space bar animation)
            else:
                painter.setPen(QColor(150, 190, 50))
                painter.setBrush(QColor(150, 190, 50))
                painter.drawEllipse(player_x * s + 12, player_y * s + 12, s / 1.2, s / 1.2)
                painter.setPen(Qt.black)
                painter.setBrush(Qt.black)
                painter.drawEllipse(player_x * s + (s / 2.7) + 12, player_y * s + (s / 4) + 12, s / 6, s / 6)
                painter.drawEllipse(player_x * s + (s / 1.6) + 12, player_y * s + (s / 4) + 12, s / 6, s / 6)
                painter.drawArc(player_x * s + (s / 2.7) + 12, player_y * s + (s / 2) + 12,  s / 4, s / 6, 0, 180 * 16)
                # dead player after zombie eats it
            # Yes, i should really be working more with percentages here. Yes, the +12 is also
            # HORRIBLE coding practice. Please forgive me. I'll try to fix this later
            if self.show_animation and not self.maze_done:
                self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours, self.the_chosen_one = \
                    maze.construct_maze(self.grid, self.walls, self._grid_inactive_neighbours, self.show_animation,
                                        self.player_is_on_square)
                self.goal_is_on_square = self.get_goal_square()

                if self.maze_done:
                    self.my_maze_solution = solve_maze(self.grid, self.walls, self.player_is_on_square,
                                                       self.goal_is_on_square)
                    self.points = len(self.my_maze_solution) + 22
                self.update()

            if self.display_solution:
                def draw_solution(route):
                    prev = route[0]
                    for square in route:
                        painter.drawLine(prev[1] * s + 10 + s / 2, prev[0] * s + 10 + s / 2, square[1] * s + 10 + s / 2,
                                         square[0] * s + 10 + s / 2)
                        prev = square

                painter.setPen(Qt.red)
                if len(self.all_answer_routes) > self.count + 1:  # draw the routes taken to find answer, if animation is toggled
                    draw_solution(self.all_answer_routes[self.count])
                    self.count += 1
                    self.update()
                else:
                    draw_solution(self.my_maze_solution)
                painter.setPen(Qt.black)

            if self.player_is_on_square == self.goal_is_on_square:

                self.allow_movement = False
                explosion = QSoundEffect()
                explosion.setSource(QUrl("explosion.wav"))  # TODO: fix sound not playing (needs a loop?)
                explosion.play()

                painter.setOpacity(0.7)
                for i in range(100):  # draw the "explosion" at the end
                    painter.setBrush(choice([Qt.red, Qt.yellow, Qt.darkRed, Qt.white]))
                    s = randint(2, 250)
                    painter.drawEllipse(randint(0, 400), randint(0, 400), s, s)
                painter.setPen(Qt.black)
                painter.setOpacity(1)
                painter.setFont(QFont("Times", 65))
                painter.drawText(150, 270, "You won!")
                if not self.challenge_mode:
                    painter.drawText(50, 350, f"Your points: {self.points}")
                    if self.points >= 20:
                        painter.setFont(QFont("Times", 35))
                        painter.drawText(50, 400, "You are a true master of mazes!")
                    elif self.points >= 18:
                        painter.drawText(50, 400, "Well done!")
                    elif self.points > 0:
                        painter.drawText(50, 400, "Good try!")
                    else:
                        if not self.display_solution:
                            painter.setFont(QFont("Times", 25))
                            painter.drawText(50, 400, "Everyone solves mazes at their own pace :)")
                        else:
                            painter.drawText(50, 400, "I saw you cheat!")

    def get_goal_square(self):
        g = self.grid.get_grid()
        for i in range(len(g)):
            for j in range(len(g[i])):
                if g[i][j].get_goal_status() and self.maze_done:
                    return [i, j]
        return [-1, -1]  # else

    def get_player_square(self):
        g = self.grid.get_grid()
        for i in range(len(g)):
            for j in range(len(g[i])):
                if g[i][j].get_player_status() and self.maze_done:
                    return [i, j]
        return [-1, -1]  # else

    def move_to(self, square):
        if square == self.goal_is_on_square and self.challenge_mode and not self.challenge_mode_key_found:
            return
        if square[0] >= self.grid.get_height():
            return
        if square[1] >= self.grid.get_width():
            return

        ans = self.walls.is_there_wall_between(self.player_is_on_square[::-1], square[::-1], using_coords=True)

        if (not ans) or (ans == 2 and not self.player_is_on_ground) or (ans == 3 and self.player_is_on_ground):
            self.prev_square = self.player_is_on_square
            self.player_is_on_square = square
        else:
            return
        self.grid.remove_player_from_square(self.prev_square[0], self.prev_square[1])
        self.grid.add_player_to_square(self.player_is_on_square[0], self.player_is_on_square[1])

    def jump(self):
        self.player_is_on_ground = not self.player_is_on_ground
        self.update()

    def solve_my_maze(self, show_all=False):
        self.my_maze_solution, self.all_answer_routes = solve_maze(self.grid, self.walls, self.player_is_on_square,
                                           self.goal_is_on_square, show_all=show_all)
        if not self.my_maze_solution:  # if user inputs unsolvable maze we don't want to cause errors/crashes later on
            return
        # to show the solution from the player's square
        self.display_solution = True
        self.points = min(self.points, 0)  # reset points
        self.update()

    def keyPressEvent(self, event):
        if not self.allow_movement or self.player_is_dead:
            return

        # WARNING: the following code segments are big walls of copy/paste. I do not know how to
        # re-init my own class :-(
        # TODO: learn to re-init my own class and remove these ugly code blocks

        if event.key() == Qt.Key_Return and self.show_menu:
            self.show_animation = not self.show_animation
            self.grid = NewGrid(width=self.grid.get_width(), height=self.grid.get_height())
            self.player_is_on_square = [0, 0]
            self._grid_inactive_neighbours = self.grid.get_inactive_neighbours(0, 0)
            self.grid.get_square(self.player_is_on_square).set_active()
            self.prev_square = None

            self.x_squares = self.grid.get_width()
            self.y_squares = self.grid.get_height()
            self.square_size = min(self.width / self.x_squares, self.height / self.y_squares)

            if not self.challenge_mode:
                self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours, self.the_chosen_one = \
                    maze.construct_maze(self.grid, Walls(self.grid), self._grid_inactive_neighbours, self.show_animation,
                                        self.player_is_on_square)
            else:
                self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours, self.the_chosen_one = \
                    maze.construct_maze(self.grid, Walls(self.grid, wall_inverse_ratio=3), self._grid_inactive_neighbours,
                                        self.show_animation, self.player_is_on_square)
                # more ceiling / ground walls = more fun!
            self.goal_is_on_square = self.get_goal_square()

            self.update()

        if event.key() == Qt.Key_Plus and self.show_menu:
            self.grid = NewGrid(width=min(self.grid.get_width() + 1, 150), height=min(self.grid.get_height() + 1, 150))
            self.player_is_on_square = [0, 0]
            self._grid_inactive_neighbours = self.grid.get_inactive_neighbours(0, 0)
            self.grid.get_square(self.player_is_on_square).set_active()
            self.prev_square = None

            self.x_squares = self.grid.get_width()
            self.y_squares = self.grid.get_height()
            self.square_size = min(self.width / self.x_squares, self.height / self.y_squares)
            if not self.challenge_mode:
                self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours, self.the_chosen_one = \
                    maze.construct_maze(self.grid, Walls(self.grid), self._grid_inactive_neighbours, self.show_animation,
                                        self.player_is_on_square)
            else:
                self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours, self.the_chosen_one = \
                    maze.construct_maze(self.grid, Walls(self.grid, wall_inverse_ratio=3), self._grid_inactive_neighbours,
                                        self.show_animation, self.player_is_on_square)
            self.goal_is_on_square = self.get_goal_square()

            if not self.show_animation:
                self.my_maze_solution = solve_maze(self.grid, self.walls, self.player_is_on_square, self.goal_is_on_square)
                self.points = len(self.my_maze_solution) + 22

            self.zombie_positions = [[0, self.x_squares - 1], [self.y_squares - 1, 0],
                                     [self.y_squares - 1, self.x_squares - 1]] \
                                    + [[randint(0, self.x_squares - 1), randint(0, self.y_squares - 1)]
                                       for i in range(self.x_squares // 15 + self.y_squares // 15)]
            self.player_is_dead = False
            self.challenge_key = [randint(int(self.x_squares / 2 - 1), self.x_squares - 1),
                                  randint(int(self.y_squares / 2 - 1), self.y_squares - 1)]
            self.challenge_mode_key_found = False

            self.update()

        if event.key() == Qt.Key_Minus and self.show_menu:
            self.grid = NewGrid(width=max(self.grid.get_width() - 1, 2), height=max(self.grid.get_height() - 1, 2))
            self.player_is_on_square = [0, 0]
            self._grid_inactive_neighbours = self.grid.get_inactive_neighbours(0, 0)
            self.grid.get_square(self.player_is_on_square).set_active()
            self.prev_square = None

            self.x_squares = self.grid.get_width()
            self.y_squares = self.grid.get_height()
            self.square_size = min(self.width / self.x_squares, self.height / self.y_squares)

            if not self.challenge_mode:
                self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours, self.the_chosen_one = \
                    maze.construct_maze(self.grid, Walls(self.grid), self._grid_inactive_neighbours,
                                        self.show_animation, self.player_is_on_square)
            else:
                self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours, self.the_chosen_one = \
                    maze.construct_maze(self.grid, Walls(self.grid, wall_inverse_ratio=3),
                                        self._grid_inactive_neighbours, self.show_animation, self.player_is_on_square)
            self.goal_is_on_square = self.get_goal_square()

            if not self.show_animation:
                self.my_maze_solution = solve_maze(self.grid, self.walls, self.player_is_on_square, self.goal_is_on_square)
                self.points = len(self.my_maze_solution) + 22

            self.zombie_positions = [[0, self.x_squares - 1], [self.y_squares - 1, 0], [self.y_squares - 1, self.x_squares - 1]] + [[randint(0, self.x_squares - 1), randint(0, self.y_squares - 1)] for i in range(self.x_squares // 10 + self.y_squares // 10)]
            self.player_is_dead = False
            self.challenge_key = [randint(int(self.x_squares / 2 - 1), self.x_squares - 1),
                                  randint(int(self.y_squares / 2 - 1), self.y_squares - 1)]
            self.challenge_mode_key_found = False

            self.update()

        if event.key() == Qt.Key_I and self.show_menu:
            width, bl = QInputDialog.getInt(self, "How big do you want your grid to be?", "Height:", 10)
            width = min(max(width, 2), 150)
            height, bl = QInputDialog.getInt(self, "How big do you want your grid to be?", "Width:", 10)
            height = min(max(height, 2), 150)
            self.grid = NewGrid(width=width, height=height)
            self.player_is_on_square = [0, 0]
            self._grid_inactive_neighbours = self.grid.get_inactive_neighbours(0, 0)
            self.grid.get_square(self.player_is_on_square).set_active()
            self.prev_square = None

            self.x_squares = self.grid.get_width()
            self.y_squares = self.grid.get_height()
            self.square_size = min(self.width / self.x_squares, self.height / self.y_squares)

            if not self.challenge_mode:
                self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours, self.the_chosen_one = \
                    maze.construct_maze(self.grid, Walls(self.grid), self._grid_inactive_neighbours, self.show_animation,
                                        self.player_is_on_square)
            else:
                self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours, self.the_chosen_one = \
                    maze.construct_maze(self.grid, Walls(self.grid, wall_inverse_ratio=3),
                                        self._grid_inactive_neighbours, self.show_animation, self.player_is_on_square)
            self.goal_is_on_square = self.get_goal_square()

            if not self.show_animation:
                self.my_maze_solution = solve_maze(self.grid, self.walls, self.player_is_on_square, self.goal_is_on_square)
                self.points = len(self.my_maze_solution) + 22

            self.zombie_positions = [[0, self.x_squares - 1], [self.y_squares - 1, 0], [self.y_squares - 1, self.x_squares - 1]] + [[randint(0, self.x_squares - 1), randint(0, self.y_squares - 1)] for i in range(self.x_squares // 10 + self.y_squares // 10)]
            self.player_is_dead = False
            self.challenge_key = [randint(int(self.x_squares / 2 - 1), self.x_squares - 1),
                                  randint(int(self.y_squares / 2 - 1), self.y_squares - 1)]
            self.challenge_mode_key_found = False

            self.update()

        if event.key() == Qt.Key_U and self.show_menu:
            width = min(randint(5, 150), randint(5, 150), randint(5, 150), randint(5, 150))
            height = min(randint(5, 150), randint(5, 150), randint(5, 150), randint(5, 150))
            # a really thin grid isn't fun to play on
            self.grid = NewGrid(width=width, height=height)
            self.player_is_on_square = [0, 0]
            self._grid_inactive_neighbours = self.grid.get_inactive_neighbours(0, 0)
            self.grid.get_square(self.player_is_on_square).set_active()
            self.prev_square = None

            self.x_squares = self.grid.get_width()
            self.y_squares = self.grid.get_height()
            self.square_size = min(self.width / self.x_squares, self.height / self.y_squares)

            if not self.challenge_mode:
                self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours, self.the_chosen_one = \
                    maze.construct_maze(self.grid, Walls(self.grid), self._grid_inactive_neighbours, self.show_animation,
                                        self.player_is_on_square)
            else:
                self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours, self.the_chosen_one = \
                    maze.construct_maze(self.grid, Walls(self.grid, wall_inverse_ratio=3),
                                        self._grid_inactive_neighbours, self.show_animation, self.player_is_on_square)
            self.goal_is_on_square = self.get_goal_square()

            if not self.show_animation:
                self.my_maze_solution = solve_maze(self.grid, self.walls, self.player_is_on_square, self.goal_is_on_square)
                self.points = len(self.my_maze_solution) + 22

            self.zombie_positions = [[0, self.x_squares - 1], [self.y_squares - 1, 0], [self.y_squares - 1, self.x_squares - 1]] + [[randint(0, self.y_squares - 1), randint(0, self.x_squares - 1)] for i in range(self.x_squares // 10 + self.y_squares // 10)]
            self.player_is_dead = False
            self.challenge_key = [randint(int(self.x_squares / 2 - 1), self.x_squares - 1),
                                  randint(int(self.y_squares / 2 - 1), self.y_squares - 1)]
            self.challenge_mode_key_found = False

            self.update()

        if event.key() == Qt.Key_F and self.show_menu:
            fn, bl = QInputDialog.getText(self, "Which file would you like to read?", "Filename:",
                                          QLineEdit.Normal, "mymaze.txt")
            if not fn.endswith(".txt"):
                fn += ".txt"
            try:
                self.challenge_mode = False
                self.grid, self.walls, self.msg, self.points = read_file(fn)
                self.maze_done = True

                self.x_squares = self.grid.get_width()
                self.y_squares = self.grid.get_height()
                self.square_size = min(self.width / self.x_squares, self.height / self.y_squares)
                self._grid_inactive_neighbours = []
                self.goal_is_on_square = self.get_goal_square()
                self.player_is_on_square = self.get_player_square()
                if self.player_is_on_square == [-1, -1]:
                    self.player_is_on_square = [0, 0]
                if self.goal_is_on_square == [-1, -1]:
                    self.grid.make_goal(randint(int(self.y_squares / 2), self.y_squares - 1), randint(int(self.x_squares / 2), self.x_squares - 1))
                    self.goal_is_on_square = self.get_goal_square()

                self.my_maze_solution, self.all_answer_routes = solve_maze(self.grid, self.walls, self.player_is_on_square, self.goal_is_on_square)
                if self.my_maze_solution is not False:
                    pass
                else:
                    raise IndexError  # for lack of a better error type
                self.update()
            except FileNotFoundError:
                self.msg = f"File < {fn} > was not found! Did you type it in correctly?"
            except IndexError:
                self.msg = f"File < {fn} > is not possible to be solved!"
            self.update()

        if event.key() == Qt.Key_C and self.show_menu:
            self.challenge_mode = not self.challenge_mode
            if self.challenge_mode:
                self.grid = NewGrid(width=self.grid.get_width(), height=self.grid.get_height())
                self._grid_inactive_neighbours = self.grid.get_inactive_neighbours(0, 0)
                self.grid.set_active(0, 0)
                self.player_is_on_square = [0, 0]
                self.prev_square = None
                self.grid, self.walls, self.maze_done, self._grid_inactive_neighbours, self.the_chosen_one = \
                    maze.construct_maze(self.grid, Walls(self.grid, wall_inverse_ratio=3),
                                        self._grid_inactive_neighbours, self.show_animation, self.player_is_on_square)
            self.update()

        if not self.maze_done:
            return

        if event.key() == Qt.Key_R and not self.challenge_mode:
            fn, bl = QInputDialog.getText(self, "Enter filename under which you want this saved!", "Filename:",
                                          QLineEdit.Normal, "mymaze.txt")
            if not fn.endswith(".txt"):
                fn += ".txt"
            self.file_successful = write_file(self.grid, self.walls, fn, self.points)

        if self.all_answer_routes and self.count + 1 != len(self.all_answer_routes):
            return

        if self.show_menu:  # don't want users from playing around in the maze while still in the menu
            return

        if event.key() == Qt.Key_9 and not self.challenge_mode:
            self.solve_my_maze(show_all=True)

        if event.key() == Qt.Key_0 and not self.challenge_mode:
            self.solve_my_maze()

        if event.key() == Qt.Key_W:
            self.points -= 1
            self.move_to([self.player_is_on_square[0], self.player_is_on_square[1] - 1])
            self.update()

        if event.key() == Qt.Key_A:
            self.points -= 1
            self.move_to([self.player_is_on_square[0] - 1, self.player_is_on_square[1]])
            self.update()

        if event.key() == Qt.Key_S:
            self.points -= 1
            self.move_to([self.player_is_on_square[0], self.player_is_on_square[1] + 1])
            self.update()

        if event.key() == Qt.Key_D:
            self.points -= 1
            self.move_to([self.player_is_on_square[0] + 1, self.player_is_on_square[1]])
            self.update()

        if event.key() == Qt.Key_Space:
            self.jump()

    def mousePressEvent(self, event):
        if not self.allow_movement:
            return

        self.show_menu = False
        self.update()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Mane()
    sys.exit(App.exec())
