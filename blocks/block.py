import pygame
from res.resource_manager import ResourceManager
from utils import Utilz
rm  = ResourceManager()

class IBlock(pygame.sprite.Sprite):
    def __init__(self, position, image, durability) -> None:
        self.rect = position
        self.or_image:pygame.Surface = image
        self.image:pygame.Surface = image
        # how long to break block in ticks
        self.dur = durability
        self.tiki = 0
        self.STATES = rm.get_breaking_states(self.rect.size)
        self.state = 0
    def draw(self, scr):
        scr.blit(self.image, self.rect)
    def get_pos(self,*args,**kwargs):
        return self.rect.center


    def tick(self,is_holding_l_button, player):
                
        self.rect.y -= player.y_vel
        if not is_holding_l_button:
            # reset
            self.state = 0
            self.tiki = 0
            self.image = self.or_image
            return
        else:
            tiki += 1
            if tiki > self.dur/len(self.STATES):
                if self.state + 1 > len(self.STATES):
                    # over
                    self.on_break()
                    self.kill()
                self.tiki = 0
                
                self.state+= 1
                self.image = self.or_image
                #update image
                self.image = self.image.blit(self.STATES[self.state-1],pygame.Rect(0, 0, self.rect.width, self.rect.height))
    def on_right_click(self,*args,**kwargs):
        raise Exception("NotImplemented error")
    def on_left_click(self):
        # INITIATE BREAKIN
        self.image = self.or_image
        self.image.blit()
    def on_break(self,*args,**kwargs):
        raise Exception("NotImplemented error")