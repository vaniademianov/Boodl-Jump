from dataclasses import dataclass
@dataclass
class CraftingIngredient:
    def __init__(self,i, c):
        self.item = i 
        self.count = c 
    item = None
    count = None
    def __eq__(self, __value: object) -> bool:
        if __value == None:
            return False 
        if __value and self.item and self.count != None:
            return __value.item.title == self.item.title and __value.count >= self.count 
        else:
            return False
    def __floordiv__(self, __value:object) -> int: 
        return self.count//__value.count 
    def __repr__(self) -> str:
        print(self.item)
        if self.item != None:
            return "CI"+self.item.title 
        return "CI"