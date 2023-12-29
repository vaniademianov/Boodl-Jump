from player.wall import Wall
import random
from other.cons import WIDTH, HEIGHT,lst
import pygame

class Generator:
    def __init__(self, player, wall_0) -> None:
        self.wall_0 = wall_0
        self.last_wall = wall_0
        self.player = player
        self.count = 1
        self.hardness = 0
        self.color_n = 1

    def generate(self,walls,colliders):
        y = self.wall_0.rect.y
        c = y // 120

        for i in range(self.count, c + 1):
            j = random.randint(2, 3)
            self.last_y = walls.sprites()[-1].rect.y

            jump_h = sum(range(self.player.jumper + 1)) - self.player.rect.h - 25
            jump_h -= 35
            y = (self.last_wall.rect.top - round(jump_h* 1.5)) 


            pw = list(range(250, 100 - 1, -25))
            while j > 0:
                w = random.choice(
                    pw[
                        min(int(self.hardness / 5), len(pw) - 2) : min(
                            int(self.hardness / 5), len(pw) - 2
                        )
                        + 3
                    ]
                )
                x = random.choice([ii for ii in range(0, WIDTH - w, 50)])

                new_wall = Wall((x - 26, y), (w + 52, 50),topik=y,player=self.player)
                tries = 0
                while (
                    pygame.sprite.spritecollideany(new_wall, colliders) is not None
                ):  # or rect_group_collide(Wall((x, y+70), (w, 50)).rect, walls):
                    if tries > 50:
                        # left or right side:
                        if x < WIDTH / 2:  # left
                            x -= 75
                        else:
                            x += 75
                    else:
                        x = random.choice([ii for ii in range(0, WIDTH - w, 50)])

                    if tries == 70:
                        # while rect_group_collide(Wall((x, y+70), (w, 50)).rect, walls):

                        #     x = random.choice([ii for ii in range(0, WIDTH-w, 50)])
                        new_wall = Wall((x - 26, y), (w + 52, 50),topik=y,player=self.player)
                        break

                    tries += 1
                    # 0,06
                    new_wall = Wall((x - 26, y), (w + 52, 50), color=lst[self.color_n],topik=y,player=self.player)
                    # new_wall_1 = Wall((x+75, self.last_wall.rect.y), (w-125, 50))
                j -= 1
                new_wall = Wall((x, y), (w, 50), color=lst[self.color_n],topik=y,player=self.player)
                # walls_to_add.append(new_wall)
                walls.add(new_wall)
                colliders.add(new_wall)
            self.hardness += 1
            self.color_n += 1

            # last wall format: last_x, last_y_ last_w
            self.last_wall = new_wall
            self.count += 1

