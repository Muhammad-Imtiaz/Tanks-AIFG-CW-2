import arcade
import math
import sys

class Tanks(arcade.Window):
    size = 15
    turn = 1
    grid = []

    up_1 = 11
    down_1 = 12
    left_1 = 13
    right_1 = 14

    up_2 = 21
    down_2 = 22
    left_2 = 23
    right_2 = 24

    up_3 = 31
    down_3 = 32
    left_3 = 33
    right_3 = 34

    up_4 = 41
    down_4 = 42
    left_4 = 43
    right_4 = 44
    SPRITE_SCALING_PLAYER = 0.2
    stone = 100

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.width = width
        self.height = height
        self.player_sprite = None
        self.sprite_list = None

        arcade.set_background_color(arcade.color.AMAZON)
        self.initialize_grid()

    def initialize_grid(self):
        for row in range(self.size):
            self.grid.append([])
            for column in range(self.size):
                self.grid[row].append(0)

        self.grid[0][0] = self.right_1
        self.grid[0][self.size - 1] = self.down_2
        self.grid[self.size - 1][0] = self.up_4
        self.grid[self.size - 1][self.size - 1] = self.left_4

        for i in range(3):
            self.grid[i][7] = self.stone
            self.grid[7][i] = self.stone
        i = 14
        while i>11:
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
                if self.grid[i][j] is self.right_1:
                    self.player_sprite = arcade.Sprite("1_right.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                elif self.grid[i][j] is self.left_1:
                    self.player_sprite = arcade.Sprite("1_left.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    # arcade.draw_circle_filled(i * bw + ri, j * bh + ci, bw / 4, arcade.color.AMAZON)
                elif self.grid[i][j] is self.up_1:
                    self.player_sprite = arcade.Sprite("1_up.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                elif self.grid[i][j] is self.down_1:
                    self.player_sprite = arcade.Sprite("1_down.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                elif self.grid[i][j] is self.right_2:
                    self.player_sprite = arcade.Sprite("2_right.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)


                elif self.grid[i][j] is self.left_2:
                    self.player_sprite = arcade.Sprite("2_left.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    # arcade.draw_circle_filled(i * bw + ri, j * bh + ci, bw / 4, arcade.color.AMAZON)
                elif self.grid[i][j] is self.up_2:
                    self.player_sprite = arcade.Sprite("2_up.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                elif self.grid[i][j] is self.down_2:
                    self.player_sprite = arcade.Sprite("2_down.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                elif self.grid[i][j] is self.right_3:
                    self.player_sprite = arcade.Sprite("3_right.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)


                elif self.grid[i][j] is self.left_3:
                    self.player_sprite = arcade.Sprite("3_left.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    # arcade.draw_circle_filled(i * bw + ri, j * bh + ci, bw / 4, arcade.color.AMAZON)
                elif self.grid[i][j] is self.up_3:
                    self.player_sprite = arcade.Sprite("3_up.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                elif self.grid[i][j] is self.down_3:
                    self.player_sprite = arcade.Sprite("3_down.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)

                elif self.grid[i][j] is self.right_4:
                    self.player_sprite = arcade.Sprite("4_right.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)


                elif self.grid[i][j] is self.left_4:
                    self.player_sprite = arcade.Sprite("4_left.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                    # arcade.draw_circle_filled(i * bw + ri, j * bh + ci, bw / 4, arcade.color.AMAZON)
                elif self.grid[i][j] is self.up_4:
                    self.player_sprite = arcade.Sprite("4_up.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                elif self.grid[i][j] is self.down_4:
                    self.player_sprite = arcade.Sprite("4_down.png", self.SPRITE_SCALING_PLAYER)
                    self.player_sprite.center_x = i * bw + ri
                    self.player_sprite.center_y = j * bh + ci
                    self.player_list.append(self.player_sprite)
                elif self.grid[i][j] is self.stone:
                    self.player_sprite = arcade.Sprite("stone.png", 0.022)
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
            turn = 2
        elif turn is 2:
            turn = 3
        elif turn is 3:
            turn = 4
        elif turn is 4:
            turn = 1
        return turn





def main():
    """ Main method """
    game = Tanks(650, 650, "Snails")
    game.setup()
    arcade.run()

main()



