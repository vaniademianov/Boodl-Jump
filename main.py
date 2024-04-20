from typing import Any
import pygame
import random
import serial as sm
# import keyboard
import threading
import queue
from controller import Controller
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
from inventory import universal_inventory_gui as inv
from inventory.inventory import inventory
from other.utils import *
from controller import Controller
from other.cons import *
from player.wall import Wall
from gui.gui_module.gui_holder import GuiGroup
from inventory.universal_inventory_gui import gui
from gui.gui_module.irs import o_irs
from inventory import inventory_gui as ne_uni_gui



scope = rm.get_scope()
proc = None

print_lock = threading.Lock()
inf_q = queue.Queue()



pygame.font.init()






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
controller = Controller()
controller.controller_calibration()


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
# inventory = Inventory()
player.inv = inventory
player_group.add(player)
gen = Generator(player, wall_0)
gui_coordinates = [WIDTH/2, HEIGHT/2]

gui_group = GuiGroup()

gui_group.add(inv.gui, inv.tick)

gui_group.add(ne_uni_gui.gui, ne_uni_gui.tick)
gui_group.add(ne_uni_gui.wardrobe)

inv.dropped_items = breaked_stuff

# def blit_l(l, screen):
#     for obj in l:
#         screen.blit(obj.image, obj.rect)
tp_anim_progress = 0
tp_back_anim_active = False
tp_anim_active = False
last_remembered_activ_state = False
tp_anim_spd = 155/(TRANSPARENCY_ANIMATION_SPEED*30) 

pygame.mouse.set_visible(False)
tp_anim_ready = False
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
    if controller.is_classifier_available:
        player_group.update(controller.classify_joystick(0), splt_val)
        # print(classi.center)
        wrek = pygame.Rect(gui_coordinates[0], gui_coordinates[1], rm.get_scope().get_width(), rm.get_scope().get_height())
        blocked = False
        miniblock = None
        block_blocked = False
        if inventory.selected != None and inventory.selected.item != None:
            if inventory.selected.item.is_block:
                miniblock:pygame.Surface = inventory.selected.item.blocky_image.copy()
                miniblock.convert_alpha()
                miniblock.set_alpha(100)

        for block in blocks.sprites():

            if block.rect.colliderect(wrek):
                # got them
                
                rim_added =block.rect
                if Utilz.calc_dist_rec(block.rect, player.rect) < INTERACTION_DISTANCE:
                    srf = rm.get_scope_on_block()
                else:
                    srf = rm.get_scope_on_isnt_breakable()
                block_blocked = True
                blocked = True
        if not blocked:
            rim_added = grd.get_nearest(tuple(gui_coordinates))
            if Utilz.good_location(rim_added.topleft, colliders, player.rect.center,player):
                srf = rm.get_scope_on_good_loc()
            else:
                srf = rm.get_scope_on_bad_loc()
      
            blocked = True
            block_blocked = False
        updatik = DataClass_Transporter(controller.read_button_state(0))
        gui_group.update(gui_coordinates, splt_val,player)
        blocks.update(updatik, player, gui_coordinates)
        second_joystick_classified = controller.classify_joystick(1)
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
        if splt_val[12] == "0" and inventory.drop_cooldown == 0: 
            # Drop item 
            inventory.drop_cooldown = FPS/3
            if o_irs.item != None and o_irs.count > 0:
                # dropping from gui then

                for i in range(o_irs.count):
                    new_mini = o_irs.item.mini(o_irs.last_pos)
                    new_mini.activate_override(player.rect.center,gui_coordinates)
                o_irs.item = None
                o_irs.count = 0
            elif inventory.selected.item != None: 
                inventory.selected.count -= 1 
                new_mini = inventory.selected.item.mini(gui_coordinates)
                breaked_stuff.add(new_mini)
                new_mini.activate_override(player.rect.center,gui_coordinates)
                if inventory.selected.count <= 0: 
                    inventory.selected.update_activity(None)
                
    else:
        player_group.update((None, None),None)
        blocks.update(False, player, gui_coordinates)
    walls.update()
    breaked_stuff.update(player, colliders)

    
    

    gen.generate(walls, colliders)
    grd.greedy(player)
    walls.draw(screen)
    blocks.draw(screen)
    

    screen.blit(player.image, (player.rect.topleft[0],player.rect.topleft[1]+player.game_changer*2))
    if rim_added != None:
        if block_blocked:
            screen.blit(srf, Utilz.wm(rim_added.topleft, (4,4)))
        else:
            if miniblock != None:
                screen.blit(miniblock, rim_added.topleft)
            screen.blit(srf, rim_added.topleft)
    # screen.blit(scope, convert_top_left_to_center(gui_coordinates[0], gui_coordinates[1], scope.get_width(), scope.get_height()))

    breaked_stuff.draw(screen)

    # walls, breaked_stuff, blocks, colliders
    inventory.tick(splt_val, screen,player,gui_coordinates,walls, breaked_stuff, blocks, colliders)

    if inv.gui.is_visible != last_remembered_activ_state:
        
        if inv.gui.is_visible and not tp_anim_active and not tp_anim_ready:
            tp_anim_active= True
            tp_anim_progress = 0
            screen.fill((255-tp_anim_progress, 255-tp_anim_progress, 255-tp_anim_progress, 100), special_flags=pygame.BLEND_MULT)
            last_remembered_activ_state = inv.gui.is_visible
        elif not inv.is_leaving and tp_anim_ready:
            tp_back_anim_active = True

            tp_anim_progress = 155
            last_remembered_activ_state = inv.gui.is_visible
            tp_anim_ready = False
            screen.fill((255-tp_anim_progress, 255-tp_anim_progress, 255-tp_anim_progress, 100), special_flags=pygame.BLEND_MULT)
    if tp_anim_active:
        tp_anim_progress += round(tp_anim_spd)
        screen.fill((255-tp_anim_progress, 255-tp_anim_progress, 255-tp_anim_progress, 100), special_flags=pygame.BLEND_MULT)
        if tp_anim_progress >= 155:
            
            tp_anim_ready = True
            tp_anim_active = False
            tp_anim_progress = 155
    if tp_back_anim_active:

        tp_anim_progress -= round(tp_anim_spd)
        tp_anim_progress = int(tp_anim_progress)
       
        
        if tp_anim_progress <= 0:
            tp_anim_ready = False
            tp_anim_active = False
            tp_anim_progress = 0
            tp_back_anim_active = False

        else:
            screen.fill((255-tp_anim_progress, 255-tp_anim_progress, 255-tp_anim_progress, 100), special_flags=pygame.BLEND_MULT)
    if tp_anim_ready and not tp_back_anim_active: 
        screen.fill((255-tp_anim_progress, 255-tp_anim_progress, 255-tp_anim_progress, 100), special_flags=pygame.BLEND_MULT)
    gui_group.draw(screen)
    o_irs.draw(screen, gui_coordinates)
    # blit_l([player.hitbox.topl, player.hitbox.topr, player.hitbox.btml, player.hitbox.btml], screen)
    pygame.display.flip()
if proc != None:
    proc.kill()
pygame.quit()
