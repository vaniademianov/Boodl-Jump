import pygame

class IItem:
    def __init__(self) -> None:
        self.title = "undefined"
        self.is_block = False
    def get_slot(self,*args,**kwargs):
        raise Exception("NotImplemented error")
    def on_move(self,*args,**kwargs):
        raise Exception("NotImplemented error")
    def on_right_click(self,*args,**kwargs):
        raise Exception("NotImplemented error")
    def on_left_click(self,*args,**kwargs):
        raise Exception("NotImplemented error")