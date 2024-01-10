from inventory.slot import Slot
from other.cons import FPS
from other.cons import COUNT_COLOR, WIDTH, HEIGHT,font_txt
from blocks.crafting_table import CraftingTable as crafting_table_item

class Inventory:
    def __init__(self) -> None:
        self.SLOT_NUMBER = 9
        self.INV_NUMBER = 27
        self.hotbar = [
            Slot(None, True),
            *[Slot(None) for i in range(self.SLOT_NUMBER - 1)],
        ]
        self.inventory = [Slot(None) for i in range(self.INV_NUMBER +0)]
        self.shield = Slot(None, False)
        self.crafting_grid = (Slot(None,False),Slot(None,False),Slot(None,False),Slot(None,False), Slot(None, False))
        self.selected = self.hotbar[0]
        self.selected_n = 0
        self.change_cd = 0.5 * FPS
        self.interaction_cd_const = 0.4 * FPS
        self.interaction_cd = 0
        self.cd = 0
        self.animation_active = False
        self.animation_progress = 0
        self.item_name = None
        self.wardrobe_count = 9
        self.wardrobe_stuff = [Slot(None) for i in range(self.wardrobe_count +0)]
        self.developer_items()
        # Active slot events

    def add_to_inventory(self, item, count):
        slot = None
        i = 0
        all_inv = self.hotbar + self.inventory
        while i < len(all_inv):
            slot = all_inv[i]
            if (
                slot.get_item() != None
                and slot.get_item().title == item.title
                and slot.count + count <= 64
            ):
                # found avalible slot
                slot.count += count

                item.parent = slot
                return True
            i += 1

        slot = None
        i = 0
        while i < len(all_inv):
            slot = all_inv[i]
            if slot.get_item() == None:
                # found
                slot.update_activity(item)
                item.parent = slot
                return True
            i += 1

        return False

    # REMOVE ON PUSH
    def developer_items(self):
        # do not cheat or ill eat you

        self.hotbar[0].update_activity(crafting_table_item(self.hotbar[-1]))
        self.hotbar[0].count = 3

    def f_all(self, active_currently):
        for item in self.hotbar:
            # None | class<Item>
            if item is not active_currently:
                item.update_activity(item.get_item(), False)
            else:
                item.update_activity(item.get_item(), True)

    def check_info(self, info,gui_coordinates,walls, breaked_stuff, blocks, colliders):
        if len(info) > 3:
            if info[8] == "0":  # right
                self.selected.get_item().on_right_click(
                    tuple(gui_coordinates), walls, breaked_stuff, blocks, colliders
                )
                self.interaction_cd = self.interaction_cd_const
            if info[10] == "0":
                self.selected.get_item().on_left_click(
                    tuple(gui_coordinates), walls, breaked_stuff, blocks, colliders
                )
                self.interaction_cd = self.interaction_cd_const

    def tick(self, info, screen,player,gui_coordinates,walls, breaked_stuff, blocks, colliders):
        # COOLDOWN
        if self.interaction_cd > 0:
            self.interaction_cd -= 1
        else:
            self.interaction_cd = 0
            if self.selected.item != None:
                self.check_info(info,gui_coordinates,walls, breaked_stuff, blocks, colliders)
        if self.cd > 0:
            self.cd -= 1
        else:
            self.cd = 0
            self.scroll(info,screen)
        # 8, 10
        for item in self.hotbar:
            if item.item != None:

                item.item.on_move(player)
        self.act_s()
        x = (WIDTH - (70 * (len(self.hotbar) + 2))) / 2
        for slot in self.hotbar:
            x += 70
            slot.draw(screen, (x, HEIGHT - 70))
            if slot.count > 1:
                text_surf = font_txt.render(str(slot.count), False, COUNT_COLOR)
                screen.blit(text_surf, (x + 55, HEIGHT - 30))

    def classify_np(self, info):
        if len(info) > 1:
            if info[4] == "0":
                # left
                return "l"
            elif info[6] == "0":
                return "r"
        return ""
        # ['516', '514', '1', '1:', '1', '2:', '1', '3:', '1', '4:', '1', '5:', '1', '6:', '1', '\n']

    def act_s(self):
        self.selected.is_active = True

    def scroll(self, info,screen):
        np = self.classify_np(info)

        if np == "l":
            self.selected_n -= 1
            self.cd = self.change_cd
            self.animation_active = True
            self.animation_progress = 0

        if np == "r":
            self.selected_n += 1
            self.cd = self.change_cd
            self.animation_active = True
            self.animation_progress = 0

        if self.selected_n < 0:
            self.selected_n = self.SLOT_NUMBER - 1
        elif self.selected_n > self.SLOT_NUMBER - 1:
            self.selected_n = 0

        self.selected = self.hotbar[self.selected_n]
        self.f_all(self.selected)

        if self.animation_active and self.selected.item is not None:
            self.animation_progress += 20

            if self.animation_progress == 20:
                self.item_name = font_txt.render(
                    self.selected.item.title, True, self.selected.item.rarity.color 
                )

                self.item_name.set_alpha(28)

            if self.animation_progress >= 227:
                self.animation_active = False
                self.item_name = self.item_name
            if self.item_name is not None:
                alpha_value = min(255, self.animation_progress + 28)
                self.item_name.set_alpha(alpha_value)
        if self.item_name is not None and self.selected.item is not None:
            text_x = WIDTH//2 - self.item_name.get_width() // 2

            screen.blit(self.item_name, (text_x, HEIGHT - 110))

inventory = Inventory()