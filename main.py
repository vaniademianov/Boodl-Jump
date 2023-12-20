from typing import Any
import pygame
import random
import serial as sm
import threading
import queue
import time
import os
import math
import pickle
import subprocess
from blocks.crafting_table import CraftingTable as crafting_table_item
from pathlib import Path
from res.resource_manager import resource_manager as rm

playerz = rm.get_players()
scope = rm.get_scope()
proc = None
try:
    serial = sm.Serial("COM6")
except Exception as e:
    proc = subprocess.Popen(["python", "sim.py"])
    time.sleep(1)
    serial = sm.Serial("COM9")
WIDTH = 1000
HEIGHT = 800
GUI_SENSA = 5
FPS = 30
INTERACTION_DISTANCE = 230
print_lock = threading.Lock()
inf_q = queue.Queue()
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BASE_HEIGHT = 200
_HEIGHT_MODIFIER = -200
lst = [(255, g, b) for g in range(0, 256, 8) for b in range(0, 256, 8)]
pygame.font.init() 
font_txt = pygame.font.SysFont('Comic Sans MS', 25)
COUNT_COLOR = (244, 230, 15)
class Informator(threading.Thread):
    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True

    def run(self):
        self.do_thing()

    def do_thing(self):
        while True:
            with print_lock:
                rl = serial.readline()
                sl = str(rl)
                if "\\n" in sl:
                    inf_q.put(str(rl, encoding="utf-8"))


def w(a: tuple, b: tuple):
    return (a[0] + b[0], a[1] + b[1])


def wm(a: tuple, b: tuple):
    return (a[0] - b[0], a[1] - b[1])


def wd(a: tuple, b: int):
    return (a[0] / b, a[1] / b)


def rect_group_collide(r: pygame.Rect, g: pygame.sprite.Group):
    for sprite in g.sprites():
        if r.colliderect(sprite.rect):
            return True
    return False


def the_one(a, b):
    return True in [a, b]




def i_fals(v):
    return v != None


class Slot:
    def __init__(self, item, act=False) -> None:
        self.item = item

        self.image_act = rm.get_active_slot().copy()
        self.image_unact = rm.get_unactive_slot().copy()
        self.og_image_act = rm.get_active_slot().copy()
        self.og_image_unact = rm.get_unactive_slot().copy()
        self.is_active = act
        self.count = 1
        # TODO blit name

        if item != None:
            rect: pygame.rect.Rect = item.minimized_for_inv.get_rect()
            rect.center = self.image_act.get_rect().center

            self.image_act.blit(item.minimized_for_inv, rect)
            self.image_unact.blit(item.minimized_for_inv, rect)
        else:
            self.image_act = self.og_image_act
            self.image_unact = self.og_image_unact
        self.image = self.image_act if self.is_active else self.image_unact

    def update_activity(self, item, act=None):
        if act == None:
            act = self.is_active
        self.item = item
        self.is_active = act
        
        if item != None:
            rect: pygame.rect.Rect = item.minimized_for_inv.get_rect()
            rect.center = self.image_act.get_rect().center

            self.image_act.blit(item.minimized_for_inv, rect)
            self.image_unact.blit(item.minimized_for_inv, rect)
        else:
            self.image_act = self.og_image_act
            self.image_unact = self.og_image_unact
        self.image = self.image_act if self.is_active else self.image_unact 

    def get_item(self):
        return self.item

    def draw(self, surf: pygame.Surface, top_left):
        surf.blit(self.image, pygame.Rect(top_left, self.image.get_rect().size))


