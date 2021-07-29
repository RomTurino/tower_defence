import random
import time
import math
import arcade

# задаем ширину, высоту и заголовок окна

SCREEN_TITLE = "Tower Defence"
CELL_WIDTH = 40
CELL_HEIGHT = 40
ROW_COUNT = 20
COLUMN_COUNT = 13
SCREEN_WIDTH = CELL_WIDTH * ROW_COUNT
SCREEN_HEIGHT = CELL_HEIGHT * COLUMN_COUNT
MONSTERS_ON_STAGE = 5
FACTOR = 2 #множитель, влияющий на сложность - чем он больше, тем больше будет уровней и больше будет жизней у врагов
WAVES = FACTOR * 5 #общее количество волн


def difference(arg, par): #центр ячейки
    return arg * par + par / 2


def justify_x(position_x): #выравнивание по центру для координаты х
    for x in range(ROW_COUNT):
        x = difference(x, CELL_WIDTH)
        if position_x - x <= 30:
            center_x = x
            return center_x


def justify_y(position_y):#выравнивание по центру для координаты у
    for y in range(COLUMN_COUNT):
        y = difference(y, CELL_HEIGHT)
        if position_y - y <= 30:
            center_y = y
            return center_y


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

]#список для отрисовки дороги. 1- есть дорога, 0 - нет


