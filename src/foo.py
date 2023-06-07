#!/usr/bin/python3
# https://realpython.com/pygame-a-primer/

import pygame
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    #     QUIT,
)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# get the tank image


class Tank(pygame.sprite.Sprite):
    @classmethod
    def load_image(cls, fn):
        """Load a sprite image to be used in tank instantances."""
        img = pygame.image.load(fn)
        return img.convert_alpha()

    def __init__(self, screen, img):
        super(Tank, self).__init__()
        self.image = img
        self.rect = img.get_rect(center=(50, 50))
        # self.surf = pygame.Surface((75, 25))
        # self.surf.fill((255, 255, 255))
        # self.rect = self.surf.get_rect()
        self.screen = screen

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(800, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(600, self.rect.bottom)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode(
    (800, 600), pygame.DOUBLEBUF | pygame.RESIZABLE)
fake_screen = screen.copy()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

i = Tank.load_image("../assets/Modern_Tank_Pack1.png")

tank = Tank(screen, i)
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(tank)

clock = pygame.time.Clock()

# Run until the user asks to quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                event.size,
                pygame.DOUBLEBUF | pygame.RESIZABLE,
            )
        elif event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        elif event.type == ADDENEMY:
            ne = Enemy()
            enemies.add(ne)
            all_sprites.add(ne)

    # Fill the background with black
    fake_screen.fill((0, 0, 0))

    # Draw a solid blue circle in the center
    pygame.draw.circle(fake_screen, (0, 0, 255), (550, 550), 45)

    tank.update(pygame.key.get_pressed())
    enemies.update()

    # for e in all_sprites:
    fake_screen.blit(tank.image, tank.rect)

    # if pygame.sprite.spritecollideany(tank, enemies):
    #     tank.kill()
    #     running = False

    screen.blit(pygame.transform.scale(
        fake_screen, screen.get_rect().size), (0, 0))

    clock.tick(60)
    # Flip the display
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()
