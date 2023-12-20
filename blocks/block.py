import pygame
from res.resource_manager import ResourceManager
from utils import Utilz
rm  = ResourceManager()

class IBlock(pygame.sprite.Sprite):
    def __init__(self, position, image, durability) -> None:
        super().__init__()
        self.or_image:pygame.Surface = image
        self.image:pygame.Surface = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        # how long to break block in ticks
        self.dur = durability
        self.tiki = 0
        self.STATES = rm.get_breaking_states(self.rect.size)
        self.state = 0
    def draw(self, scr):
        scr.blit(self.image, self.rect)
    def get_pos(self,*args,**kwargs):
        return self.rect.center


    def update(self,is_holding_l_button, player,gui_coordinates):
                
        self.rect.y -= player.y_vel
        if not is_holding_l_button or not self.rect.colliderect(gui_coordinates[0], gui_coordinates[1], 1, 1):
            # reset
            self.state = 0
            self.tiki = 0
            self.image = self.or_image

            
            return
 
        #interaction distance TODO
        elif Utilz.calc_dist(player.rect.centerx,player.rect.centery,self.rect.centerx, self.rect.centerx) < 230:
            self.tiki += 1
            
            if self.tiki > self.dur/len(self.STATES):
                if self.state+1 > len(self.STATES):
                    # over
                    self.on_break()
                    self.kill()
                else:
                    self.tiki = 0
                    
                    self.state+= 1
                    self.image = self.or_image.copy()
                    #update image
                    print(len(self.STATES),self.state)
                    self.image.blit(self.STATES[self.state-1],pygame.Rect(0, 0, self.rect.width, self.rect.height))
    def on_right_click(self,*args,**kwargs):
        raise Exception("NotImplemented error")
    def on_left_click(self):
        # INITIATE BREAKIN
        self.image = self.or_image
        self.image.blit()
    def on_break(self,*args,**kwargs):
        raise Exception("NotImplemented error")