from gui.gui_module.element import Element
import pygame
from other.utils import Utilz

class Image(Element):
    def __init__(self,image, center: tuple, boh) -> None:
        super().__init__(image, center, boh)