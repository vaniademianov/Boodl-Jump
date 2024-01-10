from dataclasses import dataclass
@dataclass
class CraftingIngredient:
    def __init__(i, c):
        item = i 
        count = c 
    item = None
    count = None
    def __eq__(self, __value: object) -> bool:
        return __value.item == self.item and __value.count >= self.count 
    