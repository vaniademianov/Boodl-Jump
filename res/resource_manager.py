import pygame
class ResourceManager:
    def __init__(self) -> None:
        self.player = pygame.image.load("res/player.png")
        self.player = pygame.transform.scale(self.player, (50,50))
        self.players = []
        for i in range(36):
            self.players.append(pygame.transform.rotate(self.player, 360/36*i))
    def get_player(self):
        return self.player
    def get_players(self):
        return self.players