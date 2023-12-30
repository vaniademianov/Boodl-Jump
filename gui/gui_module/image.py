from gui.gui_module.element import Element
import pygame
from other.utils import Utilz
from other.coordinates import Coordinates

class Image(Element):
    def __init__(self,image, center,sync,  boh) -> None:
        self.coordz = center
        self.syncer = sync
        super().__init__(image, center.to_tuple(), boh)
    def sync(self):
        if self.syncer:
            self.coordinates = self.coordz