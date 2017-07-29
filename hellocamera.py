import pprint

import pygame
import pygame.camera
from pygame.locals import *

DEVICE = '/dev/video0'
screen_size = (800, 480)
camera_size = (1280, 720)
detect_size = (800, 480)
FILENAME = 'capture.png'


def camstream():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.camera.init()

    pprint.pprint(pygame.camera.list_cameras())

    display = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    camera = pygame.camera.Camera(DEVICE, camera_size)
    camera.start()

    actual_camera_size = camera.get_size()
    pprint.pprint(actual_camera_size)

    screen = pygame.surface.Surface(screen_size, 0, display)
    frame = pygame.surface.Surface(camera_size, 0, display)
    detect = pygame.surface.Surface(detect_size, 0, display)
    capture = True
    while capture:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_s:
                    capture = False
                elif event.type == KEYDOWN:
                    if event.key == K_s:
                        pygame.image.save(screen, FILENAME)
                    elif event.key == K_q:
                        capture = False
        if camera.query_image():
            camera.get_image(frame)

            pygame.transform.scale(frame, screen_size, screen)
            pygame.transform.flip(screen, True, False)

            pygame.transform.scale(screen, detect_size, detect)
            pygame.camera.colorspace(detect, "HSV", detect)
            # pygame.transform.threshold(detect, detect, (0, 255, 0), (90, 170, 170), (0, 0, 0), 2)
            # display.blit(screen, (0, 0))
            display.blit(detect, (0, 0))
        pygame.display.flip()
        dt = clock.tick(60)

    camera.stop()
    pygame.quit()
    return


if __name__ == '__main__':
    camstream()
