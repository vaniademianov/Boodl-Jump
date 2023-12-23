import pygame
import os
from cons import PLAYER_SIZE
class ResourceManager:
    def __init__(self, res_name = "") -> None:
        
        self.player = pygame.image.load("res/player.png")
        self.player = pygame.transform.scale(self.player, PLAYER_SIZE)
        self.slot_active = pygame.image.load("res/active.png")
        self.slot_active = pygame.transform.scale(self.slot_active, (70,70))
        self.slot_unactive = pygame.image.load("res/unactive.png")
        self.slot_unactive = pygame.transform.scale(self.slot_unactive, (70,70))
        # load breaking states
        filenames = [f for f in os.listdir("res/destroy_stages")]
        self.breaking_states_og = [pygame.image.load("res/destroy_stages/"+surf) for surf in filenames]
        print(self.breaking_states_og)    
        self.crafting_table = pygame.image.load("res/crafting_table.png")
        self.crafting_table = pygame.transform.scale(self.crafting_table, (25,25))
        self.scope = pygame.image.load("res/scope.png")
        self.scope = pygame.transform.scale(self.scope, (50,50))

        self.scope_on_bad_loc = pygame.image.load("res/scope_on_bad_loc.png")
        self.scope_on_bad_loc = pygame.transform.scale(self.scope_on_bad_loc, (50,50))
        self.scope_on_block = pygame.image.load("res/scope_on_block.png")
        self.scope_on_block = pygame.transform.scale(self.scope_on_block, (50,50))
        self.scope_on_good_location = pygame.image.load("res/scope_on_good_location.png")
        self.scope_on_good_location = pygame.transform.scale(self.scope_on_good_location, (50,50))


        self.players = []
        for i in range(72):
            self.players.append(pygame.transform.rotate(self.player, 360/72*i))

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
            res.append(pygame.transform.scale(state, size))
        return res
    def get_crafting_table(self, size):
        result = pygame.transform.scale(self.crafting_table, size)
        return result
    def get_scope(self):
        return self.scope
    def get_scope_on_good_loc(self):
        return self.scope_on_good_location
    def get_scope_on_bad_loc(self):
        return self.scope_on_bad_loc
    def get_scope_on_block(self):
        return self.scope_on_block
    
resource_manager = ResourceManager()