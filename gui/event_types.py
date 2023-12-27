class HOVER:
    def __init__(self,hld = []) -> None:
        self.evt_type = HOVER
        self.hold = hld
    def call(self):
        for holdi in self.hold:
            holdi()
class RIGHT_CLICK:
    def __init__(self,hld = []) -> None:
        self.evt_type =RIGHT_CLICK
        self.hold = hld
    def call(self):
        for holdi in self.hold:
            holdi()
class LEFT_CLICK:
    def __init__(self,hld = []) -> None:
        self.evt_type =LEFT_CLICK
        self.hold = hld
    def call(self):
        for holdi in self.hold:
            holdi()