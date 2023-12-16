import pygame
class ResourceManager:
    def __init__(self) -> None:
        self.player = pygame.image.load("res/player.png")
        self.player = pygame.transform.scale(self.player, (50,50))
        self.slot_active = pygame.image.load("res/active.png")
        self.slot_active = pygame.transform.scale(self.slot_active, (70,70))
        self.slot_unactive = pygame.image.load("res/unactive.png")
        self.slot_unactive = pygame.transform.scale(self.slot_unactive, (70,70))
        # load breaking states
        self.breaking_states_og = []
        pygame.image.
        self.players = []
        for i in range(36):
            self.players.append(pygame.transform.rotate(self.player, 360/36*i))
    def get_player(self):
        return self.player
    def get_players(self):
        return self.players
    def get_unactive_slot(self):
        return self.slot_unactive
    def get_active_slot(self):
        return self.slot_active
    def get_breaking_states(self, size):
