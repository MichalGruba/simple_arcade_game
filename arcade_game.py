#Arcade Game
#Authors
#Kacper Plesiak
#Michał Gruba

import pygame
from pygame.locals import *
import numpy as np
from PIL import Image


class Sprite:
    def __init__(self):
        print(".")
    def prepare_sprite(self, x, y, path):
        self.img = pygame.image.load(path).convert_alpha()
        self.hitbox = self.img.get_rect()
        self.hitbox.x = x
        self.hitbox.y = y
        self.centerx = self.img.get_rect().center[0] + self.hitbox.x
        self.centery = self.img.get_rect().center[1] + self.hitbox.y
        self.size =  self.img.get_size()


class Player(Sprite):
    def __init__(self, startx, starty):
        self.startx = startx
        self.starty = starty
        self.go = True
    def control(self, data):
        global lvl
        keys = pygame.key.get_pressed()                # player control
        left_upc = [self.hitbox.x, self.hitbox.y]      # calculating player's corners coords
        right_upc = [self.centerx + int(self.size[1] / 2) - 1, self.centery - int(self.size[0] / 2)]
        left_downc = [self.centerx - int(self.size[1] / 2), self.centery + int(self.size[0] / 2) - 1]
        right_downc = [self.centerx + int(self.size[1] / 2) - 1, self.centery + int(self.size[0] / 2) - 1]

        # data[x, y]
        if unequality((data[right_upc[0] + 1, right_upc[1]]), wall_colour) and unequality((data[right_downc[0] + 1, right_downc[1]]), wall_colour) and player.go == True:
            self.centerx += keys[pygame.K_RIGHT]
            self.hitbox.x += keys[pygame.K_RIGHT]
        if unequality((data[left_upc[0] - 1, left_upc[1]]), wall_colour) and unequality((data[left_downc[0] - 1, left_downc[1]]), wall_colour) and player.go == True:
            self.centerx -= keys[pygame.K_LEFT]
            self.hitbox.x -= keys[pygame.K_LEFT]
        if unequality((data[left_downc[0], left_downc[1] + 1]), wall_colour) and unequality((data[right_downc[0], right_downc[1] + 1]), wall_colour) and player.go == True:
            self.centery += keys[pygame.K_DOWN]
            self.hitbox.y += keys[pygame.K_DOWN]
        if unequality((data[right_upc[0], right_upc[1] - 1]), wall_colour) and unequality((data[left_upc[0], left_upc[1] - 1]), wall_colour) and player.go == True:
            self.centery -= keys[pygame.K_UP]
            self.hitbox.y -= keys[pygame.K_UP]

        if not unequality((data[right_upc[0], right_upc[1]]), win_area_colour):
            print("WIN")
            lvl += 1
            load_level(lvl)
        elif not unequality((data[left_upc[0], left_upc[1]]), win_area_colour):
            print("WIN")
            lvl += 1
            load_level(lvl)
        elif not unequality((data[left_downc[0], left_downc[1]]), win_area_colour):
            print("WIN")
            lvl += 1
            load_level(lvl)
        elif not unequality((data[right_downc[0], right_downc[1]]), win_area_colour):
            print("WIN")
            lvl += 1
            load_level(lvl)
        elif not unequality((data[right_upc[0], right_upc[1]]), orange):
            self.update_start_pos(checkpoint_pos[0], checkpoint_pos[1])
        elif not unequality((data[left_upc[0], left_upc[1]]), orange):
            self.update_start_pos(checkpoint_pos[0], checkpoint_pos[1])
        elif not unequality((data[left_downc[0], left_downc[1]]), orange):
            self.update_start_pos(checkpoint_pos[0], checkpoint_pos[1])
        elif not unequality((data[right_downc[0], right_downc[1]]), orange):
            self.update_start_pos(checkpoint_pos[0], checkpoint_pos[1])
    def update_start_pos(self, x, y):
        print("CHECKPOINT")
        self.startx = x
        self.starty = y


class Coin(Sprite):
    def __init__(self):
        self.collected = False
    def __del__(self):
        print("deleted")


class Key(Sprite):
    def __init__(self):
        self.collected = False