class Inventory:
    def __init__(self) -> None:
        self.SLOT_NUMBER = 9
        self.INV_NUMBER = 27
        self.hotbar = [
            Slot(None, True),
            *[Slot(None) for i in range(self.SLOT_NUMBER - 1)],
        ]
        self.inventory = [Slot(None) for i in range(self.INV_NUMBER - 1)]
        self.selected = self.hotbar[0]
        self.selected_n = 0
        self.change_cd = 0.5 * FPS
        self.interaction_cd_const = 0.4*FPS
        self.interaction_cd = 0
        self.cd = 0
        self.developer_items()
        # Active slot events
    
    def add_to_inventory(self, item, count):
        slot = None
        i = 0
        all_inv = self.hotbar + self.inventory
        while i < len(all_inv):
            slot = all_inv[i]
            if slot.get_item() == item and slot.count+count <= 64:
                # found avalible slot
                slot.count += count
                item.parent = slot
                return True
            i+=1

        slot = None
        i = 0
        while i < len(all_inv):
            slot = all_inv[i]
            if slot.get_item() == None:
                # found
                slot.update_activity(item)
                item.parent = slot
                return True
            i += 1

        return False
    # REMOVE ON PUSH  
    def developer_items(self):
        # do not cheat or ill eat you

        self.hotbar[0].update_activity(crafting_table_item(self.hotbar[-1]), False)
        self.hotbar[0].count = 3
    def f_all(self, active_currently):
        for item in self.hotbar:
            # None | class<Item>
            if item is not active_currently:
                item.update_activity(item.get_item(), False)
            else:
                item.update_activity(item.get_item(), True)
    def check_info(self,info):

        if len(info) > 3:
            if info[8] == "0": # right
                self.selected.get_item().on_right_click(tuple(gui_coordinates), walls,breaked_stuff, blocks, colliders)
                self.interaction_cd = self.interaction_cd_const
            if info[10] == "0":
                self.selected.get_item().on_left_click(tuple(gui_coordinates), walls,breaked_stuff, blocks, colliders)
                self.interaction_cd = self.interaction_cd_const
    def tick(self, info, screen):
        # COOLDOWN
        if self.interaction_cd > 0:
            self.interaction_cd -=1
        else:
            self.interaction_cd = 0
            if self.selected.item != None:
                self.check_info(info)
        if self.cd > 0:
            self.cd -= 1
        else:
            self.cd = 0
            self.scroll(info)
        # 8, 10
        

        self.act_s()
        x = (WIDTH - (70 * (len(self.hotbar) + 2))) / 2
        for slot in self.hotbar:
            x += 70
            slot.draw(screen, (x, HEIGHT - 70))
            if slot.count > 1:

                text_surf = font_txt.render(str(slot.count), False, COUNT_COLOR)
                screen.blit(text_surf, (x+55, HEIGHT-30))

    def classify_np(self, info):
        if len(info) > 1:
            if info[4] == "0":
                # left
                return "l"
            elif info[6] == "0":
                return "r"
        return ""
        # ['516', '514', '1', '1:', '1', '2:', '1', '3:', '1', '4:', '1', '5:', '1', '6:', '1', '\n']

    def act_s(self):
        self.selected.is_active = True

    def scroll(self, info):
        np = self.classify_np(info)
        if np == "l":
            self.selected_n -= 1
            self.cd = self.change_cd
        if np == "r":
            self.selected_n += 1
            self.cd = self.change_cd
        if self.selected_n < 0:
            self.selected_n = self.SLOT_NUMBER - 1
        elif self.selected_n > self.SLOT_NUMBER - 1:
            self.selected_n = 0
        self.selected = self.hotbar[self.selected_n]
        self.f_all(self.selected)


