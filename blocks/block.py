import pygame
from res.resource_manager import resource_manager as rm
from other.utils import *
from other.cons import *

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
    @staticmethod
    def spawn(daughter,cords,walls,player,breaked_group,blocks,colliders):
        new_coordinates = Utilz.round_coordinates(cords,player.Y_CHANGE,colliders)

        if Utilz.good_location( new_coordinates,colliders,player.rect.center,player):
            new_block = daughter(new_coordinates,breaked_group)
            blocks.add(new_block)

            colliders.add(new_block)
            return new_block
            
        return None

    def update(self,updatik, player,gui_coordinates):
        is_holding_l_button = updatik.val
        self.rect.y -= player.y_vel
        if not is_holding_l_button or not self.rect.colliderect(grd.get_nearest(gui_coordinates)) or player.controls_locked or Utilz.calc_dist(player.rect.centerx,player.rect.centery,self.rect.centerx, self.rect.centery) > INTERACTION_DISTANCE:
            # reset
            self.state = 0
            self.tiki = 0
            self.image = self.or_image
            
            
            return
 
        else:
            self.tiki += 1
            updatik.val = False
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
                    self.image.blit(self.STATES[self.state-1],pygame.Rect(0, 0, self.rect.width, self.rect.height))
    def on_right_click(self,*args,**kwargs):
        raise Exception("NotImplemented error")
    def on_left_click(self):
        # INITIATE BREAKIN
        raise Exception("NotImplemented error")
    def on_break(self,*args,**kwargs):
        raise Exception("NotImplemented error")