class Doors(Sprite):
    def __init__(self):
        self.open = False


class Replay(Sprite):
    def __init__(self):
        self.datax = []
        self.datay = []
        self.datax2 = []
        self.datay2 = []
        self.isplay = False
    def play(self, frame, deaths):
        if deaths % 2 == 1:
            if self.datax.__len__() != frame:
                window.blit(self.img, (self.datax[frame], self.datay[frame]))
            else:
                self.isplay = False
        elif deaths == 0 or deaths % 2 == 0:
            if self.datax2.__len__() != frame:
                window.blit(self.img, (self.datax2[frame], self.datay2[frame]))
            else:
                self.isplay = False


class Path():
    def __init__(self, enemy, waypoints, type='reverse'):
        self.path = []
        self.waypoint = 0
        self.type = type
        self.reverse = False

        for i in range(waypoints.__len__()):
            waypoints[i][0] += enemy.hitbox.x
            waypoints[i][1] += enemy.hitbox.y
            self.path.append(waypoints[i])
        if self.type == 'repeat':
            self.path.append([enemy.hitbox.x, enemy.hitbox.y])
    def update(self, enemy):

        if enemy.hitbox.x < self.path[self.waypoint][0]:
            enemy.hitbox.x += 1
        elif enemy.hitbox.x > self.path[self.waypoint][0]:
            enemy.hitbox.x -= 1
        if enemy.hitbox.y < self.path[self.waypoint][1]:
            enemy.hitbox.y += 1
        elif enemy.hitbox.y > self.path[self.waypoint][1]:
            enemy.hitbox.y -= 1
        if enemy.hitbox.x == self.path[self.waypoint][0] and enemy.hitbox.y == self.path[self.waypoint][1]:
            if self.waypoint == self.path.__len__()-1:
                if self.type == 'reverse':
                    self.reverse = True
                else:
                    self.waypoint = 0
            elif self.waypoint == 0:
                self.reverse = False
            if self.reverse == False:
                self.waypoint += 1
            else:
                self.waypoint -= 1


def add_enemy(enemies, enemy_hitbox, x, y):
    global n_enemies
    enemy = Sprite()
    enemy.prepare_sprite(x, y, "image\enemy.png")
    enemies.append(enemy)
    enemy_hitbox.append(enemy.hitbox)
    n_enemies += 1


def add_coin(coins, coin_hitbox, x, y):
    global n_coins
    coin = Coin()
    coin.prepare_sprite(x, y, "image\coin.png")
    coins.append(coin)
    coin_hitbox.append(coin.hitbox)
    n_coins += 1


def unequality (a, b):
    for i in range(b.__len__()):
        if  a[i] != b[i]:
            return True
    return False


def update_window():
    global frame
    window.blit(level, (0, 0))
    for i in range(n_coins): # coins drawing
        window.blit(coins[i].img, (coins[i].hitbox.x, coins[i].hitbox.y))
    for i in range(n_enemies): # enemies drawing
        window.blit(enemies[i].img, (enemies[i].hitbox.x, enemies[i].hitbox.y))
    for i in range(paths.__len__()): # path updating
        paths[i].update(enemies[i])
    if key[0].collected == False:
        window.blit(key[0].img, (key[0].hitbox.x, key[0].hitbox.y))
    if doors[0].open == False:
        window.blit(doors[0].img, (doors[0].hitbox.x, doors[0].hitbox.y))
    if replay.isplay:
        replay.play(frame, deaths)
        frame += 1
    else:
        frame = 0
    window.blit(player.img, (player.hitbox.x, player.hitbox.y))
    if final_lvl_window == False:
        for i in range(textsurface.__len__()):
            window.blit(textsurface[i], (10+i*200, 0))
    pygame.display.flip()


