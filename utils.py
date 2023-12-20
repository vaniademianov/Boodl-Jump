import pygame
pygame.init()
class Utilz:
    @staticmethod
    def good_location(cords,colliders,player_loc):
        
        # TODO
        return True
    @staticmethod
    def round_coordinates(inp_cords,colliders):
        # TODO
        return inp_cords
    def calc_dist(x1,y1,x2,y2):
        return pygame.math.Vector2(x1, y1).distance_to((x2, y2))