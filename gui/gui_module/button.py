from gui.gui_module.element import Element
import pygame
from other.utils import Utilz

class Button(Element):
    def __init__(self,color, borders, size, center: tuple, boh,custom_borders = None) -> None:
        srf = pygame.Surface(size,pygame.SRCALPHA)
        self.borders = borders
        self.custom_borders = custom_borders
        self.size = size
        # top_l = Utilz.convert_center_to_top_left(center[0], center[1], size[0], size[1])
        if custom_borders != None:
            pygame.draw.rect(srf, color, pygame.Rect((0,0), size),0,-1, custom_borders[0], custom_borders[1], custom_borders[2],custom_borders[3])
        else:
            pygame.draw.rect(srf, color, pygame.Rect((0,0), size),0,borders)
        super().__init__(srf, center, boh)
    def get_srf(self):

        return self.surface
    def neat_init(self, color):
        srf = pygame.Surface(self.size,pygame.SRCALPHA)
        # top_l = Utilz.convert_center_to_top_left(center[0], center[1], size[0], size[1])
        if self.custom_borders != None:
            pygame.draw.rect(srf, color, pygame.Rect((0,0), self.size),0,-1, self.custom_borders[0], self.custom_borders[1], self.custom_borders[2],self.custom_borders[3])
        else:
            pygame.draw.rect(srf, color, pygame.Rect((0,0), self.size),0,self.borders)
        self.surface = srf
        self.or_surf = srf
    def set_srf(self,r):
        self.surface = r
    def st_or(self, r):
        self.or_surf = r