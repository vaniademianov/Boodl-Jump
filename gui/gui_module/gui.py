from gui.gui_module.event_types import HOVER, LEFT_CLICK, RIGHT_CLICK
from cons import FPS, HEIGHT, PLAYER_SIZE, TRANSPARENCY_ANIMATION_SPEED
import pygame
from res.resource_manager import resource_manager

class Gui: 
    def __init__(self, active=False) -> None:
        # Requirements: set visible/invisible, is reacting to events, open, close, draw (calls element's draw), events, global hover & click events
        self.is_visible = active
        self.is_reacting = active
        self.elements = []
        self.global_events = [HOVER([]),RIGHT_CLICK([]),LEFT_CLICK([])]
        self.transparency = 0
        self.transparency_anim_progress = 0
        self.tp_anim_active = False
        self.tp_anim_spd = 255/(TRANSPARENCY_ANIMATION_SPEED*FPS)
        self.sli_anim_spd = HEIGHT/(TRANSPARENCY_ANIMATION_SPEED*FPS)
        self.subscribers = [HOVER([]),RIGHT_CLICK([]),LEFT_CLICK([])]
        self.slide_in_anim_active = False
        self.slide_in_anim_progress = 0
        self.slide_out_anim_active = False
        self.slide_out_anim_progress = 0
    def subscribe(self, element, typ):
        for local_evt in self.subscribers:
            if local_evt.evt_type == typ:

                local_evt.hold.append(element)
    def add_listener(self, fnc, typ):
        for global_event in self.global_events:
            if global_event.evt_type == typ:
                global_event.hold.append(fnc)
    def rmv_listener(self, fnc, typ):
        for global_event in self.global_events:
            if global_event.evt_type == typ:
                
                global_event.hold.remove(fnc)
    def open(self):
        self.is_visible = True
        self.is_reacting = True
    def close(self):
        self.is_reacting = False
        self.is_visible = False
    def stick_element(self, element, level):
        self.elements.insert(level, element)
    def draw(self,screen):
        if self.is_visible:
            for element in self.elements:
                element.draw(screen)
    def set_visible(self, visible):
        self.is_visible = visible
    def set_reacting(self, react):
        self.is_reacting = react
    def update_transparency(self,val):

        self.transparency = val
        for element in self.elements: 
            element.alpha(val)

    def transparency_anim(self):
        if not self.tp_anim_active:
            self.update_transparency(0)
            self.transparency_anim_progress = 0
            self.tp_anim_active = True
            if not self.is_visible:
                self.open()
    def tick(self, gui_coordinates:tuple, splt_val):
        if self.tp_anim_active:
            self.transparency_anim_progress += self.tp_anim_spd
            self.update_transparency(self.transparency_anim_progress)
            if self.transparency_anim_progress >= 255:
                self.tp_anim_active = False
                self.transparency_anim_progress = 0
                self.update_transparency(255)
        if self.slide_in_anim_active: 
            self.slide_in_anim_progress += self.sli_anim_spd
            self.update_ys(-self.sli_anim_spd)
            if self.slide_in_anim_progress >= HEIGHT:
                self.slide_in_anim_active = False
                self.update_ys(-(self.slide_in_anim_progress-HEIGHT))
                self.slide_in_anim_progress = 0
        if self.slide_out_anim_active:
            self.slide_in_anim_progress += self.sli_anim_spd
            self.update_ys(self.sli_anim_spd)
            if self.slide_in_anim_progress >= HEIGHT:
                self.slide_out_anim_active = False
                self.update_ys((self.slide_in_anim_progress-HEIGHT))
                self.update_ys(-self.slide_in_anim_progress)
                self.slide_in_anim_progress = 0
                if self.slide_out_finish != None:
                    self.slide_out_finish()

        # EVENTS # ['517', '516', '1', '1:', '1', '2:', '1', '3:', '1', '4:', '1', '5:', '1', '6:', '1', '522', '501', '1']
        if self.is_reacting:

            rectik2 = pygame.Rect(gui_coordinates,resource_manager.get_scope().get_size())
            any_hovered = False
            for element in self.elements:
                element.tick()
                
                if element in self.subscribers[0].hold:

                    element.disable_hovers()
                    size = element.surface.get_size()
                    rectik = pygame.Rect((0,0), size)
                    rectik.center = (element.x, element.y)
                    
                    if rectik.colliderect(rectik2):
                        element.on_hover()
                        any_hovered = True
                    else:
                        element.hovers_disabled()
            if any_hovered:
                self.global_events[0].call()
            # CLICK
            any_r_clicked = False
            any_l_clicked = False
            left_button = (splt_val[10] == "0")
            right_button = (splt_val[8] == "0")
            for element in self.elements:
                if element in self.subscribers[1].hold and right_button:
                    size = element.surface.get_size()
                    rectik = pygame.Rect((0,0), size)
                    rectik.center = (element.x, element.y)
                
                    if rectik.colliderect(rectik2):
                        element.on_right_click()
                        any_r_clicked = True
                if element in self.subscribers[2].hold and left_button:
                    size = element.surface.get_size()
                    rectik = pygame.Rect((0,0), size)
                    rectik.center = (element.x, element.y)
                
                    if rectik.colliderect(rectik2):
                        element.on_left_click()
                        any_l_clicked = True
            if any_r_clicked: 
                self.global_events[1].call()
            if any_l_clicked:
                self.global_events[2].call()
    def update_ys(self, value):
        for element in self.elements:
            element.y+= value

    def slide_in_anim(self):
        if not self.slide_in_anim_active:
            self.update_ys(HEIGHT)
            self.slide_in_anim_active = True
            self.slide_in_anim_progress = 0
            if not self.is_visible:
                self.open()
        
    def slide_out_anim(self,finish=None):

        if not self.slide_in_anim_active:
            self.slide_out_anim_active = True
            self.slide_out_anim_progress = 0
            if not self.is_visible: 
                self.open()
        
        self.slide_out_finish = finish
    def close_animated(self):
        self.slide_out_anim(finish=self.close)
        