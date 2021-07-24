import random

import arcade

# задаем ширину, высоту и заголовок окна

SCREEN_TITLE = "Tower Defence"
CELL_WIDTH = 60
CELL_HEIGHT = 60
ROW_COUNT = 20
COLUMN_COUNT = 11
SCREEN_WIDTH = CELL_WIDTH * ROW_COUNT
SCREEN_HEIGHT = CELL_HEIGHT * COLUMN_COUNT


def difference(arg, par):
    return arg * par + par / 2


area_life = [
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]

]


class Monsters(arcade.AnimatedTimeSprite):
    def __init__(self):
        super().__init__(0.6)
        for i in range(1, 7):
            self.textures.append(arcade.load_texture(f'demon/walk/Walk{i}.png'))
        self.texture = self.textures[0]
        self.step = 1


    def update(self):
        self.center_y += self.change_y
        self.center_x += self.change_x
        self.movement()

    def go_left(self, steps):
        limit_x = difference(steps, CELL_WIDTH)
        self.change_x = 3
        if self.center_x > limit_x:
            self.center_x = limit_x
            self.change_x = 0
            self.step += 1
    def go_up(self, steps):
        limit_y = difference(steps, CELL_HEIGHT)
        self.change_y = 3
        if self.center_y > limit_y:
            self.change_y = limit_y
            self.change_y = 0
            self.step += 1
    def go_down(self, steps):
        limit_y = difference(steps, CELL_HEIGHT)
        print(limit_y)
        self.change_y = -3
        if self.center_y < limit_y:
            self.change_y = limit_y
            self.change_y = 0
            self.step += 1

    def movement(self):
        if self.step == 1:
            self.go_left(3)
        if self.step == 2:
            self.go_up(9)
        if self.step == 3:
            self.go_left(10)
        if self.step == 4:
            self.go_down(2)
        if self.step == 5:
            self.go_left(12)
        if self.step == 6:
            self.go_up(9)
        if self.step == 7:
            self.go_left(21)

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # текстуры
        self.bg = arcade.load_texture('Blocks/grass.png')

        # SpriteList
        self.road = arcade.SpriteList()
        self.monsters = arcade.SpriteList()

    def setup(self):
        for x, row in enumerate(area_life):
            for y, cell in enumerate(row):
                if cell == 1:
                    sand = arcade.Sprite('blocks/sand.png', 0.15)
                    sand.center_x = difference(x, CELL_WIDTH)
                    sand.center_y = difference(y, CELL_HEIGHT)
                    self.road.append(sand)
        demon = Monsters()
        demon.center_x = 50
        demon.center_y = random.randint(100, 160)
        self.monsters.append(demon)

    def on_draw(self):
        arcade.start_render()
        for x in range(ROW_COUNT):
            for y in range(COLUMN_COUNT):
                arcade.draw_texture_rectangle(difference(x, CELL_WIDTH), difference(y, CELL_HEIGHT), CELL_WIDTH,
                                              CELL_HEIGHT, self.bg)
        self.road.draw()
        self.monsters.draw()

    def update(self, delta_time):
        self.monsters.update()
        self.monsters.update_animation()

    def on_key_press(self, key: int, modifiers: int):
        pass

    def on_key_release(self, key: int, modifiers: int):
        pass


window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
