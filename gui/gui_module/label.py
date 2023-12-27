from gui.gui_module.element import Element
from res.resource_manager import resource_manager
from typing import Literal
class Label(Element):
    def __init__(self, text, color, font_size, font: Literal["Brownie", "Freedom"], coordinates: tuple, boh) -> None:
        if font == "Brownie":
            self.font = resource_manager.get_brownie_s(font_size)
        elif font == "Freedom":
            self.font = resource_manager.get_freedom(font_size)
        srf = self.font.render(text, False,color)
        super().__init__(srf, coordinates, boh)