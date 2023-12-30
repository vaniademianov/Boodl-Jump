from gui.gui_module.button import Button
from inventory.slot import Slot
from other.utils import Utilz
import pygame
from res.resource_manager import resource_manager as rm
from other.cons import COUNT_COLOR, font_txt, FPS, GUI_SLOT_COLOR_II
from items.item import IItem
import copy
class GUIslot(Button,):
    def __init__(self,size,color, borders, center,boh,crs, parent:Slot) -> None:
        self.parent_slot = parent
        self.size = size 
        self.coords = center

        self.crs_obj = crs
        self.last_remembered_item = ""
        super().__init__(color, borders,size,center,boh)
        self.mover_time = int(FPS/2)
        self.ore_surf = self.or_surf.copy()
        self.mover = Utilz.generate_color_transition(color, GUI_SLOT_COLOR_II,self.mover_time)
        self.moving_anim_active = False
        self.moving_anim_bck = False
        self.moving_anim_progress = 0
        self.hovered_last_time = False
        self.hovering = False
        self.moving_anim_ready = False
    def on_hover(self):
        self.hovered_last_time = True
    def disable_hovers(self):
        if self.hovered_last_time: 
            self.hovering = True
            if not self.moving_anim_active and not self.moving_anim_ready:
                self.moving_anim_active = True
                self.moving_anim_bck = False
                self.moving_anim_progress = 0
                self.moving_anim_ready = False
        else:
            self.hovering = False
        self.hovered_last_time = False
        


    def change_parent_surfaces(self, new_srf):
        self.or_surf = new_srf.copy()
        self.surface = new_srf.copy()
    def on_left_click(self):
        # uh do stuff
        if type(self.crs_obj.item) != type(self.parent_slot.item):
            crs_count = self.crs_obj.count 
            crs_item = copy.copy(self.crs_obj.item)
            
            self.crs_obj.count = self.parent_slot.count
            self.crs_obj.item = copy.copy(self.parent_slot.item)
            self.parent_slot.item = copy.copy(crs_item)
            self.parent_slot.count = crs_count 
        else:
            self.parent_slot.count += self.crs_obj.count
            self.crs_obj.item = None
            self.crs_obj.count = 0
    def on_right_click(self):
        # get one

        if self.crs_obj.item == None or self.crs_obj.item == self.parent_slot.item:
            if self.parent_slot.count > 0:
                self.parent_slot.count -= 1
                self.crs_obj.count+= 1
                if type(self.crs_obj.item) != type(self.parent_slot.item):
                    self.crs_obj.item = self.parent_slot.item
                if self.parent_slot.count <= 0:
                    self.parent_slot.count = 0
                    self.parent_slot.update_activity(None)
                
    def draw(self, screen):
        screen.blit(self.surface,Utilz.convert_center_to_top_left(self.coords[0], self.coords[1], self.size[0], self.size[1]))
        if self.parent_slot.count > 1:
            # render count
            
            txt_srf = font_txt.render(str(self.parent_slot.count), False, COUNT_COLOR)
            coords = Utilz.w(self.coords, Utilz.wd(self.size,2))
            coords = Utilz.w(self.coords, (20,5))
            screen.blit(txt_srf,coords)
    def blit_item(self, item_mini):
        # rect = item.minimized_for_inv.get_rect()
        rect = item_mini.get_rect()
        rect.center = self.coords
    
        srf = self.ore_surf.copy()
        srf.blit(item_mini, Utilz.wd(self.size,4))

        self.change_parent_surfaces(srf)
    def update_color(self, color):
        # things

        self.neat_init(color)
        self.ore_surf = self.or_surf
        if self.parent_slot.item != None:
            self.blit_item(self.parent_slot.item.minimized_for_inv)
    def sync(self):
        self.yes_y(self.y)
        # sync with slotik 
        # print(self.x, self.y)
        if self.last_remembered_item != self.parent_slot.item:
            if self.parent_slot.item != None:
                self.blit_item(self.parent_slot.item.minimized_for_inv)
            else:
                self.change_parent_surfaces(self.ore_surf.copy())
            self.last_remembered_item = self.parent_slot.item 
        # update animations
        self.moving_anim_progress = int(self.moving_anim_progress)
        if self.moving_anim_active:
            self.moving_anim_progress += 1
            
            self.update_color(self.mover[self.moving_anim_progress-1])
            if self.moving_anim_progress >= self.mover_time:
                self.moving_anim_active = False
                self.moving_anim_ready = True
                self.moving_anim_progress = self.mover_time
                self.moving_anim_progress = int(self.moving_anim_progress)

                self.update_color(self.mover[self.moving_anim_progress-1])
        if not self.hovering:
            
            if self.moving_anim_ready:

                self.moving_anim_ready = False
                self.moving_anim_bck = True
                self.moving_anim_progress = self.mover_time
                self.update_color(self.mover[self.moving_anim_progress-1])
            if self.moving_anim_bck:
                self.moving_anim_progress -= 1
                self.update_color(self.mover[self.moving_anim_progress])
                if self.moving_anim_progress <= 0:
                    self.moving_anim_active = False
                    self.moving_anim_ready = False
                    self.moving_anim_active = False
                    self.moving_anim_progress = 0
                    self.moving_anim_bck = False
                    
                    self.update_color(self.mover[0])