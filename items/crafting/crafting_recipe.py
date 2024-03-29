from items.crafting.crafting_ingredient import CraftingIngredient
from gui.gui_module.label import Label
from items.crafting.grid_types import grid2x2
from items.item import IItem
from inventory.slot import Slot
from other.utils import Utilz


class IICraftingRecipe:
    def __init__(self, item, grid, gridtype, strictness_level) -> None:
        self.grid_type = gridtype

        self.grid = list(Utilz.split_list(grid, gridtype.lines))
        self.is_strict = strictness_level == "strict"
        self.is_very_strict = strictness_level == "very_strict"
        self.itm = item

    def slots_to_ingredients(self, slots, w):


        return list(
            Utilz.split_list(
                [CraftingIngredient(slot.item, slot.count) for slot in slots], w
            )
        ), list(Utilz.split_list(slots, w))

    def eval(self, slots, width):
        ing, slotd = self.slots_to_ingredients(slots, width)
        if self.is_very_strict:
            # check if slots strict match grid
            if sum(map(lambda x: sum(x), ing)) < sum(map(lambda x: sum(x), self.grid)):
                return (CraftingIngredient(None, 0), None, None)
            # SELF.GRID = RECIPE
            # ING = ITEMS
            counts = []
            creatable = True
            for i in range(i, len(self.grid)):
                for j in range(len(self.grid[i])):
                    if not (self.grid[i][j] == ing[i][j]):
                        creatable = False
                        break
                    else:
                        counts.append(ing[i][j] // self.grid[i][j])
                if not creatable:
                    break
            items_we_can_create = min(counts)
            if creatable and items_we_can_create <= 0:
                print("Something went wrong during comparison")
                return (CraftingIngredient(None, 0), None, None)
            if creatable:
                # If we can craft the object, return it
                return (
                    CraftingIngredient(self.itm(None), items_we_can_create),
                    slotd,
                    counts,
                )
        elif self.is_strict:
            if len(ing) < len(self.grid):
                return (CraftingIngredient(None, 0), None, None)
            for i2 in range(0, len(ing) - len(self.grid) + 1):
                for j2 in range(0, len(ing[i2]) - len(self.grid[i2]) + 1):
                    counts = []
                    creatable = True
                    for i in range(i, len(self.grid)):
                        for j in range(len(self.grid[i])):
                            if not (self.grid[i][j] == ing[i][j]):
                                creatable = False
                                break
                            else:
                                counts.append(ing[i][j] // self.grid[i][j])
                        if not creatable:
                            break
                    if creatable:
                        break
                if creatable:
                    break

            items_we_can_create = min(counts)
            if creatable and items_we_can_create <= 0:
                print("Something went wrong during comparison")
                return (CraftingIngredient(None, 0), None, None)
            if creatable:
                # If we can craft the object, return it
                return (
                    CraftingIngredient(self.itm(), items_we_can_create),
                    slotd,
                    counts,
                )
        else:
            # Check if all items are same
            counts = []
            ing_flat = [item for sublist in ing for item in sublist]
            creatable = True

            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    # print(self.grid[i][j], ing_flat)
                    if self.grid[i][j] in ing_flat:

                        occur = ing_flat.pop(ing_flat.index(self.grid[i][j]))

                        # if error then its not finiding it
                        counts.append(occur // self.grid[i][j])

                    else:
                        # print("not ok :(")
                        creatable = False
                        break
                if not creatable:
                    break
            items_we_can_create=0
            if len(counts) > 0:
                items_we_can_create = min(counts)
            
            if creatable and items_we_can_create <= 0:
                print("Something went wrong during comparison")
                return (CraftingIngredient(None, 0), None, None)
            if creatable:
                print("creatable")
                # If we can craft the object, return it
                return (
                    CraftingIngredient(self.itm(None), items_we_can_create),
                    slotd,
                    counts,
                )

    def take_it(self, slots: list[Slot, Slot, Slot, Slot], w) -> CraftingIngredient:
        result, slotd, counts = self.eval(slots, w)
        # print(result, slotd, counts)
        # assert len(slotd) == len(counts)
        if result.item != None:
            # can craft the item
            slotd = [j for sub in slotd for j in sub]
            for i in range(len(slotd)):
                count_we_should_take_from_slt = counts[i]
                slot = slotd[i]
                slot.count -= count_we_should_take_from_slt
                if slot.count <= 0:
                    slot.item = None
                    slot.count = 0
        return result
