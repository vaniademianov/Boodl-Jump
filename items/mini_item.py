import pygame
from other.utils import Utilz
from other.cons import *
from res.audio.mixer import mx
class IIMiniItem(pygame.sprite.Sprite):
    def __init__(self, cords, image, parent) -> None:
        super().__init__()

        self.rect = image.get_rect()
        self.rect.center = cords
        self.or_rect_center = list(cords)
        self.delay = 0
        self.parent = parent
        self.pickup_time = 0.60
        self.path = None
        self.original_image = image.copy()
        self.rotation_speed = 4
        self.image = self.original_image.copy()  # Assign a copy of the original image
        self.angle = 0
        self.anti_down = False
    def calc_path(self, a, b, time):
        direction = pygame.math.Vector2(b) - pygame.math.Vector2(a)
        step = direction / time
        path = [(int(a[0] + step[0] * i), int(a[1] + step[1] * i)) for i in range(int(time) + 1)]
        path.reverse()
        return path

    def update(self, player, colliders: pygame.sprite.Group):
        self.rect.y -= player.y_vel
        self.or_rect_center[1] -= player.y_vel
        # if self.anti_down:
        #     self.or_rect_center[1] -= 8
        #     self.rect.centery -= 8
        if pygame.sprite.spritecollideany(self, colliders) == None and self.rect.width >0:

            self.or_rect_center[1] += 2
            self.rect.centery += 2

        dist = Utilz.calc_dist(player.rect.centerx, player.rect.centery, self.rect.centerx, self.rect.centery)

        if dist < INTERACTION_DISTANCE // 3:
            self.delay = FPS * self.pickup_time if self.delay <= 0 else self.delay
            if self.delay == 1:
                ad = player.inv.add_to_inventory(self.parent(None), 1)
                mx.play_looting(0.3)
                if ad:
                    self.kill()
            self.path = self.calc_path(self.rect.center, player.rect.center, FPS * self.pickup_time)

            if self.path is not None:
                self.rect.center = self.path[int(self.delay)]
            self.delay -= 1
        else:
            self.delay = 0
            self.path = None
            self.rect.center = self.or_rect_center

        if self.rect.center[0] == self.or_rect_center[0] and self.rect.center[1] == self.or_rect_center[1]:
            self.angle += self.rotation_speed
            ang = int(((90 - self.angle) / 90) * self.original_image.get_width())
            if ang <= 0:
                angr = -ang
            else:
                angr = ang
            # self.anti_down = False
            if ang < -self.original_image.get_width():
                self.image = self.original_image.copy()

                self.rect = self.image.get_rect()
                self.rect.center= self.or_rect_center

                self.angle = 0
            
            self.image = pygame.transform.scale(self.original_image, (angr, self.image.get_height()))
            self.rect = self.image.get_rect()
            self.rect.center= self.or_rect_center

        else:

            self.image = self.original_image.copy()  # Use a copy of the original image
