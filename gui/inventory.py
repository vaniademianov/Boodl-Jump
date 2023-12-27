from gui.gui_module.gui import Gui
from gui.gui_module.frame import Frame
from cons import BLACK, FPS, HEIGHT, RED, WHITE, WIDTH
from gui.gui_module.event_types import RIGHT_CLICK

gui = Gui(True)
frame1 = Frame(WHITE, 5, (WIDTH/2, HEIGHT/2), (WIDTH/2, HEIGHT/2), True)
frame1.pack(gui, 0)
delay = 0
def tick(gui_coordinates, splt_val):
    global delay
    gui.tick(gui_coordinates, splt_val)
    delay -= 1
    if splt_val[-1] == "0" and delay <= 0:
        if gui.is_visible == False:
            gui.open()
            gui.transparency_anim()
            gui.slide_in_anim()
            delay = FPS*0.4
        else:
            gui.close_animated()
            delay = FPS*0.4
# example_frame.on_right_click = tick
# example_gui.subscribe(example_frame, RIGHT_CLICK)