def load_level(lvl, loadtype = 'next level'):
    global data, level, checkpoint_pos
    if(lvl == 0):
        level_np = Image.open('image\level2.png')
        data = np.transpose(np.asarray(level_np), axes=(1, 0, 2))
        level = pygame.image.load("image\level2.png").convert()
        player_start_coords = [100, 300]
        checkpoint_pos = [900, 400]
        enemy_start_pos = [(200, 40),
                           (200, 320),
                           (520, 40),
                           (520, 640),
                           (900, 540)]
        lvl_paths = [[[0, 0], [0, 280], [320, 280], [320, 0]],
                     [[0, 0], [0, 320], [320, 320], [320, 0]],
                     [[0, 0], [0, 600], [240, 600], [240, 0]],
                     [[0, 0], [0, -600]],
                     [[0, 0], [0, 48], [48, 48], [48, 0]]]
        path_types = ['repeat','repeat','repeat','reverse','repeat']
        coin_start_coords = [(700, 40),
                             (200, 320),
                             (520, 40),
                             (520, 640),
                             (924, 640)]
        keys = [(520, 320)]
        doors = [(800, 324)]

        if loadtype == 'next level':
            delete_objects()
            create_level(player_start_coords, enemy_start_pos, lvl_paths, path_types, coin_start_coords, keys, doors)
        elif loadtype == 'reset':
            reset_lvl()
            create_enemies(enemy_start_pos)
            create_paths(lvl_paths, path_types)
    elif(lvl == 1):
        if loadtype == 'next level':
            summary_window()
        level_np = Image.open('image\level3.png')
        data = np.transpose(np.asarray(level_np), axes=(1, 0, 2))
        level = pygame.image.load("image\level3.png").convert()
        player_start_coords = [110, 90]
        checkpoint_pos = [485, 370]
        enemy_start_pos = [(190, 170),
                           (30, 430),
                           (250, 470),
                           (655, 220),
                           (755, 115),
                           (350, 520),
                           (605, 520)]
        lvl_paths = [[[0, 0], [0, 48], [48, 48], [48, 0]],
                     [[0, 0], [220, 0]],
                     [[0, 0], [-220, 0]],
                     [[0, 0], [48, 0], [48, 48], [0, 48], [0, 0]],
                     [[0, 0], [56, 0], [56, 56]],
                     [[0, 0], [0, 120], [180, 120]],
                     [[0, 0], [0, 120], [-180, 120]]]
        path_types = ['repeat', 'reverse', 'repeat', 'repeat', 'reverse', 'reverse', 'reverse']
        coin_start_coords = [(30, 470),
                             (524, 640),
                             (424, 640)]
        keys = [(840, 80)]
        doors = [(700, 440)]
        if loadtype == 'next level':
            delete_objects()
            create_level(player_start_coords, enemy_start_pos, lvl_paths, path_types, coin_start_coords, keys, doors)
        elif loadtype == 'reset':
            reset_lvl()
            create_enemies(enemy_start_pos)
            create_paths(lvl_paths, path_types)
    elif(lvl == 2):
        if loadtype == 'next level':
            summary_window()
        level_np = Image.open('image\level4.png')
        data = np.transpose(np.asarray(level_np), axes=(1, 0, 2))
        level = pygame.image.load("image\level4.png").convert()
        player_start_coords = [810, 40]
        checkpoint_pos = [190, 90]
        enemy_start_pos = [(570, 40),
                           (570, 230),
                           (825, 640),
                           (100, 40),
                           (100, 230),
                           (360, 640)]
        lvl_paths = [[[0, 0], [0, 190], [250, 190]],
                     [[0, 0], [0, 190], [250, 190], [250, 0]],
                     [[0, 0], [0, -180], [-260, -180], [-260, 0]],
                     [[0, 0], [0, 190], [260, 190], [260, 0]],
                     [[0, 0], [0, 190], [250, 190], [250, 0]],
                     [[0, 0], [0, -180], [-260, -180], [-260, 0]]]
        path_types = ['reverse', 'repeat', 'repeat', 'repeat', 'repeat', 'repeat']
        coin_start_coords = [(230, 230),
                             (230, 440),
                             (230, 640),
                             (700, 230),
                             (700, 440),
                             (700, 640)]
        keys = [(110, 610)]
        doors = [(880, 310)]
        if loadtype == 'next level':
            delete_objects()
            create_level(player_start_coords, enemy_start_pos, lvl_paths, path_types, coin_start_coords, keys, doors)
        elif loadtype == 'reset':
            reset_lvl()
            create_enemies(enemy_start_pos)
            create_paths(lvl_paths, path_types)
    elif (lvl == 3):
        summary_window()


