from gui.gui_module.element import Element
import pygame
from other.utils import Utilz

class Button(Element):
    def __init__(self,color, borders, size, center: tuple, boh) -> None:
        srf = pygame.Surface(size)
        # top_l = Utilz.convert_center_to_top_left(center[0], center[1], size[0], size[1])
        pygame.draw.rect(srf, color, pygame.Rect((0,0), size),0,borders)
        super().__init__(srf, center, boh)
    def get_srf(self):

        return self.surface
    def set_srf(self,r):
        self.surface = r
    def st_or(self, r):
        self.or_surf = r