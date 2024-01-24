from items.crafting.crafting_recipe import IICraftingRecipe
from items.crafting.grid_types import grid2x2
from blocks.crafting_table import CraftingTable
from items.crafting.crafting_ingredient import CraftingIngredient

class Recipe(IICraftingRecipe):
    def __init__(self) -> None:
        self.strictness_level = ""
        self.grid_type = grid2x2
        self.item = CraftingTable
        self.grid = [CraftingIngredient(CraftingTable(None), 1), CraftingIngredient(CraftingTable(None), 1), CraftingIngredient(CraftingTable(None), 1),CraftingIngredient(CraftingTable(None), 1)]
        super().__init__(self.item, self.grid, self.grid_type, self.strictness_level)

