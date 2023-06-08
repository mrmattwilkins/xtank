#!/usr/bin/python3
# https://realpython.com/pygame-a-primer/

import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_r,
    K_t,
    #     QUIT,
)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# get the tank image


def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


def rot_center2(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def rot_center3(image, angle):
    """rotate an image while keeping its center and size"""
    pos = image.get_rect().center

    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (
        min(box_rotate, key=lambda p: p[0])[0],
        min(box_rotate, key=lambda p: p[1])[1],
    )
    max_box = (
        max(box_rotate, key=lambda p: p[0])[0],
        max(box_rotate, key=lambda p: p[1])[1],
    )

    origin = pygame.math.Vector2(pos[0] + min_box[0], pos[1] - max_box[1])
    rotated_image = pygame.transform.rotate(image, angle)

    return rotated_image, origin


class Tank(pygame.sprite.Sprite):
    @classmethod
    def load_image(cls, fn):
        """Load a sprite image to be used in tank instantances."""
        img = pygame.image.load(fn)
        return img.convert_alpha()

    def __init__(self, body, gun):
        super(Tank, self).__init__()

        # start tank here, probably should be an argument
        self.pos = pygame.math.Vector2(100, 100)

        # keep original images because rotation is lossey
        self.body = body
        self.body_orig = body.copy()
        self.gun = gun
        self.gun_orig = gun.copy()

        # pivot relative to top left of tank body image body.  The 0.75 should
        # be a parameter of the tank definition.
        self.gpivot = pygame.math.Vector2(gun.get_width() / 2, gun.get_height() * 0.75)

        # start facing north
        self.body_angle = 0
        self.gun_angle = 0

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.pos.y -= 5
        if pressed_keys[K_DOWN]:
            self.pos.y += 5
        if pressed_keys[K_LEFT]:
            self.pos.x -= 5
        if pressed_keys[K_RIGHT]:
            self.pos.x += 5
        if pressed_keys[K_r]:
            self.body_angle += 1
            self.body = pygame.transform.rotate(self.body_orig, self.body_angle)
        if pressed_keys[K_t]:
            self.gun_angle += 1

    def draw(self, sur):
        sur.blit(self.body, self.pos - self.body.get_rect().center)

        # offset from pivot to center
        image_rect = self.gun_orig.get_rect(topleft=self.pos - self.gpivot)
        offset_center_to_pivot = self.pos - image_rect.center

        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(
            -(self.gun_angle + self.body_angle)
        )

        rotated_image_center = self.pos - rotated_offset

        # get a rotated image
        rotated_image = pygame.transform.rotate(
            self.gun_orig, self.gun_angle + self.body_angle
        )
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        # rotate and blit the image
        sur.blit(rotated_image, rotated_image_rect.topleft)


pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.RESIZABLE)
fake_screen = screen.copy()

b = Tank.load_image("../assets/tanks/basic_body.png")
b = pygame.transform.smoothscale(
    b, (int(0.5 * b.get_rect().width), int(0.5 * b.get_rect().height))
)
g = Tank.load_image("../assets/tanks/basic_gun.png")
g = pygame.transform.smoothscale(
    g, (int(0.5 * g.get_rect().width), int(0.5 * g.get_rect().height))
)
tank = Tank(b, g)
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

    # Fill the background with black
    fake_screen.fill((0, 0, 0))

    pygame.draw.rect(fake_screen, (0, 0, 255), (0, 0, 100, 100))
    tank.update(pygame.key.get_pressed())

    tank.draw(fake_screen)
    # pygame.draw.rect(fake_screen, (0, 0, 255), (0, 0, 200, 200))

    # # for e in all_sprites:
    # # fake_screen.blit(tank.image, tank.location)
    # x, y = tank.image.get_rect().center
    # fake_screen.blit(tank.image, (100 - x, 100 - y))

    # rotated_image = pygame.transform.rotate(tank.image, 45)
    # x, y = rotated_image.get_rect().center
    # fake_screen.blit(rotated_image, (100 - x, 100 - y))

    # rotated_image = pygame.transform.rotate(tank.image, 20)
    # x, y = rotated_image.get_rect().center
    # fake_screen.blit(rotated_image, (100 - x, 100 - y))

    screen.blit(pygame.transform.scale(fake_screen, screen.get_rect().size), (0, 0))

    clock.tick(60)
    # Flip the display
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()
