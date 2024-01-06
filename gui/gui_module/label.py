from gui.gui_module.element import Element
from res.resource_manager import resource_manager
from typing import Literal
from other.utils import Utilz
from other.coordinates import Coordinates
class Label(Element):
    def __init__(self, text, color, font_size, font: Literal["Brownie", "Freedom"], coordinates: tuple, boh,offset = None,parent_to_offset_from = None) -> None:
        if font == "Brownie":
            self.font = resource_manager.get_brownie_s(font_size)
        elif font == "Freedom":
            self.font = resource_manager.get_freedom(font_size)
        self.text = text 
        self.color = color 
        self.offset = offset
        self.parent_offset =parent_to_offset_from
        srf = self.font.render(text, False,color)
        super().__init__(srf, coordinates, boh)
    def sync_offset(self):
        if self.parent_offset != None:

            self.coordinates_t = Utilz.w(self.parent_offset.coordinates.to_tuple(), self.offset)
            self.coordinates = Coordinates(self.coordinates_t[0], self.coordinates_t[1])
    def upd_text(self, new_text):
        self.text = new_text 
        srf = self.font.render(self.text, False,self.color)
        self.surface = srf.copy()
        self.or_surf = srf.copy()
    def neat_init(self):
        srf = self.font.render(self.text, False,self.color)
        self.surface = srf.copy()
        self.or_surf = srf.copy()
        return srf