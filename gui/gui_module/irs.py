from blocks.crafting_table import MiniCraftingTable
import pygame
from res.resource_manager import resource_manager
from other.utils import Utilz
from other.cons import COUNT_COLOR, font_txt
# from inventory.inventory_gui import gui
scope = resource_manager.get_scope()
class IRS:
    # crs obj should have item, count, and closed to close
    def __init__(self) -> None:
        self.item = None
        self.count = 0
    def draw(self, screen, gui_coordinates):
        # print(f"item is {self.item}")
        # print(self.count,self.item)
        screen.blit(scope, tuple(gui_coordinates))
        if self.item != None:
            item_crd = Utilz.w(tuple(gui_coordinates),Utilz.wd(resource_manager.get_scope().get_size(),4))
            screen.blit(self.item.minimized_for_inv, item_crd)
            if self.count > 1:
                txt_rdr = font_txt.render(str(self.count), False, COUNT_COLOR)
                screen.blit(txt_rdr, Utilz.w(item_crd, (20,5)))
    def closed(self,player, breaked_stuff:pygame.sprite.Group):
        if self.item!= None:
            micr = self.item.mini(player.rect.center)
            breaked_stuff.add(micr)
o_irs = IRS()