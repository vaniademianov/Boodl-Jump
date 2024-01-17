from items.crafting.crafting_ingredient import CraftingIngredient


class gridBase:
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    def get_slots(self):
        res = []
        for i in range(self.lines ):
            r = []
            for j in range(self.columns):
                r.append(CraftingIngredient(None, 1))
            res.append(r)
        return res 

class grid2x2(gridBase):
    name = "2x2"
    lines = 2
    columns = 2
    slots_count = lines*columns
class grid3x3(gridBase):
    name = "3x3"
    lines = 3
    columns = 3
    slots_count = lines*columns
 