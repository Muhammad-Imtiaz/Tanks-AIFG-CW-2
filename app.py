from copy import deepcopy
import random
import time
import arcade
import math
import sys
import ANN
import numpy
import pandas as pd
import xlwt

class Tanks(arcade.Window):
    size = 15
    turn = 4
    grid = []

    fire = 50

    is_dead = 0

    input = 225
    hidden = 10

    score_board_p1 = []
    score_board_p2 = []
    score_board_p3 = []
    score_board_p4 = []

    tank_destroying_score = 50

    score_p1 = 0
    score_p2 = 0
    score_p3 = 0
    score_p4 = 0

    up_1 = 11
    down_1 = 13
    left_1 = 14
    right_1 = 12

    up_2 = 21
    down_2 = 23
    left_2 = 24
    right_2 = 22

    up_3 = 31
    down_3 = 33
    left_3 = 34
    right_3 = 32

    up_4 = 41
    down_4 = 43
    left_4 = 44
    right_4 = 42

    SPRITE_SCALING_PLAYER = 0.18
    SPRITE_SCALING_PLAYER1 = 0.82
    stone = 100

    w1 = []
    w2 = []

    total_turn = 1

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.width = width
        self.height = height
        self.player_sprite = None
        self.sprite_list = None

        arcade.set_background_color(arcade.color.WHITE)
        self.initialize_grid()
        self.initialize_score_board()
        self.w1 = self.generate_matrix(self.input, self.hidden)
        self.w2 = self.generate_matrix(self.hidden, 7)
        # dataframe = pd.DataFrame({'W1': [], 'w2': [], 'score': []})
        # dataframe.to_excel('data.xls', index=False)

    def initialize_grid(self):
        for row in range(self.size):
            self.grid.append([])
            for column in range(self.size):
                self.grid[row].append(0)

        self.grid[0][0] = self.right_1
        self.grid[0][self.size - 1] = self.down_2
        self.grid[self.size - 1][0] = self.up_4
        self.grid[self.size - 1][self.size - 1] = self.left_3

        for i in range(3):
            self.grid[i][7] = self.stone
            self.grid[7][i] = self.stone
        i = 14
        while i > 11:
            self.grid[i][7] = self.stone
            self.grid[7][i] = self.stone
            i -= 1

        self.grid[3][3] = self.stone
        self.grid[3][4] = self.stone
        self.grid[3][10] = self.stone
        self.grid[3][11] = self.stone

        self.grid[4][3] = self.stone
        self.grid[4][11] = self.stone
        self.grid[5][7] = self.stone
        self.grid[7][5] = self.stone

        self.grid[7][7] = self.stone
        self.grid[7][9] = self.stone

        self.grid[9][7] = self.stone

        self.grid[9][7] = self.stone
        self.grid[10][3] = self.stone
        self.grid[10][11] = self.stone

        self.grid[11][3] = self.stone
        self.grid[11][4] = self.stone
        self.grid[11][10] = self.stone
        self.grid[11][11] = self.stone



    def initialize_score_board(self):
        for row in range(self.size):
            self.score_board_p1.append([])
            self.score_board_p2.append([])
            self.score_board_p3.append([])
            self.score_board_p4.append([])
            for column in range(self.size):
                self.score_board_p1[row].append(0)
                self.score_board_p2[row].append(0)
                self.score_board_p3[row].append(0)
                self.score_board_p4[row].append(0)
        self.score_board_p1[0][0] = 1
        self.score_board_p2[0][self.size - 1] = 2
        self.score_board_p3[self.size - 1][self.size - 1] = 3
        self.score_board_p4[self.size - 1][0] = 4
        # add scores to 1 initially
        self.score_p1 += 1
        self.score_p2 += 1
        self.score_p3 += 1
        self.score_p4 += 1

    def draw_screen(self):

        ri = self.width / self.size
        ci = self.height / self.size
        ri1 = self.width / self.size
        ci1 = self.height / self.size
        for i in range(self.size - 1):
            arcade.draw_line(0, ci, self.width, ci, arcade.color.BLACK)
            arcade.draw_line(ri, 0, ri, self.height, arcade.color.BLACK)
            ri += ri1
            ci += ci1

        for i in range(self.size):
            for j in range(self.size):
                bw = self.width / self.size
                bh = self.height / self.size
                ri = int(bw / 2)
                ci = int(bh / 2)

                if self.grid[i][j] is 0:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                elif self.grid[i][j] is self.right_1:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("1_right.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                elif self.grid[i][j] is self.left_1:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("1_left.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    # arcade.draw_circle_filled(i * bw + ri, j * bh + ci, bw / 4, arcade.color.AMAZON)
                elif self.grid[i][j] is self.up_1:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("1_up.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                elif self.grid[i][j] is self.down_1:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("1_down.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                elif self.grid[i][j] is self.right_2:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("2_right.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                elif self.grid[i][j] is self.left_2:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("2_left.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    # arcade.draw_circle_filled(i * bw + ri, j * bh + ci, bw / 4, arcade.color.AMAZON)
                elif self.grid[i][j] is self.up_2:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("2_up.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                elif self.grid[i][j] is self.down_2:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("2_down.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                elif self.grid[i][j] is self.right_3:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("3_right.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                elif self.grid[i][j] is self.left_3:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("3_left.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                    # arcade.draw_circle_filled(i * bw + ri, j * bh + ci, bw / 4, arcade.color.AMAZON)
                elif self.grid[i][j] is self.up_3:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("3_up.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                elif self.grid[i][j] is self.down_3:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("3_down.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                elif self.grid[i][j] is self.right_4:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("4_right.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                elif self.grid[i][j] is self.left_4:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("4_left.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    # arcade.draw_circle_filled(i * bw + ri, j * bh + ci, bw / 4, arcade.color.AMAZON)
                elif self.grid[i][j] is self.up_4:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("4_up.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                elif self.grid[i][j] is self.down_4:
                    self.player_sprite = arcade.Sprite("background.png", self.SPRITE_SCALING_PLAYER1)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    self.player_sprite = arcade.Sprite("4_down.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                elif self.grid[i][j] is self.stone:
                    self.player_sprite = arcade.Sprite("stone.png", 0.022)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                elif self.grid[i][j] is self.fire:
                    self.player_sprite = arcade.Sprite("fire.png", 0.25)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

        self.player_list.draw()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        self.draw_screen()

    def setup(self):
        # Sprite lists
        self.player_list = arcade.SpriteList()

    def turn_change(self, turn):
        if turn is 1:
            # print(turn)
            turn = 2
        elif turn is 2:
            turn = 3
        elif turn is 3:
            turn = 4
        elif turn is 4:
            turn = 1
        return turn

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_list.update()
        # print('phela')
        # print(self.grid)
        time.sleep(1)
        p, q = self.get_current_pos(self.grid, self.turn)
        if p != -1 and q != -1:
            if self.turn == 1:
                list = (self.generate_childern(self.grid, self.turn))
                output = len(list)
                # print(str(output) + ' Length')
                one_D = self.generate_1D(self.grid)
                m = []
                m.extend(self.w2[:output + 1])
                # print(m)

                score = ANN.predict_outputs(self.w1, self.w2, one_D, output)
                # print(score, 'scroe')
                self.grid = list[score]
                # print(self.grid)
            else:
                self.grid = self.make_move(self.grid, self.turn)
                print(self.grid)
            self.update_score_board(self.grid, self.turn)
            # print('dosra')
        self.turn = self.turn_change(self.turn)
        self.total_turn += 1
        if self.total_turn == 1000 or self.is_dead == 3:
            print(self.winner())
            time.sleep(2)
            sys.exit('Game Exit')

        # print('dosra')
        # print(self.grid)

    def winner(self):
        maximum = max(self.score_p1, self.score_p2, self.score_p3, self.score_p4)
        if maximum == self.score_p1:
            return 'Player 1 win!!!'
        elif maximum == self.score_p2:
            return 'Player 2 win!!!'
        elif maximum == self.score_p3:
            return 'Player 3 win!!!'
        elif maximum == self.score_p4:
            return 'Player 4 win!!!'


    def update_score_board(self, board, turn):
        i, j = self.get_current_pos(board, turn)
        if i != -1 and j != -1:
            if turn == 1:
                if self.score_board_p1[i][j] == 0:
                    self.score_board_p1[i][j] = 1
                    self.score_p1 += 1
                    # print('player 1:' + str(self.score_p1))
            elif turn == 2:
                if self.score_board_p2[i][j] == 0:
                    self.score_board_p2[i][j] = 2
                    self.score_p2 += 1
                    # print('player 2:' + str(self.score_p2))
            elif turn == 3:
                if self.score_board_p3[i][j] == 0:
                    self.score_board_p3[i][j] = 3
                    self.score_p3 += 1
                    # print('player 3:' + str(self.score_p3))
            elif turn == 4:
                if self.score_board_p4[i][j] == 0:
                    self.score_board_p4[i][j] = 4
                    self.score_p4 += 1
                    # print('player 4:' + str(self.score_p4))

    def generate_childern(self, board, turn):

        fired = False

        list = []
        copy1 = deepcopy(board)
        copy2 = deepcopy(board)
        copy3 = deepcopy(board)
        copy4 = deepcopy(board)
        copy5 = deepcopy(board)
        copy6 = deepcopy(board)
        # board = deepcopy(board)

        # generating fired child
        direction = self.get_current_direction(board, turn)
        m, n = self.get_current_pos(board, turn)

        if turn == 1:
            if direction == self.up_1:
                for i in range(self.size):
                    # print(n + 1)
                    if n + i + 1 < self.size:
                        if board[m][n + i + 1] == self.stone or board[n - i - 1][n] == self.fire:
                            break
                        elif board[m][n + i + 1] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            print(board[m][n + i + 1])
                            fired = True
                            board[m][n + i + 1] = self.fire
                            self.is_dead += 1
                            self.score_p1 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
            elif direction == self.down_1:
                for i in range(self.size):
                    if n - i - 1 >= 0:
                        if board[m][n - i - 1] == self.stone or board[n - i - 1][n] == self.fire:
                            break
                        elif board[m][n - i - 1] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            print(board[m][n - i - 1])
                            fired = True
                            board[m][n - i - 1] = self.fire
                            self.is_dead += 1
                            self.score_p1 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break

            elif direction == self.right_1:
                for i in range(self.size):
                    if m + i + 1 < self.size:
                        if board[m + i + 1][n] == self.stone or board[m + i + 1][n] == self.fire:
                            break
                        elif board[m + i + 1][n] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            print(board[m + i + 1][n])
                            fired = True
                            board[m + i + 1][n] = self.fire
                            self.is_dead += 1
                            self.score_p1 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
            elif direction == self.left_1:
                for i in range(self.size):
                    if m - i - 1 >= 0:
                        if board[m - i - 1][n] == self.stone or board[m - i - 1][n] == self.fire:
                            break
                        elif board[m - i - 1][n] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            print(board[m - i - 1][n])
                            fired = True
                            board[m - i - 1][n] = self.fire
                            self.is_dead += 1
                            self.score_p1 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
        elif turn == 2:
            if direction == self.up_2:
                for i in range(self.size):
                    if n + i + 1 < self.size:
                        if board[m][n + i + 1] == self.stone or board[m][n + i + 1] == self.fire:
                            break
                        elif board[m][n + i + 1] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(board[m][n + i + 1])
                            # print(turn)
                            fired = True
                            board[m][n + i + 1] = self.fire
                            self.is_dead += 1
                            self.score_p2 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
            elif direction == self.down_2:
                for i in range(self.size):
                    if n - i - 1 >= 0:
                        if board[m][n - i - 1] == self.stone or board[m][n - i - 1] == self.fire:
                            break
                        elif board[m][n - i - 1] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            # print(board[m][n - i - 1])
                            fired = True
                            board[m][n - i - 1] = self.fire
                            self.is_dead += 1
                            self.score_p2 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
            elif direction == self.right_2:
                for i in range(self.size):
                    if m + i + 1 < self.size:
                        if board[m + i + 1][n] == self.stone or board[m + i + 1][n] == self.fire:
                            break
                        elif board[m + i + 1][n] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            # print(board[m + i + 1][n])
                            fired = True
                            board[m + i + 1][n] = self.fire
                            self.is_dead += 1
                            self.score_p2 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
            elif direction == self.left_2:
                for i in range(self.size):
                    if m - i - 1 >= 0:
                        if board[m - i - 1][n] == self.stone or board[m - i - 1][n] == self.fire:
                            # print()
                            # print('Reached...')
                            break
                        elif board[m - i - 1][n] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            print(board[m - i - 1][n])
                            fired = True
                            board[m - i - 1][n] = self.fire
                            self.is_dead += 1
                            self.score_p2 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
        elif turn == 3:
            if direction == self.up_3:
                for i in range(self.size):
                    if n + i + 1 < self.size:
                        if board[m][n + i + 1] == self.stone or board[m][n + i + 1] == self.fire:
                            break
                        elif board[m][n + i + 1] == 0:
                            break
                        else:
                            # print('fired...')
                            # print(turn)
                            # print(board[m][n + i + 1])
                            fired = True
                            board[m][n + i + 1] = self.fire
                            self.is_dead += 1
                            self.score_p3 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
            elif direction == self.down_3:
                for i in range(self.size):
                    if n - i - 1 >= 0:
                        if board[m][n - i - 1] == self.stone or board[m][n - i - 1] == self.fire:
                            break
                        elif board[m][n - i - 1] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            fired = True
                            board[m][n - i - 1] = self.fire
                            self.is_dead += 1
                            self.score_p3 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
            elif direction == self.right_3:
                for i in range(self.size):
                    if m + i + 1 < self.size:
                        if board[m + i + 1][n] == self.stone or board[m + i + 1][n] == self.fire:
                            break
                        elif board[m + i + 1][n] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            # print(board[m + i + 1][n])
                            fired = True
                            board[m + i + 1][n] = self.fire
                            self.is_dead += 1
                            self.score_p3 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
            elif direction == self.left_3:
                for i in range(self.size):
                    if m - i - 1 >= 0:
                        if board[m - i - 1][n] == self.stone or board[m - i - 1][n] == self.fire:
                            break
                        elif board[m - i - 1][n] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            fired = True
                            board[m - i - 1][n] = self.fire
                            self.is_dead += 1
                            self.score_p3 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
        elif turn == 4:
            if direction == self.up_4:
                for i in range(self.size):
                    if n + i + 1 < self.size:
                        if board[m][n + i + 1] == self.stone or board[m][n + i + 1] == self.fire:
                            break
                        elif board[m][n + i + 1] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            fired = True
                            board[m][n + i + 1] = self.fire
                            self.is_dead += 1
                            self.score_p4 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
            elif direction == self.down_4:
                for i in range(self.size):
                    if n - i - 1 >= 0:
                        if board[m][n - i - 1] == self.stone or board[m][n - i - 1] == self.fire:
                            break
                        elif board[m][n - i - 1] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            fired = True
                            board[m][n - i - 1] = self.fire
                            self.is_dead += 1
                            self.score_p4 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
            elif direction == self.right_4:
                for i in range(self.size):
                    if m + i + 1 < self.size:
                        if board[m + i + 1][n] == self.stone or board[m + i + 1][n] == self.fire:
                            break
                        elif board[m + i + 1][n] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            fired = True
                            board[m + i + 1][n] = self.fire
                            self.is_dead += 1
                            self.score_p4 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break
            elif direction == self.left_4:
                for i in range(self.size):
                    if m - i - 1 >= 0:
                        if board[m - i - 1][n] == self.stone or board[m - i - 1][n] == self.fire:
                            break
                        elif board[m - i - 1][n] == 0:
                            continue
                        else:
                            # print('fired...')
                            # print(turn)
                            fired = True
                            board[m - i - 1][n] = self.fire
                            self.is_dead += 1
                            self.score_p4 += self.tank_destroying_score
                            list.append(board)
                            break
                    else:
                        break

        if fired == True:
            return list

        i, j = self.get_current_pos(board, turn)

        # board = self.make_fire(board, turn)
        # print(board)
        # if board != None:
        #     list.append(board)

        if j + 1 < self.size:
            if copy1[i][j + 1] is 0:
                copy1[i][j] = 0
                copy1[i][j + 1] = direction
                list.append(copy1)

        i, j = self.get_current_pos(board, turn)
        if j - 1 >= 0:
            if copy2[i][j - 1] is 0:
                copy2[i][j] = 0
                copy2[i][j - 1] = direction
                list.append(copy2)

        i, j = self.get_current_pos(board, turn)
        if i + 1 < self.size:
            if copy3[i + 1][j] is 0:
                copy3[i][j] = 0
                copy3[i + 1][j] = direction
                list.append(copy3)

        i, j = self.get_current_pos(board, turn)
        if i - 1 >= 0:
            if copy4[i - 1][j] is 0:
                copy4[i][j] = 0
                copy4[i - 1][j] = direction
                list.append(copy4)

        # # childern for direction
        i, j = self.get_current_pos(board, turn)
        child_1, child_2 = self.get_childern__by_direction(direction, turn)
        copy5[i][j] = child_1
        copy6[i][j] = child_2
        list.append(copy5)
        list.append(copy6)

        return list

    def get_childern__by_direction(self, direction, turn):
        if direction is turn * 10 + 1 or direction is turn * 10 + 3:
            return turn * 10 + 2, turn * 10 + 4
        elif direction is turn * 10 + 2 or direction is turn * 10 + 4:
            return turn * 10 + 1, turn * 10 + 3

    def get_current_pos(self, board, turn):
        for i in range(self.size):
            for j in range(self.size):
                if (board[i][j] is turn * 10 + 1) or (board[i][j] is turn * 10 + 2) or (
                        board[i][j] is turn * 10 + 3) or (board[i][j] is turn * 10 + 4):
                    return i, j
        else:
            return -1, -1

    def get_current_direction(self, board, turn):
        i, j = self.get_current_pos(board, turn)
        if i == -1 and j == -1:
            return -1
        else:
            direction = board[i][j]
            return direction

    def make_move(self, board, turn):
        return random.choice(self.generate_childern(board, turn))


    #returns matrix of size a, b
    def generate_matrix(self, a, b):
        list = []
        for i in range(a):
            list.append([])
            for j in range(b):
                list[i].append(random.randint(-10, 10))

        return list

    def generate_1D(self, matrix):
        output = []
        for index, data in enumerate(matrix):
            for j in range(len(data)):
                output.append(matrix[index][j])

        return output

def main():
    """ Main method """
    game = Tanks(650, 650, "Tanks")
    game.setup()
    arcade.run()


main()
