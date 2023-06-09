#!/usr/bin/python3
# https://realpython.com/pygame-a-primer/

import math
import pygame
import pygame.freetype

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    K_f,
    K_d,
    K_j,
    K_k,
    K_s,
    K_l,
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

    def __init__(self, body, gun):
        super(Tank, self).__init__()

        self.mass = 4
        self.friction = 10

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

        # start facing north, 90 is east
        self.body_angle = 0
        self.gun_angle = 0

        # start out zero velocity and torque
        # we have a bunch of torque vs velocity curves.  Depending on power
        self.vel = [0, 0]
        self.torque = [0, 0]
        self.power = [0, 0]
        # power goes from -300 to 300 say.  Let
        #
        #  T = -v + power if power >= 0
        #  T = -v - power if power <= 0
        #
        # and limit
        # Using T = ma, we get the acceleration, so can modify the velocity
        # using
        #
        #  vnew = vold + a dt
        #       = vold + (T/m) dt

    def update(self, pressed_keys):
        if pressed_keys[K_f]:
            self.power[0] += 2
        elif pressed_keys[K_d]:
            self.power[0] -= 2
        else:  # no f or d, so just reduce the power
            if self.power[0] < 0:
                self.power[0] += 4
            elif self.power[0] > 0:
                self.power[0] -= 4

        if pressed_keys[K_j]:
            self.power[1] += 2
        elif pressed_keys[K_k]:
            self.power[1] -= 2
        else:  # no j or k, so just reduce the power
            if self.power[1] < 0:
                self.power[1] += 4
            elif self.power[1] > 0:
                self.power[1] -= 4

        for i in 0, 1:
            self.power[i] = min(100, max(-100, self.power[i]))

        for i in 0, 1:
            self.torque[i] = self.power[i]  # - self.vel[i]

        # for i in 0, 1:
        #     if self.power[i] > 0:
        #         self.torque[i] = min(self.power[i], max(0, self.torque[i]))
        #     else:
        #         self.torque[i] = min(0, max(self.power[i], self.torque[i]))

        for i in 0, 1:
            force = self.torque[i] - self.friction * self.vel[i]
            self.vel[i] += force / self.mass * dt

        # the difference in left and right velocities rotates body
        self.body_angle += (self.vel[0] - self.vel[1]) / 10
        self.body = pygame.transform.rotate(self.body_orig, -self.body_angle)

        # move the average of our velocities in the angle direction
        vel = (self.vel[0] + self.vel[1]) / 2
        self.pos.x += vel * math.sin(math.radians(self.body_angle))
        self.pos.y -= vel * math.cos(math.radians(self.body_angle))

        if pressed_keys[K_s]:
            self.gun_angle -= 1
        if pressed_keys[K_l]:
            self.gun_angle += 1

    def draw(self, sur):
        sur.blit(self.body, self.pos - self.body.get_rect().center)

        # offset from pivot to center
        image_rect = self.gun_orig.get_rect(topleft=self.pos - self.gpivot)
        offset_center_to_pivot = self.pos - image_rect.center

        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(
            (self.gun_angle + self.body_angle)
        )

        rotated_image_center = self.pos - rotated_offset

        # get a rotated image
        rotated_image = pygame.transform.rotate(
            self.gun_orig, -(self.gun_angle + self.body_angle)
        )
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        # rotate and blit the image
        sur.blit(rotated_image, rotated_image_rect.topleft)


pygame.init()
my_font = pygame.freetype.SysFont("arial", 30)

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
dt = 1 / 60

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

    my_font.render_to(
        fake_screen,
        (400, 400),
        f"P: {tank.power[0]:3d}, {tank.power[1]:3d}",
        fgcolor=(255, 255, 255),
    )
    my_font.render_to(
        fake_screen,
        (400, 450),
        f"T: {int(tank.torque[0]):3d}, {int(tank.torque[1]):3d}",
        fgcolor=(255, 255, 255),
    )
    my_font.render_to(
        fake_screen,
        (400, 500),
        f"V: {int(tank.vel[0]):3d}, {int(tank.vel[1]):3d}",
        fgcolor=(255, 255, 255),
    )
    my_font.render_to(
        fake_screen,
        (400, 550),
        f"Angle: {int(tank.body_angle):3d}",
        fgcolor=(255, 255, 255),
    )

    screen.blit(pygame.transform.scale(fake_screen, screen.get_rect().size), (0, 0))

    clock.tick(60)
    # Flip the display
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()
