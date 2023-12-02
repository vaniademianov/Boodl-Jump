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
from pathlib import Path
try:
    serial = sm.Serial("COM6")
except Exception as e:
    print(e)
    serial = sm.Serial("COM9")
WIDTH = 800
HEIGHT = 650
FPS = 30
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
                rl =serial.readline()
                sl = str(rl)
                if "\\n" in sl:
                    inf_q.put(str(rl,encoding="utf-8"))
def w(a:tuple, b:tuple):
    return (a[0]+b[0], a[1]+b[1])
def wm(a:tuple, b:tuple):
    return (a[0]-b[0], a[1]-b[1])
def wd(a:tuple, b:int):
    return (a[0]/b, a[1]/b)
class Generator:
    def __init__(self, player, wall_0) -> None:
        self.wall_0 = wall_0
        self.last_wall = wall_0
        self.player = player
        self.count = 1
        self.hardness = 1

    def generate(self):
        y = self.wall_0.rect.y
        c = y // 150

        for i in range(self.count, c + 1):
            j = random.randint(1, 2)
            while j > 0:
                w = random.choice([150, 200])
                x = random.randint(0, WIDTH-w)
                print(sum(range(self.player.jumper + 1))-50)
                y = self.last_wall.rect.y - random.randint(120, sum(range(self.player.jumper + 1))-50)

                new_wall = Wall((x-50, y), (w+50, 50))
                # new_wall_1 = Wall((x+75, self.last_wall.rect.y), (w-125, 50))

                while pygame.sprite.spritecollideany(new_wall, walls):
                    x = random.randint(0, WIDTH-100)
                    new_wall = Wall((x-50, y), (w+50, 50))
                    # new_wall_1 = Wall((x+75, self.last_wall.rect.y), (w-125, 50))

                j -= 1
                new_wall = Wall((x, y), (w, 50))
                walls.add(new_wall)
            self.hardness += 0.02
            # last wall format: last_x, last_y_ last_w
            self.last_wall = new_wall
            self.count += 1
class Classifier:
    def __init__(self, top_l, top_r, btm_l, btm_r, cent, cent_l, cent_r,cent_t):
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
    def __init__(self, size, ofs,hitty):
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
        return pygame.sprite.spritecollideany(self,walls) != None
        # list > True
    
def the_one(a,b):
    return (True in [a,b])
