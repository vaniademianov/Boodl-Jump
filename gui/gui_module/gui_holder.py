class GuiGroup:
    def __init__(self) -> None:
        self.guis = []
    def update(self,gui_coordinates, splt_val, *args):
        for gei in self.guis:
            gei[0].tick(gui_coordinates, splt_val)

            if gei[1] != None:
                gei[1](gui_coordinates, splt_val,*args)
            
    def draw(self, screen):
        for gei in self.guis:
            gei[0].draw(screen)
            
    def add(self, new_gui, update_func=None):
        self.guis.append((new_gui, update_func))