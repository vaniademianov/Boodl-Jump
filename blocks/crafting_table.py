from blocks.block import IBlock
from res.resource_manager import ResourceManager
from utils import Utilz
from items.item import IItem
import pygame
pygame.init()
rm = ResourceManager()

class CraftingTable_block(IBlock):
    def __init__(self, pos, breaked_group) -> None:
        img = rm.get_crafting_table((48,48))
        self.breaked = breaked_group
        # fps * 3
        super().__init__(pos,img, 30*2)

    @staticmethod
    def spawn(cords,walls,player_loc,breaked_group,blocks,colliders):
        new_coordinates = Utilz.round_coordinates(cords,colliders)
    
        if Utilz.good_location(new_coordinates,walls,player_loc):
            new_block = CraftingTable_block(new_coordinates,breaked_group)
            blocks.add(new_block)

            colliders.add(new_block)

            return new_block
        return None
    def on_right_click(self,):
        # open gui
        pass
    def on_break(self):
        # summon mini crafting table
        self.breaked.add(MiniCraftingTable(self.rect.center))

class MiniCraftingTable(pygame.sprite.Sprite):
    def __init__(self,cords) -> None:
        super().__init__()
        self.parent = CraftingTable
        self.image = rm.get_crafting_table((16,16))
        self.rect = self.image.get_rect()
        self.rect.center = cords 
        self.delay = 0
    def update(self, player, colliders:pygame.sprite.Group):
        if not pygame.sprite.spritecollideany(self, colliders):
            self.rect.centery += 2
        # check is player near and give block to them
        dist = Utilz.calc_dist(player.rect.centerx,player.rect.centery,self.rect.centerx, self.rect.centery)
        if dist < 100:
            self.delay = 100 if self.delay <= 0 else self.delay
            if self.delay == 1:
                ad = player.inv.add_to_inventory(self.parent(None),1)
                if ad:
                    self.kill()
            self.delay -= 1
        else:
            self.delay = 0

class CraftingTable(IItem):
    def __init__(self, parent_slot) -> None:
        super().__init__()
        self.parent = parent_slot
        self.minimized_for_inv = rm.get_crafting_table((32,32))
        self.cords_to_place = (0,0)
    def get_slot(self):
        return self.parent
    def on_move(self,player):
        self.cords_to_place = player.rect.center
    def on_right_click(self,cordi, walls,breaked_group, blocks,colliders):
        # Place table
        
        CraftingTable_block.spawn(cordi, walls,self.cords_to_place,breaked_group,blocks,colliders)
        self.parent.count -= 1
        if self.parent.count <= 0:
            # self, item, act
            self.parent.update_activity(None)
    def on_left_click(self,*args,**kwargs):
        pass
