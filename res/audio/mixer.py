import pygame
import random

pygame.mixer.init()

class Mixer:
    def __init__(self) -> None:
        self.block1 = pygame.mixer.Sound("res/audio/sounds/block1.ogg")
        self.block2 = pygame.mixer.Sound("res/audio/sounds/block2.ogg")
        self.block3 = pygame.mixer.Sound("res/audio/sounds/block3.ogg")
        self.block4 = pygame.mixer.Sound("res/audio/sounds/block4.ogg")
        self.loot = pygame.mixer.Sound("res/audio/sounds/loot.ogg")

        self.blocks = [self.block1, self.block2,self.block3,self.block4]
        self.current_block_playing = None
    def play_block_breaking(self, volume):
        blck =random.choice(self.blocks)
        blck.set_volume(volume)
        blck.play()
        self.current_block_playing = blck 
    def play_looting(self, volume):
        s = self.loot
        s.set_volume(volume)
        s.play()
        
    def stop_block_breaking(self):
        if self.current_block_playing != None:
            self.current_block_playing.stop()
    def stop_looting(self):
        self.loot.stop()

mx = Mixer()