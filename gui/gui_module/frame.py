from gui.gui_module.element import Element
import pygame
from other.utils import Utilz


class Frame(Element):
    def __init__(self,color, borders, size, center: tuple, boh,sep_borders = None) -> None:
        srf = pygame.Surface(size)
        # top_l = Utilz.convert_center_to_top_left(center[0], center[1], size[0], size[1])
        if sep_borders == None:
            pygame.draw.rect(srf, color, pygame.Rect((0,0), size),0,borders)
        else:
            pygame.draw.rect(srf, color, pygame.Rect((0,0), size),0,border_top_left_radius=sep_borders[0], border_top_right_radius=sep_borders[1], border_bottom_left_radius=sep_borders[2], border_bottom_right_radius=sep_borders[3])
        super().__init__(srf, center, boh)