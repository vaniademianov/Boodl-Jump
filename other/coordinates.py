

class Coordinates:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y    
    def to_tuple(self):
        return (self.x, self.y)