def summary_window():
    global textsurface, final_lvl_window
    final_lvl_window = True
    update_window()
    win_sound.play()
    textsurface = []
    textsurface.append(myfont.render("Score: " + str(int((coin_counter * 100 - 50 * deaths)/(0.1*time))), False, (0, 0, 0)))
    textsurface.append(myfont.render("Time: " + str("%.1f" % time), False, (0, 0, 0)))
    textsurface.append(myfont.render("Deaths: " + str(deaths), False, (0, 0, 0)))
    textsurface.append(myfont.render("PRESS C TO CONTINUE", False, (0, 0, 0)))

    for i in range(textsurface.__len__()-1):
        window.blit(textsurface[i], (10+i*200, 0))
    window.blit(textsurface[3], (300, 100))
    pygame.display.flip()
    wait()


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                pygame.sys.exit()
            if event.type == KEYDOWN and event.key == K_c:
                return


# some initial states
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
program_speed = 3
run = True
final_lvl_window = False

# graphics and audio
window = pygame.display.set_mode((1024, 720))
myfont = pygame.font.SysFont('Calibri', 30)
dead_sound = pygame.mixer.Sound("audio\dead.mp3")
coin_sound = pygame.mixer.Sound("audio\mario_coin.wav")
coin_sound.set_volume(0.3)
key_sound = pygame.mixer.Sound("audio\mario_key.mp3")
door_sound = pygame.mixer.Sound("audio\door.mp3")
win_sound = pygame.mixer.Sound("audio\win.mp3")
win_sound.set_volume(0.3)


#defining colours RGB + alpha channel
black = np.array([0, 0, 0, 255])
yellow = np.array([255, 242, 0, 255])
red = np.array([237, 28, 36, 255])
green = np.array([34, 177, 76, 255])
orange = np.array([255, 127, 39, 255])

#control panel
wall_colour = black # defines which colour from the picture is interpreted as wall
win_area_colour = green # defines which colour from the picture is interpreted as win area
checkpoint_colour = orange # defines which color from the picture is interpreted as checkpoint

# replay
replay = Replay()
replay.prepare_sprite(0, 0, "image\player replay.png")
frame = 0


# some global variables
deaths = 0
lvl = 0
time = 0.

n_enemies = 0
enemies = []
enemy_hitbox = []

paths = []

n_coins = 0
coins = []
coin_hitbox = []
coin_counter = 0

key = []
key_hitbox = []

doors = []
doors_hitbox = []


def create_player(coords):
    global player
    player = Player(coords[0], coords[1])
    player.prepare_sprite(coords[0], coords[1], "image\player.png")
    player.update_start_pos(coords[0], coords[1])


def create_enemies(start_coords):
    for i in range(start_coords.__len__()):
        add_enemy(enemies, enemy_hitbox, start_coords[i][0], start_coords[i][1])


def create_paths(lvl_path, path_type):
    for i in range(lvl_path.__len__()):
        paths.append(Path(enemies[i], lvl_path[i], type=path_type[i]))


def create_coins(start_coords):
    for i in range(start_coords.__len__()):
        add_coin(coins, coin_hitbox, start_coords[i][0], start_coords[i][1])


def create_keys(start_coords):
    for i in range(start_coords.__len__()):
        key.append(Key())
        key[i].prepare_sprite(start_coords[i][0], start_coords[i][1], "image\key.png")
        key_hitbox.append(key[i].hitbox)


def create_doors(start_coords):
    for i in range(start_coords.__len__()):
        doors.append(Doors())
        doors[i].prepare_sprite(start_coords[i][0], start_coords[i][1], "image\doors.png")
        doors_hitbox.append(doors[i].hitbox)


def create_level(player_start_coords, enemy_start_pos, lvl_paths, path_types, coin_start_coords, keys, doors):
    create_player(player_start_coords)
    create_enemies(enemy_start_pos)
    create_paths(lvl_paths, path_types)
    create_coins(coin_start_coords)
    create_keys(keys)
    create_doors(doors)


