from typing import Any
import pygame
import random
import serial as sm
# import keyboard
import threading
import queue
import time
import os
import math
import pickle
from environment.classifier import Classifier
from environment.generator import Generator
import subprocess
from blocks.crafting_table import CraftingTable as crafting_table_item
from pathlib import Path
from player.player import Player
from res.resource_manager import resource_manager as rm
from inventory import inventory_gui as inv
from inventory.inventory import inventory
from other.utils import *
from other.cons import *
from player.wall import Wall
from gui.gui_module.gui_holder import GuiGroup
from inventory.inventory_gui import gui
from gui.gui_module.irs import o_irs



scope = rm.get_scope()
proc = None
try:
    serial = sm.Serial("COM6")
except Exception as e:
    proc = subprocess.Popen(["python", "simulator.py"])
    time.sleep(1)
    serial = sm.Serial("COM9")

print_lock = threading.Lock()
inf_q = queue.Queue()



pygame.font.init()



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
                    try:
                        inf_q.put(str(rl, encoding="utf-8"))
                    except UnicodeDecodeError:
                        pass


# class Informator(threading.Thread):
#     def __init__(self, queue, args=(), kwargs=None):
#         threading.Thread.__init__(self, args=(), kwargs=None)
#         self.queue = queue
#         self.daemon = True

#     def run(self):
#         self.do_thing()

#     def do_thing(self):
#         global running
#         while True:
#             pos1 = "520 518"
#             try:
#                 if keyboard.is_pressed('w'):
#                     pos1 = "520 0"
#                 elif keyboard.is_pressed('a'):
#                     pos1 = "0 518"
#                 elif keyboard.is_pressed('s'):
#                     pos1 = "520 1023"
#                 elif keyboard.is_pressed('d'):
#                     pos1 = "1023 518"
#                 if keyboard.is_pressed('left shift'):
#                     pos1 += " 0"
#                 else:
#                     pos1 += " 1"
#             except:
#                 pass

#             pos2 = "520 518"
#             try:
#                 if keyboard.is_pressed('up'):
#                     pos2 = "520 0"
#                 elif keyboard.is_pressed('left'):
#                     pos2 = "0 518"
#                 elif keyboard.is_pressed('down'):
#                     pos2 = "520 1023"
#                 elif keyboard.is_pressed('right'):
#                     pos2 = "1023 518"
#                 if keyboard.is_pressed('right shift'):
#                     pos2 += " 0"
#                 else:
#                     pos2 += " 1"
#             except:
#                 pass
#             btns = ''
#             try:
#                 btns += '1: 0 ' if keyboard.is_pressed('z') else '1: 1 '
#                 btns += '2: 0 ' if keyboard.is_pressed('x') else '2: 1 '
#                 btns += '3: 0 ' if keyboard.is_pressed('c') else '3: 1 '
#                 btns += '4: 0 ' if keyboard.is_pressed('v') else '4: 1 '
#                 btns += '5: 0 ' if keyboard.is_pressed('b') else '5: 1 '
#                 btns += '6: 0' if keyboard.is_pressed('n') else '6: 1'
#             except:
#                 pass
#             inf_q.put(' '.join([pos1, btns, pos2]))
#             time.sleep(0.2)


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
        with open("environment/classi.bin", "rb") as f:
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

        calib = 5
        print("Got it!")
        print("Move to the top right and press the joystick button again!")
        cd = FPS * 2
    elif calib == 5 and cd == 0 and splt_val[2] == "0":
        calib_top_j_right = (int(splt_val[0]), int(splt_val[1]))

        calib = 6
        print("Got it!")
        print("Move to the bottom left and press the joystick button again!")
        cd = FPS * 2
    elif calib == 6 and cd == 0 and splt_val[2] == "0":
        calib_bottom_j_left = (int(splt_val[0]), int(splt_val[1]))

        calib = 7
        print("Got it!")
        print("Move to the bottom right and press the joystick button!")
        cd = FPS * 2
    elif calib == 7 and splt_val[2] == "0" and cd == 0:
        calib_bottom_j_right = (int(splt_val[0]), int(splt_val[1]))
  
        calib = 8
        print("Got it!")
        print("Move to the center left and press the joystick button again!")
        cd = FPS * 2
    elif calib == 8 and splt_val[2] == "0" and cd == 0:
        calib_center_left = (int(splt_val[0]), int(splt_val[1]))

        calib = 9
        print("Got it!")
        print("Move to the center right and press the joystick button again!")
        cd = FPS * 2
    elif calib == 9 and splt_val[2] == "0" and cd == 0:
        calib_center_right = (int(splt_val[0]), int(splt_val[1]))

        calib = 10
        print("Got it!")
        print("Move to the center top and press the joystick button again!")
        cd = FPS * 2
    elif calib == 10 and splt_val[2] == "0" and cd == 0:
        calib_center_top = (int(splt_val[0]), int(splt_val[1]))

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
        with open("environment/classi.bin", "wb") as f:
            pickle.dump(classi, f)


