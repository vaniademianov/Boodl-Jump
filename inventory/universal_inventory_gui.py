from gui.gui_module.gui import Gui
from gui.gui_module.frame import Frame
from other.cons import (
    BLACK,
    FIRST_INV_COLOR,
    FPS,
    HEIGHT,
    RED,
    SECOND_INV_COLOR,
    THIRD_INV_COLOR,
    WHITE,
    WIDTH,
)
from gui.gui_module.event_types import LEFT_CLICK, RIGHT_CLICK
from gui.gui_module.gui_slot import GUIslot
from gui.gui_module.irs import o_irs
from inventory.inventory_gui import gui as o_gui
from inventory.inventory import inventory

BASE_INV_Y = 320
gui = Gui(False)
frame1 = Frame(
    FIRST_INV_COLOR,
    0,
    (800, 434),
    (WIDTH / 2, HEIGHT / 2 - 150 + 217),
    False,
    (0, 0, 16, 16),
)
frame1.pack(gui, 0)
slotovii_hotbar = []
x = 154

for i in range(9):
    new_slotiks = GUIslot(
        (65, 65), SECOND_INV_COLOR, 0, (x, 633), False, o_irs, inventory.hotbar[i]
    )

    new_slotiks.pack(gui, 1)

    slotovii_hotbar.append(new_slotiks)
    x += 87

frame2 = Frame(THIRD_INV_COLOR, 15, (798, 15), (WIDTH / 2, 561), False)
frame2.pack(gui, -1)
ONE_SIZE = 95
slotovii_inventar = [
    GUIslot(
        (ONE_SIZE, 88),
        SECOND_INV_COLOR,
        0,
        (146, BASE_INV_Y),
        False,
        o_irs,
        inventory.inventory[0],
        (16, 0, 0, 0),
        4,
        BLACK,
    )
]
slotovii_inventar[0].pack(gui, -1)

for i in range(1, 8, 1):
    new_slot = GUIslot(
        (ONE_SIZE, 88),
        SECOND_INV_COLOR,
        0,
        ((i) * 88 + (54 + ONE_SIZE), BASE_INV_Y),
        True,
        o_irs,
        inventory.inventory[i],
        (0, 0, 0, 0),
        4,
        BLACK,
    )
    new_slot.pack(gui, -1)

    slotovii_inventar.append(new_slot)
new_slot = GUIslot(
    (ONE_SIZE, 88),
    SECOND_INV_COLOR,
    0,
    (WIDTH - 146, BASE_INV_Y),
    False,
    o_irs,
    inventory.inventory[8],
    (0, 16, 0, 0),
    4,
    BLACK,
)


def a(i):
    return 3 if i >= 1 else 0


new_slot.pack(gui, -1)
slotovii_inventar.append(new_slot)
for i in range(0, 9, 1):
    new_slot = GUIslot(
        (ONE_SIZE, 88),
        SECOND_INV_COLOR,
        0,
        (((i) * 88) + (51 + ONE_SIZE) + a(i), BASE_INV_Y + ONE_SIZE - 10),
        True,
        o_irs,
        inventory.inventory[i + 9],
        (0, 0, 0, 0),
        4,
        BLACK,
    )
    new_slot.pack(gui, -1)

    slotovii_inventar.append(new_slot)
new_slot = GUIslot(
    (ONE_SIZE, 88),
    SECOND_INV_COLOR,
    0,
    (146, BASE_INV_Y+ONE_SIZE*2-20),
    False,
    o_irs,
    inventory.inventory[18],
    (0, 0,16, 0),
    4,
    BLACK,
)

new_slot.pack(gui, -1)
slotovii_inventar.append(new_slot)


for i in range(1, 8, 1):
    new_slot = GUIslot(
        (ONE_SIZE, 88),
        SECOND_INV_COLOR,
        0,
        ((i) * 88 + (54 + ONE_SIZE), BASE_INV_Y+ONE_SIZE*2-20),
        True,
        o_irs,
        inventory.inventory[i+19],
        (0, 0, 0, 0),
        4,
        BLACK,
    )
    new_slot.pack(gui, -1)

    slotovii_inventar.append(new_slot)

new_slot = GUIslot(
    (ONE_SIZE, 88),
    SECOND_INV_COLOR,
    0,
    (WIDTH - 146, BASE_INV_Y+ONE_SIZE*2-20),
    False,
    o_irs,
    inventory.inventory[8+18],
    (0, 0, 0, 16),
    4,
    BLACK,
)

new_slot.pack(gui, -1)
slotovii_inventar.append(new_slot)
delay = 0
is_button_left = True
is_leaving = False

def tick(gui_coordinates, splt_val, *args):
    global delay, is_button_left
    player = args[0]
    delay -= 1
    for slt in slotovii_hotbar:
        slt.sync(gui_coordinates, splt_val)
    for slt in slotovii_inventar:
        slt.sync(gui_coordinates, splt_val)
    if splt_val[-1] == "1":
        is_button_left = True
    if splt_val[-1] == "0" and delay <= 0 and is_button_left == True:
        if gui.is_visible == False:
            gui.open()
            gui.transparency_anim()
            gui.slide_in_anim()
            o_gui.open()
            o_gui.transparency_anim()
            o_gui.slide_in_anim()
            player.controls_locked = True
            delay = FPS * 0.4
            is_leaving = False
            is_button_left = False
        else:
            # o_irs.closed(inventory.player)
            # gui.transparency_anim()
            o_gui.backward_transparency_anim()
            player.controls_locked = False
            is_leaving = True
            o_gui.close_animated()
            gui.backward_transparency_anim()
            gui.close_animated()
            delay = FPS * 0.4
            is_button_left = False


# example_frame.on_right_click = tick
# example_gui.subscribe(example_frame, RIGHT_CLICK)
