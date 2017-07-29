import pprint

import pygame
import pygame.camera
from pygame.locals import *

DEVICE = '/dev/video0'
screen_size = (800, 480)
camera_size = (1280, 720)
FILENAME = 'capture.png'


def camstream():
    pygame.init()
    pygame.camera.init()

    pprint.pprint(pygame.camera.list_cameras())

    display = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    camera = pygame.camera.Camera(DEVICE, camera_size)
    camera.start()

    actual_camera_size = camera.get_size()
    pprint.pprint(actual_camera_size)

    screen = pygame.surface.Surface(screen_size, 0, display)
    frame = pygame.surface.Surface(camera_size, 0, display)
    capture = True
    while capture:
        frame = camera.get_image(frame)
        screen = pygame.transform.scale(frame, screen_size, screen)
        screen = pygame.transform.flip(screen, True, False)
        display.blit(screen, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_s:
                    capture = False
                elif event.type == KEYDOWN:
                    if event.key == K_s:
                        pygame.image.save(screen, FILENAME)
                    elif event.key == K_q:
                        capture = False
    camera.stop()
    pygame.quit()
    return


if __name__ == '__main__':
    camstream()
