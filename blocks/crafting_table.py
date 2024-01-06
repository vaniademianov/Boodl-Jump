from blocks.block import IBlock
from res.resource_manager import ResourceManager
from other.utils import *
from items.item import IItem
import pygame
from other.cons import *
from items.mini_item import IIMiniItem
from items.rarity import Rarity

pygame.init()
rm = ResourceManager()

class CraftingTable_block(IBlock):
    def __init__(self, pos, breaked_group) -> None:
        self.img = rm.get_crafting_table((50,50))
        self.breaked = breaked_group
        # fps * 3
        super().__init__(pos,self.img, FPS*2)


    def on_right_click(self,):
        # open gui
        pass
    def on_break(self):
        # summon mini crafting table
        self.breaked.add(MiniCraftingTable(self.rect.center))

class MiniCraftingTable(IIMiniItem):
    def __init__(self,cords) -> None:
        
        self.parent = CraftingTable
        self.image = rm.get_crafting_table((16,16))
        super().__init__(cords, self.image, self.parent)
class CraftingTable(IItem):
    def __init__(self, parent_slot) -> None:
        super().__init__()
        self.parent = parent_slot
        self.is_block = True
        self.blocky_image = rm.get_crafting_table((50,50))
        self.minimized_for_inv = rm.get_crafting_table((32,32))
        self.player = None
        self.mini = MiniCraftingTable
        self.title = "Crafting Table"
        self.lore = ["Ancient technology", "Some people say even our","grandgrandgrandgrandgrand","parents used it.","o","o","o","o","o","o","o","o","o","o","o","o","o","o"]
        self.rarity = Rarity.COMMON  
    def get_slot(self):
        return self.parent
    def on_move(self,player):
        self.player = player
    def on_right_click(self,cordi, walls,breaked_group, blocks,colliders):
        # Place table
        new_block = CraftingTable_block.spawn(CraftingTable_block, cordi, walls,self.player,breaked_group,blocks,colliders)
        if new_block != None:
            self.parent.count -= 1
            if self.parent.count <= 0:
                # self, item, act
                self.parent.update_activity(item=None,act=None)



    def on_left_click(self,*args,**kwargs):
        pass
