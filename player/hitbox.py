import pygame
from typing import Any
import random
from cons import WHITE, BLUE, GREEN
from cons import RED
from utils import Utilz
class Cub(pygame.sprite.Sprite):
    def __init__(self, size, ofs, hitty,colliders):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(random.choice([RED, WHITE, BLUE, GREEN]))
        self.rect = self.image.get_rect()
        self.rect.topleft = Utilz.w(hitty.rect.topleft, ofs)
        self.hitty = hitty
        self.ofs = ofs
        self.colliders = colliders
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.topleft = Utilz.w(self.hitty.rect.topleft, self.ofs)

    def sync(self, *args: Any, **kwargs: Any) -> None:
        self.rect.topleft = Utilz.w(self.hitty.rect.topleft, self.ofs)

    def touching(self) -> bool:
        return pygame.sprite.spritecollideany(self, self.colliders) != None
class Hitty(pygame.sprite.Sprite):
    def __init__(self, colliders, size, coords, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(RED)
        self.og_surf = self.image
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.player = player
        self.ii = 20
        self.angle = 0
        self.change_angle = 0
        self.colliders = colliders
    def touching(self) -> bool:
        return pygame.sprite.spritecollideany(self, self.colliders) != None

    def update(self, classi) -> None:
        self.change_angle = -self.player.x_vel

        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y

    def check_left(self):
        self.rect.centerx -= self.ii
        if self.touching():
            self.rect.centerx += self.ii
            return False
        else:
            self.rect.centerx += self.ii
            return True

    def check_right(self):
        self.rect.centerx += self.ii
        if self.touching():
            self.rect.centerx -= self.ii
            return False
        else:
            self.rect.centerx -= self.ii
            return True

    def check_up(self):
        self.rect.centery -= self.ii
        if self.touching():
            self.rect.centery += self.ii
            return False
        else:
            self.rect.centery += self.ii
            return True

    def check_down(self):
        self.rect.centery += self.ii
        if self.touching():
            self.rect.centery -= self.ii
            return False
        else:
            self.rect.centery -= self.ii
            return True

    def suuper_check_x(self, dist):
        bt_ii = self.ii

        val = False
        self.ii = dist
        val = self.check_right()

        self.ii = bt_ii

        return val

    def suuper_check_y(self, dist):
        bt_ii = self.ii

        val = False
        self.ii = dist
        val = self.check_down()
        self.ii = bt_ii
        return val
