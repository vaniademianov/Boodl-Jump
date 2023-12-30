from res.resource_manager import resource_manager as rm
import pygame
class Slot:
    def __init__(self, item, act=False) -> None:
        self.item = item

        self.image_act = rm.get_active_slot().copy()
        self.image_unact = rm.get_unactive_slot().copy()
        self.og_image_act = rm.get_active_slot().copy()
        self.og_image_unact = rm.get_unactive_slot().copy()
        self.is_active = act
        self.count = 0
  

        if item is not None:
            rect = item.minimized_for_inv.get_rect()
            rect.center = self.image_act.get_rect().center

            self.image_act.blit(item.minimized_for_inv, rect)
            self.image_unact.blit(item.minimized_for_inv, rect)

        else:
            self.image_act = self.og_image_act.copy()
            self.image_unact = self.og_image_unact.copy()
        self.image = (
            self.image_act.copy() if self.is_active else self.image_unact.copy()
        )

    def update_activity(self, item, act=None):
        if act is None:
            act = self.is_active

        self.item = item
        self.is_active = act

        if item is not None:
            self.item.parent = self
            rect = item.minimized_for_inv.get_rect()
            rect.center = self.image_act.get_rect().center

            self.image_act.blit(item.minimized_for_inv, rect)
            self.image_unact.blit(item.minimized_for_inv, rect)
            if self.is_active:
                self.image = self.image_act.copy()

            else:
                self.image = self.image_unact.copy()
        else:
            self.image_act = self.og_image_act.copy()
            self.image_unact = self.og_image_unact.copy()
            if self.is_active:
                self.image = self.og_image_act

            else:
                self.image = self.og_image_unact

    def get_item(self):
        return self.item

    def draw(self, surf: pygame.Surface, top_left):
        surf.blit(self.image, pygame.Rect(top_left, self.image.get_rect().size))
