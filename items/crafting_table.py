from item import IItem

class CraftingTable(IItem):
    def __init__(self, parent_slot) -> None:
        super().__init__()
        self.parent = parent_slot
        self.cords_to_place = (0,0)
    def get_slot(self):
        return self.parent
    def on_move(self,player):
        self.cords_to_place = player.rect.center
    def on_right_click(self,*args,**kwargs):
        # Place table
        
    def on_left_click(self,*args,**kwargs):
        pass