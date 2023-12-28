import pygame
from cons import RED
class Wall(pygame.sprite.Sprite):
    def __init__(self, coords, size,player, mov=False, color=RED,topik = None,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.player = player
        if topik != None:
            self.rect.top = topik
        self.mov = mov
        self.mov2 = True
        self.riz = 0

    def update(self) -> None:
        if self.mov2 == True:
            self.rect.y -= self.player.y_vel
        if self.mov == True:
            self.riz += self.player.y_vel
        if self.riz <= -300:
            self.mov2 = False
    