from gui.gui_module.event_types import HOVER, LEFT_CLICK, RIGHT_CLICK
from other.cons import (FPS, HEIGHT, PLAYER_SIZE, SLIDE_IN_ANIMATION_SPEED,
    TRANSPARENCY_ANIMATION_SPEED, WIDTH)
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
        self.sli_anim_spd = HEIGHT/(SLIDE_IN_ANIMATION_SPEED*FPS)
        self.subscribers = [HOVER([]),RIGHT_CLICK([]),LEFT_CLICK([])]
        self.slide_in_anim_active = False
        self.slide_in_anim_progress = 0
        self.slide_out_anim_active = False
        self.slide_out_anim_progress = 0
        self.backward_transparency_anim_active = False
        self.left_to_right_slide_anim_active = False
        self.left_to_right_slide_anim_progress = 0
        self.left_to_right_slide_anim_speed = WIDTH//(SLIDE_IN_ANIMATION_SPEED*FPS)
        self.left_to_right_slide_anim_on_end = None 
        self.right_to_left_slide_anim_active = False
        self.left_to_right_halfed = False
        self.right_to_left_halfed = False
        self.right_to_left_slide_anim_progress = 0
        self.right_click_delay = 0
        self.left_click_delay = 0
        
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
            for element in self.elements:
                element.after_draw(screen) 
    def set_visible(self, visible):
        self.is_visible = visible
    def set_reacting(self, react):
        self.is_reacting = react
    def update_transparency(self,val):

        self.transparency = val
        for element in self.elements: 
            element.alpha(val)
    def update_xs(self, value):
        for element in self.elements:
            element.coordinates.x+= int(value)
    def left_to_right_slide_anim(self, on_end=None,halfed=False):
        if not self.left_to_right_slide_anim_active:
            self.left_to_right_halfed = halfed
            self.left_to_right_slide_anim_progress =0
            self.left_to_right_slide_anim_active = True
            self.left_to_right_slide_anim_on_end = on_end
            if not self.is_visible:
                self.open()
    def right_to_left_slide_anim(self,halfed):
        if not self.right_to_left_slide_anim_active:
            self.right_left_to_halfed = halfed
            self.right_to_left_slide_anim_progress_slide_anim_progress = 0
            self.right_to_left_slide_anim_active = True
            self.update_xs(WIDTH)
            if not self.is_visible:
                self.open()
    def transparency_anim(self):
        if not self.tp_anim_active:
            self.update_transparency(0)
            self.transparency_anim_progress = 0
            self.tp_anim_active = True
            if not self.is_visible:
                self.open()
    def backward_transparency_anim(self,on_f=None):
        if not self.backward_transparency_anim_active:
            self.update_transparency(255)
            self.backward_transparency_anim_progress = 255
            self.backward_transparency_anim_active = True
            self.bw_on_finish = on_f
            if not self.is_visible:
                self.open()
    def tick(self, gui_coordinates:tuple, splt_val):
        if self.left_to_right_slide_anim_active:
            self.left_to_right_slide_anim_progress += self.left_to_right_slide_anim_speed
            self.update_xs(self.left_to_right_slide_anim_speed)
            if self.left_to_right_slide_anim_progress >= WIDTH/(2 if self.left_to_right_halfed else 1):
                self.left_to_right_slide_anim_active = False

                self.update_xs(-self.left_to_right_slide_anim_progress)
                if self.left_to_right_slide_anim_on_end != None:
                    self.left_to_right_slide_anim_on_end()
                self.left_to_right_slide_anim_progress = 0
        if self.right_to_left_slide_anim_active:
            self.right_to_left_slide_anim_progress += self.left_to_right_slide_anim_speed
            self.update_xs(-self.left_to_right_slide_anim_speed)
            
            if self.right_to_left_slide_anim_progress >= WIDTH/(2 if self.right_left_to_halfed else 1):
                self.update_xs(-self.left_to_right_slide_anim_progress)
                self.right_to_left_slide_anim_active = False
                self.right_to_left_slide_anim_progress = 0
        if self.tp_anim_active:
            self.transparency_anim_progress += self.tp_anim_spd
            self.update_transparency(self.transparency_anim_progress)
            if self.transparency_anim_progress >= 255:
                self.tp_anim_active = False
                self.transparency_anim_progress = 0
                self.update_transparency(255)
        if self.backward_transparency_anim_active:
            self.backward_transparency_anim_progress -= self.tp_anim_spd
            self.update_transparency(self.backward_transparency_anim_progress)
            if self.backward_transparency_anim_progress <= 0:
                self.backward_transparency_anim_active = False
                self.update_transparency(0)
                self.backward_transparency_anim_progress = 0
                if self.bw_on_finish != None:
                    self.bw_on_finish()
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
        if self.left_click_delay > 0:
            self.left_click_delay -= 1
        if self.right_click_delay > 0:
            self.right_click_delay -= 1
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
                    rectik.center = (element.coordinates.x, element.coordinates.y)
                    
                    if rectik.colliderect(rectik2):
                        # print("HOVERER", element)
                        # check is super
                        tochno = rectik.collidepoint(gui_coordinates)
                        element.on_hover(tochno,gui_coordinates)
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
                # print(self.right_click_delay ,self.left_click_delay)
                if element in self.subscribers[1].hold and right_button and int(self.right_click_delay) <= 0:
                    
                    size = element.surface.get_size()
                    rectik = pygame.Rect((0,0), size)
                    rectik.center = (element.coordinates.x, element.coordinates.y)
                    
                    if rectik.colliderect(rectik2):
                       
                        self.right_click_delay = FPS/5
                        element.on_right_click()
                        any_r_clicked = True
                        break
                if element in self.subscribers[2].hold and left_button and int(self.left_click_delay) <= 0:
                    
                    size = element.surface.get_size()
                    rectik = pygame.Rect((0,0), size)
                    rectik.center = (element.coordinates.x, element.coordinates.y)
                    
                    if rectik.colliderect(rectik2):
                        
                        self.left_click_delay = FPS/5

                        element.on_left_click()
                        any_l_clicked = True
                        break
            if any_r_clicked: 
                self.global_events[1].call()
            if any_l_clicked:
                self.global_events[2].call()
    def update_ys(self, value):
        for element in self.elements:
 
            element.coordinates.y+= int(value)

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
        