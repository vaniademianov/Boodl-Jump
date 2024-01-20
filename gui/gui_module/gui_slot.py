from gui.gui_module.button import Button
from inventory.slot import Slot
from other.utils import Utilz
import pygame
from res.resource_manager import resource_manager as rm
from other.cons import BLACK, COUNT_COLOR, font_txt, FPS, GUI_SLOT_COLOR_II, SECOND_INV_COLOR
from items.item import IItem
import copy
from gui.gui_module.element import Element
from gui.gui_module.event_types import HOVER, LEFT_CLICK, RIGHT_CLICK
from gui.gui_module.gui import Gui
from gui.gui_module.frame import Frame
from gui.gui_module.label import Label

class GUIslot(Button,):
    def __init__(self,size,color, borders, center,boh,crs, parent:Slot=None,custom_borders = None,stroke_w=None, stroke_color=None,afterclick = None ) -> None:
        self.parent_slot = parent
        self.size = size 
        # self.coords = center

        self.crs_obj = crs
        self.last_remembered_item = ""
        super().__init__(color, borders,size,center,boh,custom_borders,stroke_color, stroke_w)
        self.mover_time = int(FPS/2)
        self.ore_surf = self.or_surf.copy()
        self.mover = Utilz.generate_color_transition(color, GUI_SLOT_COLOR_II,self.mover_time)
        self.moving_anim_active = False
        self.moving_anim_bck = False
        self.moving_anim_progress = 0
        self.hovered_last_time = False
        self.hovering = False
        self.moving_anim_ready = False
        self.toch_h_last_time = False
        self.after_click = afterclick
        # SETUP TIP GUI
        self.tip_gui = Gui(False)

        self.title_label = Label("NULL", BLACK, 28, "Brownie", (200,120), False)
        self.title_label.pack(self.tip_gui, -1)

        self.tip_gui_label = [self.title_label]

        self.tip_frame= Frame(SECOND_INV_COLOR,16,(200, 120), center, False)
        self.tip_frame.pack(self.tip_gui, 0)
    def update_tip_coords(self, coords):
        self.tip_frame.coordinates.x = coords[0]
        self.tip_frame.coordinates.y = coords[1]
        self.tip_frame.coordinates.x, self.tip_frame.coordinates.y = Utilz.convert_top_left_to_center(self.tip_frame.coordinates.x, self.tip_frame.coordinates.y, *self.tip_frame.surface.get_size())
        self.tip_frame.coordinates.x, self.tip_frame.coordinates.y = Utilz.w((self.tip_frame.coordinates.x, self.tip_frame.coordinates.y), (20,20))
    def on_hover(self, tochno, coords):
        self.hovered_last_time = True
        self.toch_h_last_time = True

        if tochno and self.parent_slot.item != None:
            self.update_tip_coords(coords)
            if not self.tip_gui.is_visible:

                self.tip_gui.open()
                self.tip_gui.transparency_anim()
            
    def disable_hovers(self):
        if self.toch_h_last_time:
            self.toch_h = True

        else:
            self.toch_h = False
         
        self.toch_h_last_time = False
        if self.hovered_last_time: 
            self.hovering = True
            if not self.moving_anim_active and not self.moving_anim_ready:
                self.moving_anim_active = True
                self.moving_anim_bck = False
                self.moving_anim_progress = 0
                self.moving_anim_ready = False
        else:
            self.hovering = False
            if self.tip_gui.is_visible:
                self.tip_gui.backward_transparency_anim(self.tip_gui.close)
    
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
            if self.crs_obj.item == None:
                self.crs_obj.count = 0
            if self.parent_slot.item == None:
                self.parent_slot.count = 0
        else:
            self.parent_slot.count += self.crs_obj.count
            self.crs_obj.item = None
            self.crs_obj.count = 0
        if self.after_click != None: 
            self.after_click()
    def on_right_click(self):
        # get one
        if self.after_click != None: 
            return
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
        screen.blit(self.surface,Utilz.convert_center_to_top_left(self.coordinates.x, self.coordinates.y, self.size[0], self.size[1]))
        if self.parent_slot.count > 1:
            # render count
            
            txt_srf = font_txt.render(str(self.parent_slot.count), False, COUNT_COLOR)
            coords = Utilz.w(self.coordinates.to_tuple(), Utilz.wd(self.size,2))
            coords = Utilz.w(self.coordinates.to_tuple(), (20,5))
            screen.blit(txt_srf,coords)
    def after_draw(self, screen):
        self.tip_gui.draw(screen)
    def blit_item(self, item_mini):
        # coords = Utilz.wd(self.size, 2)
        # coords = Utilz.convert_center_to_top_left(coords[0], coords[1], self.size[0]/2, self.size[1]/2)

        item_rect = item_mini.get_rect()


        item_rect.center = Utilz.wd(self.size, 2)


        srf = self.ore_surf.copy()
        srf.blit(item_mini, item_rect.topleft)

        self.change_parent_surfaces(srf)
    def pack(self,master:Gui,level):
        master.stick_element(self,level) 
        master.subscribe(self,HOVER)
        master.subscribe(self, RIGHT_CLICK)
        master.subscribe(self,LEFT_CLICK)
    def update_color(self, color):
        # things

        self.neat_init(color)
        self.ore_surf = self.or_surf
        if self.parent_slot.item != None:
            self.blit_item(self.parent_slot.item.minimized_for_inv)
    def sync(self,gui_coordinates, splt_val,):
        for label in self.tip_gui_label:
            label.sync_offset()



        self.tip_gui.tick(gui_coordinates, splt_val)
        # self.yes_y(self.y)
        # sync with slotik 
        # print(self.x, self.y)
        if self.last_remembered_item != self.parent_slot.item:
            if self.parent_slot.item != None:
                # UPDATE TIP GUI
                self.tip_gui.elements = []

                 
                lbls = [self.title_label.surface.get_width()]
                for lore_part in self.parent_slot.item.lore:
                    lbl = Label(lore_part, BLACK, 20, "Brownie", (0,0), False,)
                    # lbl.pack(self.tip_gui, -1)
                    lbls.append(lbl.surface.get_width())            
    
                maximum_w = max(lbls) + 50
                maximum_h = len(lbls) * 40

                # , key = lambda label: label.surface.get_width()

                self.tip_frame= Frame(SECOND_INV_COLOR,16,(maximum_w, maximum_h),(0,0), False)
                self.tip_frame.pack(self.tip_gui, 0)
                
                self.title_label = Label(self.parent_slot.item.title, BLACK, 30, "Freedom", (0,0), False, (0,-(maximum_h/2 )+ 20), self.tip_frame)
                self.title_label.pack(self.tip_gui, 1)


                self.tip_gui_label = [self.title_label]
                y = -(maximum_h/2) + 50 
                for lore_part in self.parent_slot.item.lore:
                    lbl = Label(lore_part, BLACK, 20, "Brownie", (0,0), False, (0, y),self.tip_frame)
                    lbl.pack(self.tip_gui, -1)
                    
                    self.tip_gui_label.append(lbl)         
                    y += 30
                lbl = Label(self.parent_slot.item.rarity.name, self.parent_slot.item.rarity.color, 20, "Brownie", (0,0), False, (0, y),self.tip_frame)
                lbl.pack(self.tip_gui, -1)
                self.tip_gui_label.append(lbl) 


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