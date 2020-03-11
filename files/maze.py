from random import randint


def construct_maze(grid):
    max_x = grid.get_width()
    max_y = grid.get_heigth()
    while True:
        square = grid.get_inactive_square()
        coords = square.get_coords()
        grid.set_active(coords[0], coords[1])

        if not square:
            return
        n = randint(0, 3)  # 0 = top, 1 = left, 2 = right, 3 = bottom

        if n == 0:

            can_move_up = True
            if coords[0] < 1:
                can_move_up = False

            if can_move_up:
                other_square = [coords[0] - 1, coords[1]]
                other_square_active = grid.is_square_active(coords[0] - 1, coords[1])
                if other_square_active:
                    pass
