import pygame
import math
from other.cons import *
pygame.init()


class rc:
    def __init__(self,rect) -> None:
        self.rect = rect

class Holder:
    def __init__(self, w, h, rct_size=50) -> None:
        self.rizz = 0
        self.grid = [[pygame.Rect(x, y, rct_size, rct_size) for x in range(0, w, rct_size)] for y in range(-10025, h, rct_size)]

    def get_nearest(self, coordinates):
        min_distance = float('inf')  # Start with a large distance
        nearest_rect = None

        for row in self.grid:
            for rect in row:
                distance = pygame.math.Vector2(coordinates) - pygame.math.Vector2(rect.topleft)
                squared_distance = distance.length_squared()
                if squared_distance < min_distance:
                    min_distance = squared_distance
                    nearest_rect = rect

        return nearest_rect

    def rect_angle(self, riz):
        for x in self.grid:
            for elem in x:
                elem.y -= riz

    def greedy(self, player):
        self.rect_angle(player.y_vel)
grd = Holder(WIDTH, HEIGHT)

class Utilz:
    @staticmethod
    def good_location(cords,colliders:pygame.sprite.Group,player_loc):
        rect = grd.get_nearest(cords)
 
        if Utilz.calc_dist_cord(rect.center, player_loc) > INTERACTION_DISTANCE:
 
            return False
        for collider in colliders.sprites():
            if pygame.sprite.collide_rect(collider, rc(rect)):

                return False
        rect_2 = pygame.Rect((0,0), PLAYER_SIZE)
        rect_2.center = player_loc
        if pygame.sprite.collide_rect(rc(rect_2),rc(rect)):
  
            return False

        return True 
    @staticmethod
    def round_coordinates(inp_cords, pc, colliders):
        # res = (
        #     round(inp_cords[0] / 50) * 50 + (BASE_BLOCK_SIZE[0] / 2),
        #     round(inp_cords[1] / 50) * 50 + (BASE_BLOCK_SIZE[1] / 2)
        # )
        # return res
        return (grd.get_nearest(inp_cords).topleft[0], grd.get_nearest(inp_cords).topleft[1] - pc)
    @staticmethod
    def calc_dist(x1,y1,x2,y2):
        return pygame.math.Vector2(x1, y1).distance_to((x2, y2))
    @staticmethod
    def calc_dist_rec(r1, r2):
        return pygame.math.Vector2(r1.x, r1.y).distance_to((r2.x, r2.y))
    @staticmethod
    def calc_dist_cord(a, b):
        return pygame.math.Vector2(a[0], a[1]).distance_to(b)
    @staticmethod
    def convert_top_left_to_center(top_left_x, top_left_y, width, height):
        center_x = top_left_x + width / 2
        center_y = top_left_y + height / 2
        return center_x, center_y
    @staticmethod
    def convert_center_to_top_left(top_left_x, top_left_y, width, height):
        center_x = top_left_x - width / 2
        center_y = top_left_y - height / 2
        return center_x, center_y
    @staticmethod
    def w(a: tuple, b: tuple):
        return (a[0] + b[0], a[1] + b[1])

    @staticmethod
    def wm(a: tuple, b: tuple):
        return (a[0] - b[0], a[1] - b[1])

    @staticmethod
    def wd(a: tuple, b: int):
        return (a[0] / b, a[1] / b)

    @staticmethod
    def rect_group_collide(r: pygame.Rect, g: pygame.sprite.Group):
        for sprite in g.sprites():
            if r.colliderect(sprite.rect):
                return True
        return False

    @staticmethod
    def the_one(a, b):
        return True in [a, b]

    @staticmethod
    def i_fals(v):
        return v != None
    @staticmethod
    def generate_color_transition(color1, color2, time):
    # Convert color strings to RGB tuples
        rgb_color1 = color1
        rgb_color2 = color2 
        time = int(time)
        # Calculate the step size for each color component
        step_r = (rgb_color2[0] - rgb_color1[0]) // time
        step_g = (rgb_color2[1] - rgb_color1[1]) // time
        step_b = (rgb_color2[2] - rgb_color1[2]) // time
        print(time)
        # Generate the list of colors
        color_transition = [
            (
                rgb_color1[0] + step_r * i,
                rgb_color1[1] + step_g * i,
                rgb_color1[2] + step_b * i
            ) for i in range(int(time) + 1)
        ]

        return color_transition
    # @staticmethod
    # def draw_line_with_size(surface: pygame.Surface, start, end, size,color):
    #     angle = math.atan2(end[1] - start[1], end[0] - start[0])

    #     offset_x = size * math.sin(angle)
    #     offset_y = size * math.cos(angle)

    #     for i in range(-size // 2, size // 2 + 1):
    #         offset = (i * offset_x, i * offset_y)
    #         pygame.draw.line(surface, color, (start[0] + offset[0], start[1] + offset[1]),
    #                          (end[0] + offset[0], end[1] + offset[1]))

    # @staticmethod
    # def blit_block(rct: pygame.Rect, color, size):
    #     surface = pygame.Surface(rct.size)
    #     surface = surface.convert_alpha()
    #     Utilz.draw_line_with_size(surface, rct.topleft, rct.topright, size, color)
    #     Utilz.draw_line_with_size(surface, rct.topright, rct.bottomright, size, color)
    #     Utilz.draw_line_with_size(surface, rct.bottomright, rct.bottomleft, size, color)
    #     Utilz.draw_line_with_size(surface, rct.bottomleft, rct.topleft, size, color)
    #     return surface
class DataClass_Transporter:
    def __init__(self,val) -> None:
        self.val = val
    def get_val(self):
        return self.val
    def set_val(self, val):
        self.val = val