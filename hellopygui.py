import os
import pygame
import sys
import platform
import random
import math

from pygame.sprite import Sprite, Group

size = width, height = 800, 480
black = 0, 0, 0
red = 255, 0, 0
blue = 0, 255, 0
green = 0, 0, 255
screen = None
clock = None


class ButtonGroup(Group):
    def __init__(self):
        super(ButtonGroup, self).__init__()


class Button(Sprite):
    def __init__(self):
        super(Button, self).__init__()
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([64, 64])
        self.image.fill(red)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()


class CircularButton(Button):
    pass


def initialize():
    global screen, clock

    _platform = platform.platform()
    print(_platform)
    is_linux = _platform.startswith('Linux')
    _node = platform.node()
    print(_node)
    is_full_screen = is_linux

    pygame.init()

    clock = pygame.time.Clock()
    display_flags = 0
    if is_full_screen:
        display_flags += pygame.FULLSCREEN

    screen = pygame.display.set_mode(size, display_flags)


if __name__ == '__main__':
    initialize()

    buttons = ButtonGroup()

    a = CircularButton()
    b = CircularButton()

    buttons.add(a, b)

    while 1:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.display.toggle_fullscreen()

        screen.fill(black)
        buttons.draw(screen)

        pygame.display.flip()
        clock.tick(10)