class Monsters(arcade.AnimatedTimeSprite):
    def __init__(self):
        super().__init__(0.4)
        self.step = 1  # шаг движения
        self.speed = 1 # скорость
        self.lives = 1 # жизни
        self.cost = 50 # сколько монет дает после убийства
        self.speed_and_lives()
        self.texture_choice()
        self.center_x = difference(-1, CELL_WIDTH) + CELL_WIDTH / 4
        self.center_y = difference(random.uniform(1, 2), CELL_HEIGHT) + CELL_HEIGHT / 4

    def texture_choice(self):
        self.textures_list = []

        # demon
        self.demon_walk = []
        for i in range(1, 7):
            self.demon_walk.append(arcade.load_texture(f'demon/walk/Walk{i}.png'))
        self.demon_death = []
        for i in range(1, 7):
            self.demon_death.append(arcade.load_texture(f'demon/death/Death{i}.png'))
        self.textures_list.append(self.demon_walk)

        # jinn
        self.jinn_walk = []
        for i in range(1, 5):
            self.jinn_walk.append(arcade.load_texture(f'jinn/walk/Flight{i}.png'))
        self.jinn_death = []
        for i in range(1, 7):
            self.jinn_death.append(arcade.load_texture(f'jinn/death/Death{i}.png'))
        self.textures_list.append(self.jinn_walk)

        # lizard
        self.lizard_walk = []
        for i in range(1, 7):
            self.lizard_walk.append(arcade.load_texture(f'lizard/walk/Walk{i}.png'))
        self.lizard_death = []
        for i in range(1, 7):
            self.lizard_death.append(arcade.load_texture(f'lizard/death/Death{i}.png'))
        self.textures_list.append(self.lizard_walk)

        # medusa
        self.medusa_walk = []
        for i in range(1, 5):
            self.medusa_walk.append(arcade.load_texture(f'medusa/walk/Walk{i}.png'))
        self.medusa_death = []
        for i in range(1, 7):
            self.medusa_death.append(arcade.load_texture(f'medusa/death/Death{i}.png'))

        # dragon
        self.dragon_walk = []
        for i in range(1, 6):
            self.dragon_walk.append(arcade.load_texture(f'dragon/walk/Walk{i}.png'))
        self.dragon_death = []
        for i in range(1, 6):
            self.dragon_death.append(arcade.load_texture(f'dragon/death/Death{i}.png'))
        self.textures_list.append(self.dragon_walk)

        self.textures_list.append(self.demon_walk)
        self.textures = self.textures_list[(window.wave - 1) // FACTOR]
        self.texture = self.textures[0]

    def speed_and_lives(self):
        if window.wave < FACTOR:
            self.speed = 1
            self.lives = FACTOR
        elif window.wave < FACTOR * 2:
            self.speed = 1.5
            self.lives = FACTOR * 2
        elif window.wave < FACTOR * 3:
            self.speed = 2
            self.lives = FACTOR * 3
        elif window.wave < FACTOR * 4:
            self.speed = 2.5
            self.lives = FACTOR * 4
        elif window.wave < FACTOR * 5:
            self.speed = 3
            self.lives = FACTOR * 5

    def update(self):
        self.center_y += self.change_y
        self.center_x += self.change_x
        self.movement()
        if self.right > SCREEN_WIDTH:
            self.kill()
            window.fails += 1
        if self.lives <= 0:
            self.kill()
            window.money += self.cost
            print(window.money)

    def go_left(self, steps):
        limit_x = difference(steps, CELL_WIDTH)
        self.change_x = self.speed
        if self.center_x > limit_x:
            self.center_x = limit_x
            self.change_x = 0
            self.step += 1

    def go_up(self, steps):
        limit_y = difference(steps, CELL_HEIGHT)
        self.change_y = self.speed
        if self.center_y > limit_y:
            self.change_y = limit_y
            self.change_y = 0
            self.step += 1

    def go_down(self, steps):
        limit_y = difference(steps, CELL_HEIGHT)

        self.change_y = -self.speed
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
            self.go_left(14)
        if self.step == 6:
            self.go_up(9)
        if self.step == 7:
            self.go_left(21)


class Bullet(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        hitlist = arcade.check_for_collision_with_list(self, window.monsters)
        if len(hitlist) > 0:
            self.kill()
            for monster in hitlist:
                monster.lives -= 1


class Gun(arcade.AnimatedTimeSprite):
    reload = None

    def __init__(self):
        super().__init__(1)
        self.bullet_spawn = time.time()

    def rotate(self, x, y):
        self.x_diff = x - self.center_x
        self.y_diff = y - self.center_y
        target_angle_radians = math.atan2(self.y_diff, self.x_diff)
        '''actual_angle_radians = math.radians(self.angle - 90)

        rot_speed_radians = target_angle_radians - actual_angle_radians
        if actual_angle_radians != target_angle_radians:
            actual_angle_radians+=5
        if actual_angle_radians > 2 * math.pi:
            actual_angle_radians -= 2 * math.pi
        elif actual_angle_radians < 0:
            actual_angle_radians += 2 * math.pi'''
        self.angle = math.degrees(target_angle_radians)

    def update(self):
        for monster in window.monsters:
            if abs(monster.center_x - self.center_x) < CELL_WIDTH * 3:
                if abs(monster.center_y - self.center_y) < CELL_HEIGHT * 3:
                    self.rotate(monster.center_x, monster.center_y)
                    if isinstance(self, SimpleGun):
                        bul = Bullet('Bullets/simple_bul.png', 0.1)
                        self.reload = 1
                        self.power = 1
                    if isinstance(self, MashineGun):
                        bul = Bullet('Bullets/mashine_bul.png', 0.5)
                        self.reload = 0.5
                        self.power = 1
                    if isinstance(self, Crusher):
                        bul = Bullet('Bullets/crusher_bul.png', 1)
                        self.reload = 3
                        self.power = 2
                    if isinstance(self, Annihilator):
                        bul = Bullet('Bullets/laser_annihilation.png', 2)
                        self.reload = 4
                        self.power = window.wave
                    if time.time() - self.bullet_spawn > self.reload:
                        bul.center_y = self.center_y
                        bul.center_x = self.center_x
                        bul.angle = self.angle
                        bul.forward(10)
                        window.bullets.append(bul)
                        self.bullet_spawn = time.time()
                    if arcade.check_for_collision(monster, bul):

                        bul.kill()
                        monster.lives -= self.power



class SimpleGun(Gun):
    def __init__(self):
        super().__init__()
        for i in range(2):
            self.textures.append(arcade.load_texture('guns/simple_gun.png'))
        self.texture = self.textures[0]
        self.cost = 100


class MashineGun(Gun):
    def __init__(self):
        super().__init__()
        for i in range(2):
            self.textures.append(arcade.load_texture('guns/mashine_gun.png'))
        self.texture = self.textures[0]
        self.bullet_spawn = time.time()
        self.cost = 500


class Crusher(Gun):
    def __init__(self):
        super().__init__()
        for i in range(2):
            self.textures.append(arcade.load_texture('guns/laser.png'))
        self.texture = self.textures[0]
        self.bullet_spawn = time.time()
        self.cost = 1000


class Annihilator(Gun):
    def __init__(self):
        super().__init__()
        for i in range(1, 5):
            self.textures.append(arcade.load_texture(f'guns/annihilator{i}.png'))
        self.texture = self.textures[0]
        self.bullet_spawn = time.time()
        self.cost = 3000


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # текстуры
        self.bg = arcade.load_texture('Blocks/grass.png')
        self.menu = arcade.load_texture('menu/tower_menu.png')
        self.win = arcade.load_texture('endgame/win.png')
        self.lost = arcade.load_texture('endgame/lost.png')

        # SpriteList
        self.road = arcade.SpriteList()
        self.monsters = arcade.SpriteList()
        self.guns = arcade.SpriteList()
        self.bullets = arcade.SpriteList()

        # Спрайты
        self.activ_hand = None

        # Списки
        self.sand_coords = []
        self.tower_coords = []

        # Время появления
        self.monster_spawn = time.time()
        self.wave_spawn = time.time()

        # переменные для управления игрой
        self.wave = 5
        self.monster_counter = 0
        self.fails = 0
        self.money = 100
        self.wave_start = True

    def setup(self):
        for x, row in enumerate(area_life):
            for y, cell in enumerate(row):
                if cell == 1:
                    sand = arcade.Sprite('blocks/sand.png', 0.1)
                    sand.center_x = difference(x, CELL_WIDTH)
                    sand.center_y = difference(y, CELL_HEIGHT)
                    self.road.append(sand)
                    self.sand_coords.append((sand.center_x, sand.center_y))

    def on_draw(self):
        arcade.start_render()
        for x in range(ROW_COUNT):
            for y in range(COLUMN_COUNT):
                arcade.draw_texture_rectangle(difference(x, CELL_WIDTH), difference(y, CELL_HEIGHT), CELL_WIDTH,
                                              CELL_HEIGHT, self.bg)
        arcade.draw_texture_rectangle(center_x=SCREEN_WIDTH / 2,
                                      center_y=SCREEN_HEIGHT - CELL_HEIGHT * 2,
                                      width=SCREEN_WIDTH,
                                      height=SCREEN_HEIGHT - CELL_HEIGHT * 2,
                                      texture=self.menu)
        self.road.draw()
        self.monsters.draw()
        self.guns.draw()
        self.bullets.draw()
        if self.activ_hand != None:
            self.activ_hand.draw()

        arcade.draw_text(f'{self.wave}/{WAVES}', 545, 486, (196, 226, 22), 9)
        arcade.draw_text(f'{self.fails}/20', 545, 453, (196, 226, 22), 9)
        arcade.draw_text(f'{self.money}', 50, SCREEN_HEIGHT - 68, (196, 226, 22), 15)
        if self.wave == WAVES and len(self.monsters) == 0:
            arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                                          SCREEN_WIDTH, SCREEN_HEIGHT, self.win)
        if self.fails >=20:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                          SCREEN_WIDTH, SCREEN_HEIGHT, self.lost)
    def update(self, delta_time):
        self.monsters.update()
        self.monsters.update_animation()
        self.guns.update()
        self.guns.update_animation()
        self.bullets.update()
        if self.monster_counter < MONSTERS_ON_STAGE * self.wave:
            self.monster_attacks()
        if self.monster_counter == MONSTERS_ON_STAGE * self.wave:
            if len(self.monsters) == 0 and self.wave_start:
                self.wave_spawn = time.time()
                self.wave_start = False
        if time.time() - self.wave_spawn > 10 and self.wave_start == False:
            self.wave += 1
            print('level plus')
            self.wave_start = True
            self.monster_counter = 0

    def monster_attacks(self):
        for i in range(self.wave * MONSTERS_ON_STAGE):
            if time.time() - self.monster_spawn > MONSTERS_ON_STAGE / self.wave:
                demon = Monsters()
                self.monsters.append(demon)
                self.monster_spawn = time.time()
                self.monster_counter += 1
                print(f'counter = {self.monster_counter}')

    def on_key_press(self, key: int, modifiers: int):
        pass

    def on_key_release(self, key: int, modifiers: int):
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if y > CELL_HEIGHT * (COLUMN_COUNT - 2):
            if x < CELL_WIDTH * 3:
                pass
            elif CELL_WIDTH * 3 < x < CELL_WIDTH * 5 + CELL_WIDTH / 2:
                print('gun')
                self.activ_hand = SimpleGun()

            elif x < CELL_WIDTH * 7 + CELL_WIDTH / 2:
                print('mashine gun')
                self.activ_hand = MashineGun()

            elif x < CELL_WIDTH * 9 + CELL_WIDTH:
                print('laser')
                self.activ_hand = Crusher()
            elif x < CELL_WIDTH * 12 + CELL_WIDTH / 2:
                print('annihilator')
                self.activ_hand = Annihilator()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if self.activ_hand != None :
            self.activ_hand.center_y = y
            self.activ_hand.center_x = x

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        if self.activ_hand != None and y < CELL_HEIGHT * (COLUMN_COUNT - 2) and self.activ_hand.cost<=self.money:
            self.activ_hand.center_x = justify_x(x)
            self.activ_hand.center_y = justify_y(y)
            if (self.activ_hand.center_x, self.activ_hand.center_y) not in self.sand_coords and\
                    (self.activ_hand.center_x, self.activ_hand.center_y) not in self.tower_coords:
                self.guns.append(self.activ_hand)
                self.money-=self.activ_hand.cost
                self.tower_coords.append((self.activ_hand.center_x, self.activ_hand.center_y))
                self.activ_hand = None
        elif self.activ_hand != None and y > CELL_HEIGHT * (COLUMN_COUNT - 2):
            self.activ_hand = None


window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
