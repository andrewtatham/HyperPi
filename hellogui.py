import os
import pygame
import sys
import platform
import random
import math

size = width, height = 800, 480
black = 0, 0, 0
screen = None
clock = None


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
    all_sprites = []
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
        for sprite in all_sprites:
            sprite.display(screen)
        pygame.display.flip()
        clock.tick(60)
