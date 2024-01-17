from dataclasses import dataclass
@dataclass
class CraftingIngredient:
    def __init__(self,i, c):
        self.item = i 
        self.count = c 
    item = None
    count = None
    def __eq__(self, __value: object) -> bool:
        return __value.item == self.item and __value.count >= self.count 
    def __floordiv__(self, __value:object) -> int: 
        return self.count//__value.count 