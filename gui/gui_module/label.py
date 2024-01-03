from gui.gui_module.element import Element
from res.resource_manager import resource_manager
from typing import Literal
class Label(Element):
    def __init__(self, text, color, font_size, font: Literal["Brownie", "Freedom"], coordinates: tuple, boh) -> None:
        if font == "Brownie":
            self.font = resource_manager.get_brownie_s(font_size)
        elif font == "Freedom":
            self.font = resource_manager.get_freedom(font_size)
        self.text = text 
        self.color = color 
        srf = self.font.render(text, False,color)
        super().__init__(srf, coordinates, boh)
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