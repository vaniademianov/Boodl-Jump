import pygame
import os
from other.cons import PLAYER_SIZE
import json 
 

def load(*args, **kwargs): 
    return pygame.image.load(*args,**kwargs)

def scale(*args, **kwargs): 
    return pygame.transform.scale(*args, **kwargs)
class TextureAtlas:
    """Class for loading texture atlases""" 
    def __init__(self, path2folder):
        self.texture_path = os.path.join(path2folder, "texture.json")
        self.texture_png_path = os.path.join(path2folder, "texture.png")
        with open(self.texture_path) as f:
            self.positions = json.load(f)
        self.texture = load(self.texture_png_path)
        self.frames = {}
        self.load()
    def load(self):
        for frame_name, frame_rect  in (self.positions["frames"]).items(): 
            x, y, w, h = frame_rect["frame"].values()
            rect = pygame.Rect(x, y, w, h)
            cropped_img = self.texture.subsurface(rect)
            self.frames[frame_name] = cropped_img

    def get_frame(self, frame: str):    
        """Get frame with specific name"""
        return self.frames.get(frame, None)
    def get_all_frames(self):
        """Get all frames"""
        return self.frames.values()
class ResourceManager:
    def __init__(self, res_name = "") -> None:
        self.scope_atlas = TextureAtlas("res/images/cursors")

        self.player = load("res/images/player.png")
        self.player = scale(self.player, PLAYER_SIZE)
        self.slot_active = self.scope_atlas.get_frame("active.png")
        self.slot_active = scale(self.slot_active, (70,70))
        self.slot_unactive = self.scope_atlas.get_frame("unactive.png")
        self.slot_unactive = scale(self.slot_unactive, (70,70))

        
        self.blocks_atlas = TextureAtlas("res/images/blocks")


        # load breaking states
        filenames = [f for f in os.listdir("res/images/destroy_stages")]
        self.breaking_states_og = [load("res/images/destroy_stages/"+surf) for surf in filenames]

        self.crafting_table = self.blocks_atlas.get_frame("crafting_table.png")
    
        self.scope = self.scope_atlas.get_frame("scope.png")


        self.scope_on_bad_loc = self.scope_atlas.get_frame("scope_on_bad_loc.png")
        self.scope_on_block = self.scope_atlas.get_frame("scope_on_block.png")
        self.scope_on_block = scale(self.scope_on_block, (56,56))
        self.scope_on_good_location = self.scope_atlas.get_frame("scope_on_good_location.png")

        self.scope_on_isnt_breakable = self.scope_atlas.get_frame("scope_on_isnt_breakable.png")
        self.scope_on_isnt_breakable = scale(self.scope_on_isnt_breakable, (56,56))

        self.achievement_icon = load("res/images/achievement.svg")
        self.achievement_icon = scale(self.achievement_icon, (36,51))

        self.hanger_icon = load("res/images/hanger.svg")
        self.hanger_icon = scale(self.hanger_icon, (46,36))
        self.shield_icon = load("res/images/shield.svg")
        self.shield_icon = scale(self.shield_icon, (44,46))
        self.arrow_right = load("res/images/arrow-right.svg")
        self.arrow_right = scale(self.arrow_right, (60,46))
        self.players = []
        for i in range(72):
            self.players.append(pygame.transform.rotate(self.player, 360/72*i))
    def get_arrow_right(self):
        return self.arrow_right
    def get_shield(self):
        return self.shield_icon
    def get_hanger(self):
        return self.hanger_icon
    def get_achievement(self):
        return self.achievement_icon
    def get_brownie_s(self, size):
        self.brownie_stencil = pygame.font.Font("res/fonts/BrownieStencil.ttf",size)
        return self.brownie_stencil
    def get_freedom(self, size):
        self.freedom = pygame.font.Font("res/fonts/Freedom.ttf",size)
        return self.freedom
    def get_player(self):
        return self.player
    def get_players(self):
        return self.players
    def get_unactive_slot(self):
        return self.slot_unactive
    def get_active_slot(self):
        return self.slot_active
    def get_breaking_states(self, size):
        res = []
        for state in self.breaking_states_og:
            res.append(scale(state, size))
        return res
    def get_crafting_table(self, size):
        result = scale(self.crafting_table, size)
        return result
    def get_scope(self):
        return self.scope
    def get_scope_on_good_loc(self):
        return self.scope_on_good_location
    def get_scope_on_bad_loc(self):
        return self.scope_on_bad_loc
    def get_scope_on_block(self):
        return self.scope_on_block
    def get_scope_on_isnt_breakable(self):
        return self.scope_on_isnt_breakable
resource_manager = ResourceManager()