class Hitty(pygame.sprite.Sprite):
    def __init__(self, size, coords,player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.player = player
        self.ii = 20
    def touching(self) -> bool:
        return pygame.sprite.spritecollideany(self,walls) != None
    def update(self, classi) -> None:
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        
    def check_left(self):
        # if self.ii != 1:
        #     print(self.ii)
        self.rect.centerx-=self.ii
        if self.touching():
            # print("ok")
            self.rect.centerx+=self.ii
            return False
        else: 
            self.rect.centerx +=self.ii
            return True
    def check_right(self):
        # if self.ii != 1:
        #     print(self.ii)
        self.rect.centerx+=self.ii
        if self.touching():
            # print("ok")
            self.rect.centerx-=self.ii
            return False
        else: 
            self.rect.centerx -=self.ii
            return True
    def check_up(self):
        # if self.ii != 1:
        #     print(self.ii)
        self.rect.centery-=self.ii
        if self.touching():
            # print("ok")
            self.rect.centery+=self.ii
            return False
        else: 
            self.rect.centery +=self.ii
            return True
    def check_down(self):
        # if self.ii != 1:
        #     print(self.ii)
        self.rect.centery+=self.ii
        if self.touching():
            # print("ok")
            self.rect.centery-=self.ii
            return False
        else: 
            self.rect.centery -=self.ii
            return True
    def suuper_check_x(self, dist):
        bt_ii = self.ii
        # dist - 
        val = False
        self.ii = dist
        val = self.check_right()
        # print(val, "checked by", self.ii)
        self.ii = bt_ii
        # if val == False:

            # print("Super check fals!")
        #print("moved by", dist, val)
        return val
    def suuper_check_y(self, dist):
        bt_ii = self.ii
        # dist - 
        val = False
        self.ii = dist
        val = self.check_down()
        # print(val, "checked by", self.ii)
        self.ii = bt_ii
        # if val == False:

        #     print("Super check fals!")
        #print("moved by", dist, val)
        return val
class Wall(pygame.sprite.Sprite):
    def __init__(self, coords, size,mov=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.player = player
        self.mov = mov
        self.mov2 = True
        self.riz = 0
        
    def update(self) -> None:
        #self.rect.x -= player.x_vel
        # if self.mov == True:
        #     print(self.mov2)
        if self.mov2 == True:
            
            self.rect.y -= player.y_vel
        if self.mov == True:
            self.riz += player.y_vel
        if self.riz <= -400:
            self.mov2 = False

        else:
            
            self.mov2 = True
            
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT-self.rect.height+_HEIGHT_MODIFIER-15)
        self.y_vel = 0
        self.jump = False
        self.x_vel = 0
        self.move_down = True
        self.move_up = True
        self.move_left = True
        self.move_right = True
        self.hitbox = Hitty((50,50), self.rect.center,self)
        all_sprites.add(self.hitbox)
        self.jumper = 20
    def update(self,classified):
        # or not touching anything
        self.move_down = self.hitbox.check_down()
        self.move_up = self.hitbox.check_up()
        self.move_left = self.hitbox.check_left()
        self.move_right = self.hitbox.check_right()
        # print(self.move_down, self.move_up, self.move_left, self.move_right, self.y_vel)
        if self.move_down:
            self.y_vel+= 1

        else:
            # touchedd the gras
            self.y_vel = 0
            self.jump = False
        
        # if self.y_vel > 0:
        #     self.y_vel -= 1
        # elif self.y_vel < 0:
        #     self.y_vel += 1
        # if math.ceil(self.x_vel) > 0:
        #     self.x_vel -= 1
        # elif math.ceil(self.x_vel) < 0:
        #     self.x_vel += 1
        # else:
        #     self.jump = False
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
    global cd,ticky, calib, classi, calib_top_j_left, calib_top_j_right, calib_bottom_j_left, calib_bottom_j_right, calib_j_center, calib_center_left, calib_center_right, calib_center_top
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
            classi = pickle.load(f,)
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
        classi = Classifier(calib_top_j_left, calib_top_j_right, calib_bottom_j_left, calib_bottom_j_right, calib_j_center, calib_center_left, calib_center_right,calib_center_top)
        with open("classi.bin", "wb") as f:
            pickle.dump(classi, f) 

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(os.getcwd().split("\\")[-1])
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
walls = pygame.sprite.Group()
wall_0 = Wall((WIDTH / 2, HEIGHT / 2+200 +_HEIGHT_MODIFIER),(250, 50))
walls.add(wall_0)
wall = Wall((WIDTH/2, HEIGHT + _HEIGHT_MODIFIER), (WIDTH, 50))
walls.add(wall)
wall = Wall((25, HEIGHT + _HEIGHT_MODIFIER - 475), (50, 1000), True)
walls.add(wall)
wall = Wall((WIDTH, HEIGHT + _HEIGHT_MODIFIER - 475), (50, 1000), True)
walls.add(wall)
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
classi:Classifier = None
gen = Generator(player, wall_0)
def blit_l(l, screen):
    for obj in l:
        screen.blit(obj.image, obj.rect)
while running:
    #print(last_val)
    if cd > 0:
        cd -= 1
    clock.tick(FPS)
    if ticky != 0:
        ticky += 1
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
    
    if not inf_q.empty():
        last_val=  inf_q.get(False)
    splt_val = last_val.split(" ")
    if calib != -1:
        run_calibration(splt_val, last_val)
    #print(last_val)
    # else:
    #     print(classi.classify((int(splt_val[0]), int(splt_val[1]))))
    # if calib == -1 and cd == 0:
    #     print(splt_val
    #)
    if classi != None:
        all_sprites.update(classi.classify((int(splt_val[0]), int(splt_val[1]))))
    else:
        all_sprites.update((None,None))

    walls.update()
    gen.generate()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    walls.draw(screen)
    
    # blit_l([player.hitbox.topl, player.hitbox.topr, player.hitbox.btml, player.hitbox.btml], screen)
    pygame.display.flip()

pygame.quit()