# Создаем игру и окно
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT),)

pygame.display.set_caption(os.getcwd().split("\\")[-1] + " - By RNT Development")
clock = pygame.time.Clock()
player_group = pygame.sprite.GroupSingle()
colliders = pygame.sprite.Group()
walls = pygame.sprite.Group()
blocks = pygame.sprite.Group()
breaked_stuff = pygame.sprite.Group()

player = Player(None, colliders)

wall_0 = Wall((WIDTH / 2, HEIGHT / 2 + 200 + HEIGHT_MODIFIER ), (250, 50),player=player)

walls.add(wall_0)
wall = Wall((WIDTH / 2, HEIGHT + HEIGHT_MODIFIER), (WIDTH, 50),player=player)

walls.add(wall)
wall = Wall((25, HEIGHT + HEIGHT_MODIFIER - 475), (50, 1000), mov=True,player=player)
walls.add(wall)
wall = Wall((WIDTH, HEIGHT + HEIGHT_MODIFIER - 475), (50, 1000), mov=True,player=player)
walls.add(wall)


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
# inventory = Inventory()
player.inv = inventory
player_group.add(player)
gen = Generator(player, wall_0)
gui_coordinates = [0, 0]

gui_group = GuiGroup()
gui_group.add(inv.gui, inv.tick)

# def blit_l(l, screen):
#     for obj in l:
#         screen.blit(obj.image, obj.rect)


pygame.mouse.set_visible(False)

while running:

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
    screen.fill(BLACK)
    # if last_val != "":
    #     print(splt_val[2])
    if calib != -1:
        run_calibration(
            splt_val, last_val
        )  # ['516', '514', '1', '1:', '1', '2:', '1', '3:', '1', '4:', '1', '5:', '1', '6:', '1', '\n']
    rim_added = None
    if classi != None:
        player_group.update(classi.classify((int(splt_val[0]), int(splt_val[1]))), splt_val)
        # print(classi.center)
        wrek = pygame.Rect(gui_coordinates[0], gui_coordinates[1], rm.get_scope().get_width(), rm.get_scope().get_height())
        blocked = False
        for block in blocks.sprites():

            if block.rect.colliderect(wrek):
                # got them
                
                rim_added =block.rect
                srf = rm.get_scope_on_block()

                blocked = True
        if not blocked:
            rim_added = grd.get_nearest(tuple(gui_coordinates))
            if Utilz.good_location(rim_added.topleft, colliders, player.rect.center):
                srf = rm.get_scope_on_good_loc()
            else:
                srf = rm.get_scope_on_bad_loc()
      
            blocked = True
        updatik = DataClass_Transporter(splt_val[10] == "0")
        gui_group.update(gui_coordinates, splt_val)
        blocks.update(updatik, player, gui_coordinates)
        second_joystick_classified = classi.classify(
            (int(splt_val[-3]), int(splt_val[-2]))
        )
        if (
            second_joystick_classified[0] == "TOP"
            and gui_coordinates[1] - GUI_SENSA > 0
        ):
            gui_coordinates[1] -= GUI_SENSA
        elif (
            second_joystick_classified[0] == "BOTTOM"
            and gui_coordinates[1] - GUI_SENSA < HEIGHT
        ):
            gui_coordinates[1] += GUI_SENSA

        if (
            second_joystick_classified[1] == "RIGHT"
            and gui_coordinates[0] - GUI_SENSA < WIDTH
        ):
            gui_coordinates[0] += GUI_SENSA
        elif (
            second_joystick_classified[1] == "LEFT"
            and gui_coordinates[0] - GUI_SENSA > 0
        ):
            gui_coordinates[0] -= GUI_SENSA

    else:
        player_group.update((None, None),None)
        blocks.update(False, player, gui_coordinates)

    breaked_stuff.update(player, colliders)
    walls.update()
    
    

    gen.generate(walls, colliders)
    grd.greedy(player)
    walls.draw(screen)
    blocks.draw(screen)
    

    screen.blit(player.image, (player.rect.topleft[0],player.rect.topleft[1]+player.game_changer*2))
    if rim_added != None:
        screen.blit(srf, rim_added.topleft)
    gui_group.draw(screen)
    # screen.blit(scope, convert_top_left_to_center(gui_coordinates[0], gui_coordinates[1], scope.get_width(), scope.get_height()))

    breaked_stuff.draw(screen)

    # walls, breaked_stuff, blocks, colliders
    inventory.tick(splt_val, screen,player,gui_coordinates,walls, breaked_stuff, blocks, colliders)
    o_irs.draw(screen, gui_coordinates)
    # blit_l([player.hitbox.topl, player.hitbox.topr, player.hitbox.btml, player.hitbox.btml], screen)
    pygame.display.flip()
if proc != None:
    proc.kill()
pygame.quit()
