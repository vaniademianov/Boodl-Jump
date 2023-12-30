import pygame
from other.cons import WIDTH, HEIGHT, HEIGHT_MODIFIER, PLAYER_SIZE
from player.hitbox import Hitty
from res.resource_manager import resource_manager as rm
class Player(pygame.sprite.Sprite):
    def __init__(self, inv,colliders):
        pygame.sprite.Sprite.__init__(self)

        self.og_surf = rm.get_player()
        self.image = self.og_surf
    
        self.rect = self.image.get_rect()
        self.rect.center = (
            WIDTH / 2,
            HEIGHT - self.rect.height + HEIGHT_MODIFIER - 15,
        )
        self.y_vel = 0
        self.jump = False
        self.Y_CHANGE = 0
        self.x_vel = 0
        self.move_down = True
        self.move_up = True
        self.move_left = True
        self.move_right = True
        self.hitbox = Hitty(colliders, PLAYER_SIZE, self.rect.center, self)
        self.angle = 0
        self.change_angle = 0
        self.jumper = 20
        self.inv = inv
        self.controls_locked = False
        self.shifting = False
        self.game_changer = 0
        self.playerz = rm.get_players()
    def shift_changed(self, value):
        value_bull = value == "0"


        if value_bull == True:
            # shift 
            self.image = pygame.transform.scale(self.playerz[round((self.angle) / 36)], (PLAYER_SIZE[0], PLAYER_SIZE[1]-10))
            self.game_changer = 10
        elif value_bull == False:
            self.image = self.playerz[round((self.angle) / 36)]
            self.game_changer = 0
        self.shifting = value_bull
    def rot(self):
        self.angle += self.change_angle
        self.image = self.playerz[round((self.angle) / 36)]
        if self.shifting:
            
            self.image = pygame.transform.scale(self.playerz[round((self.angle) / 36)], (PLAYER_SIZE[0], PLAYER_SIZE[1]-10))
            self.game_changer = 10
    def update(self, classified, splt):
        if splt != None:
            self.shift_changed(splt[2])
        self.change_angle = -(self.x_vel * 2)
        self.rot()
        self.hitbox.update(classified)

        # or not touching anything
        self.move_down = self.hitbox.check_down()
        self.move_up = self.hitbox.check_up()
        self.move_left = self.hitbox.check_left()
        self.move_right = self.hitbox.check_right()
        
        if self.move_down:
            self.y_vel += 1

        else:
            # touchedd the gras
            self.y_vel = 0
            self.jump = False
        if self.controls_locked:
            return
        if classified[0] == "TOP" and not self.jump and self.move_up:
            self.y_vel -= self.jumper
            self.jump = True
        if classified[0] == "CENTER" and classified[1] == None:
            self.x_vel = 0
        elif classified[1] == "RIGHT" and self.move_right:
            self.x_vel += 1
        elif classified[1] == "LEFT" and self.move_left:
            self.x_vel -= 1
        if not self.move_up and self.y_vel < 0:
            self.y_vel = 0

        if self.x_vel != 0 and not self.hitbox.suuper_check_x(self.x_vel):
            self.x_vel = 0
        if self.y_vel != 0 and not self.hitbox.suuper_check_y(self.y_vel):
            self.y_vel = 0
            # self.jump = False
        self.Y_CHANGE += -self.y_vel
 
        # self.rect.centery += self.y_vel
        self.rect.centerx += self.x_vel

        # self.rect.x += 5
        # if self.rect.left > WIDTH:
        #     self.rect.right = 0