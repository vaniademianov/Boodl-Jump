from gui.gui_module.gui import Gui
from gui.gui_module.frame import Frame
from inventory.inventory import inventory
from other.cons import (
    BLACK,
    FIFTH_INV_COLOR,
    FIRST_INV_COLOR,
    FOURTH_INV_COLOR,
    HEIGHT,
    SIXTH_INV_COLOR,
    THIRD_INV_COLOR,
    WHITE,
    WIDTH,
)
from gui.gui_module.label import Label
from gui.gui_module.gui_slot import GUIslot
from gui.gui_module.irs import o_irs
from gui.gui_module.button import Button
from gui.gui_module.image import Image
from res.resource_manager import resource_manager
from other.coordinates import Coordinates
from gui.gui_module.event_types import LEFT_CLICK
from items.crafting.proccess_crafting import ProcessCraft
from items.crafting.grid_types import grid2x2, grid3x3


gui = Gui(False)
frame1 = Frame(
    FIRST_INV_COLOR,
    0,
    (800, 235),
    (WIDTH / 2, HEIGHT / 2 - 117 - 150),
    False,
    (16, 16, 0, 0),
)
frame1.pack(gui, 0)
inventory_label = Label("Inventory", WHITE, 32, "Brownie", (200, 40), False)
inventory_label.pack(gui, 1)

frame2 = Frame(THIRD_INV_COLOR, 15, (798, 15), (WIDTH / 2, 250), False)
frame2.pack(gui, -1)
frame3 = Frame(WHITE, 15, (264, 178), (255, 150), False)
frame3.pack(gui, -1)
shield_slot = GUIslot(
    (60, 60), FOURTH_INV_COLOR, 16, (440, 200), False, o_irs, inventory.shield
)
shield_slot.pack(gui, -1)

arch_button = Button(FOURTH_INV_COLOR, 16, (60, 60), (440, 40), True)
arch_button.pack(gui, -1)
shield_img = Image(resource_manager.get_shield(), shield_slot.coordinates, True, False)
shield_img.pack(gui, -1)
arch_img = Image(
    resource_manager.get_achievement(), arch_button.coordinates, True, False
)
arch_img.pack(gui, -1)
dress_button = Button(FOURTH_INV_COLOR, 16, (60, 60), (440, 120), True)
dress_button.pack(gui, -1)
dress_img = Image(resource_manager.get_hanger(), dress_button.coordinates, True, False)
dress_img.pack(gui, -1)

crafting_label = Label("Crafting", WHITE, 32, "Brownie", (580, 40), False)
crafting_label.pack(gui, -1)
crafting_slot1 = GUIslot(
    (88, 88),
    FIFTH_INV_COLOR,
    0,
    (560, 110),
    False,
    o_irs,
    inventory.crafting_grid[0],
    (16, 0, 0, 0),
    3,
    BLACK,
)
crafting_slot1.pack(gui, -1)
crafting_slot2 = GUIslot(
    (88, 88),
    FIFTH_INV_COLOR,
    0,
    (646, 110),
    False,
    o_irs,
    inventory.crafting_grid[1],
    (0, 16, 0, 0),
    3,
    BLACK,
)
crafting_slot2.pack(gui, -1)
crafting_slot3 = GUIslot(
    (88, 88),
    FIFTH_INV_COLOR,
    0,
    (560, 198),
    False,
    o_irs,
    inventory.crafting_grid[2],
    (0, 0, 16, 0),
    3,
    BLACK,
)
crafting_slot3.pack(gui, -1)
crafting_slot4 = GUIslot(
    (88, 88),
    FIFTH_INV_COLOR,
    0,
    (646, 198),
    False,
    o_irs,
    inventory.crafting_grid[3],
    (0, 0, 0, 16),
    3,
    BLACK,
)
crafting_slot4.pack(gui, -1)
crafting_slots = [crafting_slot1, crafting_slot2, crafting_slot3, crafting_slot4]
crafting_arrow = Image(
    resource_manager.get_arrow_right(), Coordinates(735, 154), False, False
)
crafting_arrow.pack(gui, -1)

processor = ProcessCraft(
    grid2x2, inventory.crafting_grid[:4], inventory.crafting_grid[-1]
)


crafting_result = GUIslot(
    (88, 88),
    FIFTH_INV_COLOR,
    16,
    (830, 154),
    False,
    o_irs,
    inventory.crafting_grid[4],
    None,
    3,
    BLACK,
    afterclick=processor.take,
)
crafting_result.pack(gui, -1)


wardrobe = Gui(False)

wardrobe_frame = Frame(
    SIXTH_INV_COLOR, 0, (90, 578), (81, HEIGHT / 2), False, (16, 0, 16, 0)
)
wardrobe_frame.pack(wardrobe, 0)

base_y = 200
wardrobe_lst = []


def reactivate_wardrobe():
    if wardrobe.is_visible:
        # disable

        wardrobe.left_to_right_slide_anim(wardrobe.close, True)
        wardrobe.left_to_right_slide_anim_progress = WIDTH / 2
        print(
            wardrobe.left_to_right_slide_anim_progress,
            type(wardrobe.left_to_right_slide_anim_progress),
        )
        wardrobe.update_xs((WIDTH / 2))
        wardrobe.transparency_anim()
    else:
        wardrobe.open()
        wardrobe.right_to_left_slide_anim(True)
        wardrobe.update_xs(-(WIDTH / 2))
        wardrobe.update_xs(27)
        # wardrobe.backward_transparency_anim()
        # wardrobe.right_to_left_slide_anim_progress = WIDTH/2
        # wardrobe.update_xs(-(WIDTH/2))


for parent_slot in inventory.crafting_grid:
    nw_slt = GUIslot(
        (65, 65), FOURTH_INV_COLOR, 16, (43, base_y), False, o_irs, parent_slot
    )
    wardrobe_lst.append(nw_slt)
    nw_slt.pack(wardrobe, -1)

    base_y += 150
dress_button.on_left_click = reactivate_wardrobe
# dress_img.on_left_click = reactivate_wardrobe
gui.subscribe(dress_button, LEFT_CLICK)


def tick(gui_coordinates, splt_val, *args):
    shield_slot.sync(gui_coordinates, splt_val)
    dress_img.sync()
    arch_img.sync()
    shield_img.sync()
    crafting_arrow.sync()
    for crafting_slot in crafting_slots:
        crafting_slot.sync(gui_coordinates, splt_val)
    crafting_result.sync(gui_coordinates, splt_val)
    processor.tick()