class Generator:
    def __init__(self, player, wall_0) -> None:
        self.wall_0 = wall_0
        self.last_wall = wall_0
        self.player = player
        self.count = 1
        self.hardness = 0
        self.color_n = 1

    def generate(self):
        y = self.wall_0.rect.y
        c = y // 120

        for i in range(self.count, c + 1):
            j = random.randint(2, 3)
            self.last_y = walls.sprites()[-1].rect.y


            jump_h = sum(range(self.player.jumper + 1)) - player.rect.h - 25
            y = self.last_wall.rect.y - jump_h
            pw = list(range(250, 100 - 1, -25))
            while j > 0:
                w = random.choice(
                    pw[
                        min(int(self.hardness / 5), len(pw) - 2) : min(
                            int(self.hardness / 5), len(pw) - 2
                        )
                        + 3
                    ]
                )
                x = random.choice([ii for ii in range(0, WIDTH - w, 50)])

                new_wall = Wall((x - 26, y), (w + 52, 50))
                tries = 0
                while (
                    pygame.sprite.spritecollideany(new_wall, colliders) is not None
                ):  # or rect_group_collide(Wall((x, y+70), (w, 50)).rect, walls):
                    if tries > 50:

                        # left or right side:
                        if x < WIDTH / 2:  # left
                            x -= 75
                        else:
                            x += 75
                    else:
                        x = random.choice([ii for ii in range(0, WIDTH - w, 50)])

                    if tries == 70:
                        # while rect_group_collide(Wall((x, y+70), (w, 50)).rect, walls):
                        #     print("Randed")
                        #     x = random.choice([ii for ii in range(0, WIDTH-w, 50)])
                        new_wall = Wall((x - 26, y), (w + 52, 50))
                        break

                    tries += 1
                    # 0,06
                    new_wall = Wall((x - 26, y), (w + 52, 50), color=lst[self.color_n])
                    # new_wall_1 = Wall((x+75, self.last_wall.rect.y), (w-125, 50))
                j -= 1
                new_wall = Wall((x, y), (w, 50), color=lst[self.color_n])
                # walls_to_add.append(new_wall)
                walls.add(new_wall)
                colliders.add(new_wall)
            self.hardness += 1
            self.color_n += 1

            # last wall format: last_x, last_y_ last_w
            self.last_wall = new_wall
            self.count += 1
def convert_top_left_to_center(top_left_x, top_left_y, width, height):
    center_x = top_left_x + width / 2
    center_y = top_left_y + height / 2
    return center_x, center_y


class Classifier:
    def __init__(self, top_l, top_r, btm_l, btm_r, cent, cent_l, cent_r, cent_t):
        self.top_left = top_l
        self.top_right = top_r
        self.bottom_left = btm_l
        self.bottom_right = btm_r
        self.center = cent
        self.center_left = cent_l
        self.center_right = cent_r
        self.center_top = cent_t

    def classify(self, coords):
        x, y = coords
        if self.center is not None and self.in_range(coords, self.center):
            return "CENTER", None
        elif self.center_left is not None and self.in_range(coords, self.center_left):
            return "CENTER", "LEFT"
        elif self.center_right is not None and self.in_range(coords, self.center_right):
            return "CENTER", "RIGHT"
        elif self.center_top is not None and self.in_range(coords, self.center_top):
            return "TOP", "CENTER"
        elif self.top_left is not None and self.in_range(coords, self.top_left):
            return "TOP", "LEFT"
        elif self.top_right is not None and self.in_range(coords, self.top_right):
            return "TOP", "RIGHT"
        elif self.bottom_left is not None and self.in_range(coords, self.bottom_left):
            return "BOTTOM", "LEFT"
        elif self.bottom_right is not None and self.in_range(coords, self.bottom_right):
            return "BOTTOM", "RIGHT"
        else:
            return None, None

    def in_range(self, coords, target_coords, margin=350):
        target_x, target_y = target_coords
        x, y = coords
        return abs(x - target_x) <= margin and abs(y - target_y) <= margin


class Cub(pygame.sprite.Sprite):
    def __init__(self, size, ofs, hitty):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(random.choice([RED, WHITE, BLUE, GREEN]))
        self.rect = self.image.get_rect()
        self.rect.topleft = w(hitty.rect.topleft, ofs)
        self.hitty = hitty
        self.ofs = ofs

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.topleft = w(self.hitty.rect.topleft, self.ofs)

    def sync(self, *args: Any, **kwargs: Any) -> None:
        self.rect.topleft = w(self.hitty.rect.topleft, self.ofs)

    def touching(self) -> bool:
        return pygame.sprite.spritecollideany(self, colliders) != None


