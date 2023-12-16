from block import IBlock
from res.resource_manager import ResourceManager
from utils import Utilz
rm = ResourceManager()
class CraftingTable(IBlock):
    def __init__(self, pos) -> None:
        img = rm.get_crafting_table(25,25)
        super().__init__(pos,img, 60*3)

        
    def spawn(cords):
        new_coordinates = Utilz.round_coordinates(cords)
        if Utilz.good_location(new_coordinates):
            new_block = CraftingTable(new_coordinates)
            return new_block
        return None
    def on_right_click(self,):
        # open gui
        pass
    def on_break(self):
        pass
