import pygame
from utils import Utilz
from gui.gui_module.event_types import HOVER
from cons import FPS, HEIGHT, HOVER_ANIMATION_SPEED
from gui.gui_module.gui import Gui
pygame.display.set_mode()
class Element:
    def __init__(self,srf, coordinates:tuple,boh) -> None:
        # do studff
        self.surface:pygame.Surface = srf
        self.surface.convert_alpha()
        self.or_surf = self.surface.copy()
        self.x, self.y = coordinates
        self.hover = False
        self.hovering_animation_active = False
        self.hovering_animation_progress = 0
        self.big_on_hover = boh
        self.vidsotok_zb = 5
        self.hovering_animation_spd = HOVER_ANIMATION_SPEED*6
        self.slod = False
        self.back_hover_anim_active = False
    def pack(self,master:Gui,level):
        master.stick_element(self,level) 
        
        # print("SUBBED")
        master.subscribe(self,HOVER)
        
    def alpha(self,value):
        self.surface.set_alpha(value)
    def on_hover(self):
        # print("HOVERED")
        # activate animation
        if self.big_on_hover and not self.slod:
            self.hover = True
            self.hovering_animation_active = True
            # self.hovering_animation_progress = 0
    def back_hover_anim(self):
        self.back_hover_anim_active = True
        
    def disable_hovers(self):

        if not self.hovering_animation_active:

            self.slod2 = True
    def hovers_disabled(self):
        if self.hover:
            # print(self.slod)
            # run anim

            if self.slod2 and self.slod:

                self.back_hover_anim()
    def make_bigger(self, valuex, valuey):
        # assert valuex % 2 == 0
        # assert valuey % 2 == 0
        self.x += valuex / 4
        self.y += valuey / 4

        self.surface = self.resizik(self.surface,valuex, valuey)
        
    def resizik(self,surf:pygame.Surface, valx, valy):
        # print((surf.get_width()+valx, surf.get_height()+valy))
        l = pygame.transform.smoothscale(surf, (surf.get_width()+valx, surf.get_height()+valy)).copy()
        return l
    def tick(self):

        if self.back_hover_anim_active:

            self.hovering_animation_progress-= self.hovering_animation_spd
            
            self.make_bigger(-(self.surface.get_height()/100*self.hovering_animation_spd),-(self.surface.get_height()/100*self.hovering_animation_spd))
            if self.hovering_animation_progress <= 0:
                self.hovering_animation_active = False
                self.back_hover_anim_active = False
                self.hovering_animation_progress = 0
                self.surface= self.or_surf.copy()
                self.slod = False
        elif self.hovering_animation_active:

            self.hovering_animation_progress+= self.hovering_animation_spd
            
            self.make_bigger((self.surface.get_height()/100*self.hovering_animation_spd),(self.surface.get_height()/100*self.hovering_animation_spd))
            # print(FPS*HOVER_ANIMATION_SPEED, self.hovering_animation_progress, self.hovering_animation_spd)
            if self.hovering_animation_progress >= FPS*HOVER_ANIMATION_SPEED:
                self.hovering_animation_active = False

                self.slod = True

    def draw(self, screen:pygame.Surface):
        
        screen.blit(self.surface, pygame.Rect(Utilz.convert_center_to_top_left(self.x,self.y, self.surface.get_width(),self.surface.get_height()), self.surface.get_size()))