class Hitty(pygame.sprite.Sprite):
    def __init__(self, size, coords, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(RED)
        self.og_surf = self.image
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.player = player
        self.ii = 20
        self.angle = 0
        self.change_angle = 0

    def touching(self) -> bool:
        return pygame.sprite.spritecollideany(self, colliders) != None

    def update(self, classi) -> None:
        self.change_angle = -player.x_vel

        self.rect.x = player.rect.x
        self.rect.y = player.rect.y

    def check_left(self):
        self.rect.centerx -= self.ii
        if self.touching():
            self.rect.centerx += self.ii
            return False
        else:
            self.rect.centerx += self.ii
            return True

    def check_right(self):
        self.rect.centerx += self.ii
        if self.touching():
            self.rect.centerx -= self.ii
            return False
        else:
            self.rect.centerx -= self.ii
            return True

    def check_up(self):
        self.rect.centery -= self.ii
        if self.touching():
            self.rect.centery += self.ii
            return False
        else:
            self.rect.centery += self.ii
            return True

    def check_down(self):
        self.rect.centery += self.ii
        if self.touching():
            self.rect.centery -= self.ii
            return False
        else:
            self.rect.centery -= self.ii
            return True

    def suuper_check_x(self, dist):
        bt_ii = self.ii

        val = False
        self.ii = dist
        val = self.check_right()

        self.ii = bt_ii

        return val

    def suuper_check_y(self, dist):
        bt_ii = self.ii

        val = False
        self.ii = dist
        val = self.check_down()
        self.ii = bt_ii
        return val


class Wall(pygame.sprite.Sprite):
    def __init__(self, coords, size, mov=False, color=RED):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.player = player
        self.mov = mov
        self.mov2 = True
        self.riz = 0

    def update(self) -> None:

        if self.mov2 == True:
            self.rect.y -= player.y_vel
        if self.mov == True:
            self.riz += player.y_vel
        if self.riz <= -300:
            self.mov2 = False


class Player(pygame.sprite.Sprite):
    def __init__(self,inv):
        pygame.sprite.Sprite.__init__(self)

        self.og_surf = rm.get_player()
        self.image = self.og_surf
        self.rect = self.image.get_rect()
        self.rect.center = (
            WIDTH / 2,
            HEIGHT - self.rect.height + _HEIGHT_MODIFIER - 15,
        )
        self.y_vel = 0
        self.jump = False
        self.x_vel = 0
        self.move_down = True
        self.move_up = True
        self.move_left = True
        self.move_right = True
        self.hitbox = Hitty((50, 50), self.rect.center, self)
        self.angle = 0
        self.change_angle = 0
        self.jumper = 20
        self.inv = inv
    def rot(self):
        self.angle += self.change_angle
        self.image = playerz[round((self.angle) / 36)]

    def update(self, classified):
        self.change_angle = -(self.x_vel * 2)
        self.rot()
        self.hitbox.update(classified)

        # or not touching anything
        self.move_down = self.hitbox.check_down()
        self.move_up = self.hitbox.check_up()
        self.move_left = self.hitbox.check_left()
        self.move_right = self.hitbox.check_right()

        if self.move_down:
            self.y_vel += 1

        else:
            # touchedd the gras
            self.y_vel = 0
            self.jump = False


        if classified[0] == "TOP" and not self.jump and self.move_up:
            self.y_vel -= self.jumper
            self.jump = True
        if classified[0] == "CENTER" and classified[1] == None:
            self.x_vel = 0
        elif classified[1] == "RIGHT" and self.move_right:
            self.x_vel += 1
        elif classified[1] == "LEFT" and self.move_left:
            self.x_vel -= 1
        if not self.move_up and self.y_vel < 0:
            self.y_vel = 0

        if self.x_vel != 0 and not self.hitbox.suuper_check_x(self.x_vel):
            self.x_vel = 0
        if self.y_vel != 0 and not self.hitbox.suuper_check_y(self.y_vel):
            self.y_vel = 0
            # self.jump = False

        # self.rect.centery += self.y_vel
        self.rect.centerx += self.x_vel

        # self.rect.x += 5
        # if self.rect.left > WIDTH:
        #     self.rect.right = 0


def run_calibration(splt_val, last_val):
    global cd, ticky, calib, classi, calib_top_j_left, calib_top_j_right, calib_bottom_j_left, calib_bottom_j_right, calib_j_center, calib_center_left, calib_center_right, calib_center_top
    if calib == 0 and last_val != "":
        print("Hi! It's me, Calibrator. Now, we will calibrate your joystick!")
        calib = 1
    elif calib == 1:
        print("Press the joystick button to continue!")
        ticky = 1
        calib = 3
    elif ticky > (FPS * 3):
        ticky = 0
        calib = -1
        print("Okay, you left the Calibration process, loading from the file...")
        with open("classi.bin", "rb") as f:
            classi = pickle.load(
                f,
            )
    elif calib == 3 and splt_val[2] == "0":
        calib_j_center = (int(splt_val[0]), int(splt_val[1]))
        ticky = 0
        calib = 4
        print("Let's calibrate your joystick!")
        print("Move to the top left and press the joystick button!")
        cd = FPS * 2
    elif calib == 4 and splt_val[2] == "0" and cd == 0:
        calib_top_j_left = (int(splt_val[0]), int(splt_val[1]))
        print(calib_top_j_left)
        calib = 5
        print("Got it!")
        print("Move to the top right and press the joystick button again!")
        cd = FPS * 2
    elif calib == 5 and cd == 0 and splt_val[2] == "0":
        calib_top_j_right = (int(splt_val[0]), int(splt_val[1]))
        print(calib_top_j_right)
        calib = 6
        print("Got it!")
        print("Move to the bottom left and press the joystick button again!")
        cd = FPS * 2
    elif calib == 6 and cd == 0 and splt_val[2] == "0":
        calib_bottom_j_left = (int(splt_val[0]), int(splt_val[1]))
        print(calib_bottom_j_left)
        calib = 7
        print("Got it!")
        print("Move to the bottom right and press the joystick button!")
        cd = FPS * 2
    elif calib == 7 and splt_val[2] == "0" and cd == 0:
        calib_bottom_j_right = (int(splt_val[0]), int(splt_val[1]))
        print(calib_bottom_j_right)
        calib = 8
        print("Got it!")
        print("Move to the center left and press the joystick button again!")
        cd = FPS * 2
    elif calib == 8 and splt_val[2] == "0" and cd == 0:
        calib_center_left = (int(splt_val[0]), int(splt_val[1]))
        print(calib_center_left)
        calib = 9
        print("Got it!")
        print("Move to the center right and press the joystick button again!")
        cd = FPS * 2
    elif calib == 9 and splt_val[2] == "0" and cd == 0:
        calib_center_right = (int(splt_val[0]), int(splt_val[1]))
        print(calib_center_right)
        calib = 10
        print("Got it!")
        print("Move to the center top and press the joystick button again!")
        cd = FPS * 2
    elif calib == 10 and splt_val[2] == "0" and cd == 0:
        calib_center_top = (int(splt_val[0]), int(splt_val[1]))
        print(calib_center_top)
        calib = -1
        print("Calibration process is over. Bye!")
        classi = Classifier(
            calib_top_j_left,
            calib_top_j_right,
            calib_bottom_j_left,
            calib_bottom_j_right,
            calib_j_center,
            calib_center_left,
            calib_center_right,
            calib_center_top,
        )
        with open("classi.bin", "wb") as f:
            pickle.dump(classi, f)


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(os.getcwd().split("\\")[-1] + " - By RNT Development")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player(None)
all_sprites.add(player)
walls = pygame.sprite.Group()
wall_0 = Wall((WIDTH / 2, HEIGHT / 2 + 200 + _HEIGHT_MODIFIER), (250, 50))
walls.add(wall_0)
wall = Wall((WIDTH / 2, HEIGHT + _HEIGHT_MODIFIER), (WIDTH, 50))
walls.add(wall)
wall = Wall((25, HEIGHT + _HEIGHT_MODIFIER - 475), (50, 1000), True)
walls.add(wall)
wall = Wall((WIDTH, HEIGHT + _HEIGHT_MODIFIER - 475), (50, 1000), True)
walls.add(wall)

colliders = pygame.sprite.Group()
for wall in walls.sprites():
    colliders.add(wall)

# all_sprites.add(player.hitbox)
thrd = Informator(inf_q)
thrd.start()
# Цикл игры
running = True
calib = 0
last_val = ""
ticky = 0

cd = 0
calib_top_j_left = None
calib_top_j_right = None
calib_bottom_j_left = None
calib_bottom_j_right = None
calib_j_center = None
calib_center_top = None
calib_center_left = None
calib_center_right = None
classi: Classifier = None
inventory = Inventory()
player.inv = inventory
all_sprites.add(player)
gen = Generator(player, wall_0)
gui_coordinates = [0,0]
blocks = pygame.sprite.Group()
breaked_stuff = pygame.sprite.Group()

def blit_l(l, screen):
    for obj in l:
        screen.blit(obj.image, obj.rect)
pygame.mouse.set_visible(False)

while running:
    # print(last_val)
    if cd > 0:
        cd -= 1
    clock.tick(FPS)
    if ticky != 0:
        ticky += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not inf_q.empty():
        last_val = inf_q.get(False)
    last_val = last_val.strip()
    splt_val = last_val.split(" ")

    if calib != -1:
        run_calibration(
            splt_val, last_val
        )  # ['516', '514', '1', '1:', '1', '2:', '1', '3:', '1', '4:', '1', '5:', '1', '6:', '1', '\n']
    if classi != None:
        all_sprites.update(classi.classify((int(splt_val[0]), int(splt_val[1]))))
        # print(splt_val, splt_val[10])
        blocks.update(splt_val[10] == "0", player,gui_coordinates)
        second_joystick_classified = classi.classify((int(splt_val[-3]),int(splt_val[-2])))
        if second_joystick_classified[0] == "TOP" and gui_coordinates[1]-GUI_SENSA > 0:
            gui_coordinates[1] -= GUI_SENSA
        elif second_joystick_classified[0] == "BOTTOM" and gui_coordinates[1]-GUI_SENSA < HEIGHT:
            gui_coordinates[1] += GUI_SENSA

        if second_joystick_classified[1] == "RIGHT" and gui_coordinates[0]-GUI_SENSA < WIDTH:
            gui_coordinates[0] += GUI_SENSA
        elif second_joystick_classified[1] == "LEFT" and gui_coordinates[0]-GUI_SENSA > 0:
            gui_coordinates[0] -= GUI_SENSA

    else:
        all_sprites.update((None, None))
        blocks.update(False, player,gui_coordinates)

    breaked_stuff.update(player, colliders)
    walls.update()

    gen.generate()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    walls.draw(screen)
    blocks.draw(screen)
    #screen.blit(scope, convert_top_left_to_center(gui_coordinates[0], gui_coordinates[1], scope.get_width(), scope.get_height()))
    screen.blit(scope, tuple(gui_coordinates))
    breaked_stuff.draw(screen)
    inventory.tick(splt_val, screen)
    # blit_l([player.hitbox.topl, player.hitbox.topr, player.hitbox.btml, player.hitbox.btml], screen)
    pygame.display.flip()
if proc != None:
    proc.kill()
pygame.quit()
