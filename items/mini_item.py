import pygame
from cons import *
from utils import Utilz
pygame.init()

class IIMiniItem(pygame.sprite.Sprite):
    def __init__(self,cords,image,parent) -> None:
        super().__init__()
    
        self.rect = image.get_rect()
        self.rect.center = cords 
        self.or_rect_center = list(cords)
        self.delay = 0
        self.parent = parent
        self.pickup_time =  0.60
        self.path = None
    def calc_path(self, a, b, time):

        direction = pygame.math.Vector2(b) - pygame.math.Vector2(a)

        step = direction / time
        path = [(int(a[0] + step[0] * i), int(a[1] + step[1] * i)) for i in range(int(time) + 1)]
        path.reverse()

        return path
    def update(self, player, colliders:pygame.sprite.Group):
        self.rect.y -= player.y_vel
        self.or_rect_center[1] -= player.y_vel
        if not pygame.sprite.spritecollideany(self, colliders):
            self.or_rect_center[1] += 2
            self.rect.centery += 2
        # check is player near and give block to them
        dist = Utilz.calc_dist(player.rect.centerx,player.rect.centery,self.rect.centerx, self.rect.centery)
        # interaction distance
        if dist < INTERACTION_DISTANCE//3:
            self.delay = FPS*self.pickup_time if self.delay <= 0 else self.delay
            if self.delay == 1:
                ad = player.inv.add_to_inventory(self.parent(None),1)
                if ad:
                    self.kill()
            elif self.delay == FPS*self.pickup_time:
                self.path = self.calc_path(self.rect.center, player.rect.center,FPS*self.pickup_time)
            if self.path != None:
                self.rect.center = self.path[int(self.delay)]
            self.delay -= 1
        else:
            self.delay = 0
            self.path = None
            self.rect.center = self.or_rect_center