def delete_objects():
    global deaths, n_enemies, enemies, enemy_hitbox, paths, n_coins, coins, coin_hitbox, coin_counter, frame, key, doors, doors_hitbox, key_hitbox, time, final_lvl_window
    final_lvl_window = False
    deaths = n_enemies = n_coins = coin_counter = frame = time = 0
    enemies = []
    enemy_hitbox = []
    paths = []
    coins = []
    coin_hitbox = []
    replay.datax = []
    replay.datay = []
    replay.datax2 = []
    replay.datay2 = []
    key =[]
    key_hitbox = []
    doors = []
    doors_hitbox = []


def reset_lvl():
    global enemies, enemy_hitbox, paths, frame, n_enemies
    n_enemies =  frame = 0
    enemies = []
    enemy_hitbox = []
    paths = []

# previous player coords
centerx = [0, 0]
centery = [0, 0]
hitboxx = [0, 0]
hitboxy = [0, 0]
load_level(0)
while run:  # MAIN
    clock.tick(60*program_speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            print(pygame.key.name(event.key))

    # control with player -> collision detections
    player.control(data)
    if (player.hitbox.collidelist(enemy_hitbox) != -1):  # with enemies
        player.hitbox.x = player.startx
        player.hitbox.y = player.starty
        player.centerx = player.img.get_rect().center[0] + player.hitbox.x
        player.centery = player.img.get_rect().center[1] + player.hitbox.y
        replay.isplay = True
        frame = 0
        deaths += 1
        if deaths == 0 or deaths % 2 == 0:
            replay.datax = []
            replay.datay = []
        elif deaths % 2 == 1:
            replay.datax2 = []
            replay.datay2 = []
        dead_sound.play()
        load_level(lvl, loadtype='reset')

    if (player.hitbox.collidelist(coin_hitbox) != -1): # with coins
        a = player.hitbox.collidelist(coin_hitbox)
        coins[a].collected = True
        coins[a].hitbox.x = -40
        coins[a].hitbox.y = -40
        coin_sound.play()
        coin_counter += 1
        print("MONETKA")

    # doors keys conditions
    centerx[0] = centerx[1]  # old x
    centerx[1] = player.centerx  # new x
    centery[0] = centery[1]
    centery[1] = player.centery
    hitboxx[0] = hitboxx[1]
    hitboxx[1] = player.hitbox.x
    hitboxy[0] = hitboxy[1]
    hitboxy[1] = player.hitbox.y
    if (player.hitbox.collidelist(key_hitbox) != -1):
        key_sound.play()
        key[0].hitbox.x = -60
        key[0].hitbox.y = -60
        key[0].collected = True
    #if (player.hitbox.collidelist(doors_hitbox) != -1) and key[0].collected == True:
        #doors[0].hitbox.x = -60
       # doors[0].hitbox.y = -60
       # door_sound.play()
        #doors[0].open = True
    player.go = True
    if (player.hitbox.collidelist(doors_hitbox) != -1) and key[0].collected == False:
        player.go = False

    if (player.hitbox.collidelist(doors_hitbox) != -1):
        a = player.hitbox.collidelist(doors_hitbox)
        if (key[a].collected):
            doors[a].open = True
            doors[a].hitbox.x = -30
            doors[a].hitbox.y = -30
            doors[a].centerx = -30
            doors[a].centery = -30
            door_sound.play()
        else:
            player.centerx = centerx[0]
            player.centery = centery[0]
            player.hitbox.x = hitboxx[0]
            player.hitbox.y = hitboxy[0]

    if deaths == 0 or deaths % 2 == 0: # data colecting to turn on replay
        replay.datax.append(player.hitbox.x)
        replay.datay.append(player.hitbox.y)
    elif deaths % 2 == 1:
        replay.datax2.append(player.hitbox.x)
        replay.datay2.append(player.hitbox.y)

    textsurface = []
    textsurface.append(myfont.render("Score: " + str(coin_counter*100), False, (0, 0, 0)))
    textsurface.append(myfont.render("Time: " + str("%.1f" % time), False, (0, 0, 0)))
    textsurface.append(myfont.render("Deaths: " + str(deaths), False, (0, 0, 0)))

    time += 1/(60*program_speed)
    update_window()

pygame.quit()
exit()
