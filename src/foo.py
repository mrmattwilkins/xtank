#!/usr/bin/python3
# https://realpython.com/pygame-a-primer/

import pygame

from pygame.locals import (
    #     K_UP,
    #     K_DOWN,
    #     K_LEFT,
    #     K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    #     QUIT,
)

# Simple pygame program

# Import and initialize the pygame library
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE,
)
fake_screen = screen.copy()

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
                pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE,
            )
        elif event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

    # Fill the background with white
    fake_screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(fake_screen, (0, 0, 255), (250, 250), 75)

    screen.blit(pygame.transform.scale(fake_screen, screen.get_rect().size), (0, 0))

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
