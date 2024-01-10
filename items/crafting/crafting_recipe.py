from items.crafting.crafting_ingredient import CraftingIngredient
from gui.gui_module.label import Label

class IICraftingRecipe:
    def __init__(self) -> None:
        self.grid = {CraftingIngredient(None, 0),CraftingIngredient(None, 0),CraftingIngredient(None, 0),CraftingIngredient(None, 0)}
        self.is_strict = False
        self.is_very_strict = False
    def slots_to_ingredients(self, slots):
        return [CraftingIngredient(slot.item, slot.count) for slot in slots]
    def eval(self,slots) -> tuple[int, bool]:
        ing = self.slots_to_ingredients(slots)
        if self.is_very_strict:
            # check if slots strict match grid
            