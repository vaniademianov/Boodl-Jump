import pygame
import sys

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rotating Coin")

# Set up the coin surface
coin_image = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.circle(coin_image, (255, 255, 0), (25, 25), 25)


angle = 0
rotation_speed = 2 
original_i = coin_image.copy()
clock = pygame.time.Clock()
mini = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Rotate the coin surface

    ang = int(((90 - angle)/90) * coin_image.get_size()[0])

    if ang < 0:

        angr = -ang
    else:

        angr = ang 
    if ang < -original_i.get_width():
        coin_image = original_i.copy()

        angle = 0

    print(ang)
    rotated_coin = pygame.transform.smoothscale(coin_image, (angr, coin_image.get_height()))

    # Clear the screen
    screen.fill((255, 255, 255))

    # Get the rect of the rotated coin to position it properly
    rotated_coin_rect = rotated_coin.get_rect(center=(width // 2, height // 2))

    # Draw the rotated coin on the screen
    screen.blit(rotated_coin, rotated_coin_rect)

    # Update the display
    pygame.display.flip()

    # Increase the angle for the next frame
    angle += rotation_speed

    # Cap the frame rate
    clock.tick(60)
