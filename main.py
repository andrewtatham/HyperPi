import pygame
import sys
import platform

pygame.init()

size = width, height = 800, 480

_platform = platform.platform()
print(_platform)
is_windows = _platform.startswith('Windows')
is_mac_osx = _platform.startswith('Darwin')
is_linux = _platform.startswith('Linux')

_node = platform.node()
print(_node)
is_andrew_desktop = _node == "ANDREWDESKTOP"
is_andrew_laptop = _node == "ANDREWLAPTOP"
is_raspberry_pi = _node == "raspberrypi"
is_raspberry_pi_2 = _node == "raspberrypi2"
is_andrew_macbook = _node == "Andrews-MacBook-Pro.local"
is_scroll_bot = _node == "scrollbot"

is_full_screen = is_linux
speed = [2, 2]
black = 0, 0, 0
display_flags = 0
if is_full_screen:
    display_flags += pygame.FULLSCREEN
screen = pygame.display.set_mode(size, display_flags)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pygame.display.toggle_fullscreen()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
