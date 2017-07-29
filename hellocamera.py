import pprint

import pygame
import pygame.camera
from pygame.locals import *

DEVICE = '/dev/video0'
SIZE = (800, 480)
FILENAME = 'capture.png'


def camstream():
    pygame.init()
    pygame.camera.init()

    pprint.pprint(pygame.camera.list_cameras())

    display = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
    camera = pygame.camera.Camera(DEVICE, SIZE)
    camera.start()

    actual_camera_size = camera.get_size()
    pprint.pprint(actual_camera_size)

    screen = pygame.surface.Surface(SIZE, 0, display)
    capture = True
    while capture:
        screen = camera.get_image(screen)
        display.blit(screen, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                capture = False
            elif event.type == KEYDOWN and event.key == K_s:
                pygame.image.save(screen, FILENAME)
    camera.stop()
    pygame.quit()
    return


if __name__ == '__main__':
    camstream()