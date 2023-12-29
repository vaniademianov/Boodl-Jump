from gui.gui_module.gui import Gui
from gui.gui_module.frame import Frame
from other.cons import BLACK, FIRST_INV_COLOR, FPS, HEIGHT, RED, SECOND_INV_COLOR, WHITE, WIDTH
from gui.gui_module.event_types import LEFT_CLICK, RIGHT_CLICK
from gui.gui_module.gui_slot import GUIslot
from gui.gui_module.irs import o_irs
from inventory.inventory import inventory



gui = Gui(False)
frame1 = Frame(FIRST_INV_COLOR, 0, (800, 434), (WIDTH/2, HEIGHT/2-150+217), False,(0,0,16,16))
frame1.pack(gui, 0)
slotovii_hotbar = []
x = 154
for i in range(9):
    new_slotiks = GUIslot((65,65), SECOND_INV_COLOR, 0, (x, 633), False, o_irs, inventory.hotbar[i])
    gui.subscribe(new_slotiks, RIGHT_CLICK)
    gui.subscribe(new_slotiks, LEFT_CLICK)
    new_slotiks.pack(gui, 1)
    
    slotovii_hotbar.append(new_slotiks)
    x += 87


delay = 0
is_button_left = True
def tick(gui_coordinates, splt_val, *args):
    global delay, is_button_left
    delay -= 1
    for slt in slotovii_hotbar:
        slt.sync()
    if splt_val[-1] == "1":
        is_button_left = True
    if splt_val[-1] == "0" and delay <= 0 and is_button_left == True:
        if gui.is_visible == False:

            gui.open()
            gui.transparency_anim()
            gui.slide_in_anim()
            delay = FPS*0.4
            is_button_left = False
        else:
            # o_irs.closed(inventory.player)
            # gui.transparency_anim()
            gui.backward_transparency_anim()
            gui.close_animated()
            delay = FPS*0.4
            is_button_left=False
# example_frame.on_right_click = tick
# example_gui.subscribe(example_frame, RIGHT_CLICK)