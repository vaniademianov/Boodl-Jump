from gui.event_types import HOVER, LEFT_CLICK, RIGHT_CLICK
from cons import FPS, HEIGHT, TRANSPARENCY_ANIMATION_SPEED
import pygame

class Gui: 
    def __init__(self) -> None:
        # Requirements: set visible/invisible, is reacting to events, open, close, draw (calls element's draw), events, global hover & click events
        self.is_visible = False
        self.is_reacting = False
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
        for global_event in self.global_events:
            if global_event.evt_type == typ:
                global_event.hold.append(element)
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

        # EVENTS # ['516', '514', '1', '1:', '1', '2:', '1', '3:', '1', '4:', '1', '5:', '1', '6:', '1', '\n']
        # TODO
        # checkin hover
                
        for element in self.elements:
            element.tick()
            if element in self.subscribers[0]:
                element.disable_hovers()
                size = (element.surface.get_width(), element.surface.get_height())
                rectik = pygame.Rect((0,0), size)
                rectik.center = (element.x, element.y)
                rectik2 = pygame.Rect()

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
        