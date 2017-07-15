import pygame
import sys
import platform


class Sprite(object):
    def __init__(self, image_path, speed):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.speed = speed

    def move(self):
        self.rect = self.rect.move(self.speed)

    def check_collide_sprite(self, sprite_b):
        pass

    def collide_sprite(self, other):
        pass

    def collide_left(self):
        self.bounce_horizontal()

    def collide_right(self):
        self.bounce_horizontal()

    def collide_top(self):
        self.bounce_vertical()

    def collide_bottom(self):
        self.bounce_vertical()

    def bounce_horizontal(self):
        self.speed[0] = -self.speed[0]

    def bounce_vertical(self):
        self.speed[1] = -self.speed[1]

    def check_collide_edges(self, width, height):
        if self.rect.left < 0:
            self.collide_left()
        if self.rect.right > width:
            self.collide_right()
        if self.rect.top < 0:
            self.collide_top()
        if self.rect.bottom > height:
            self.collide_bottom()

    def display(self, surface):
        surface.blit(self.image, self.rect)


sprites = [
    Sprite("intro_ball.gif", [1, 2]),
    Sprite("intro_ball.gif", [2, 1])
]

pygame.init()
size = width, height = 800, 480

def initialize():
    global black, screen

    _platform = platform.platform()
    print(_platform)
    # is_windows = _platform.startswith('Windows')
    # is_mac_osx = _platform.startswith('Darwin')
    is_linux = _platform.startswith('Linux')
    _node = platform.node()
    print(_node)
    # is_andrew_desktop = _node == "ANDREWDESKTOP"
    # is_andrew_laptop = _node == "ANDREWLAPTOP"
    # is_raspberry_pi = _node == "raspberrypi"
    # is_raspberry_pi_2 = _node == "raspberrypi2"
    # is_andrew_macbook = _node == "Andrews-MacBook-Pro.local"
    # is_scroll_bot = _node == "scrollbot"
    is_full_screen = is_linux
    black = 0, 0, 0
    display_flags = 0
    if is_full_screen:
        display_flags += pygame.FULLSCREEN
    screen = pygame.display.set_mode(size, display_flags)


initialize()

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

    for sprite in sprites:
        sprite.move()

    for sprite_a in sprites:
        for sprite_b in sprites:
            if sprite_a != sprite_b:
                sprite_a.check_collide_sprite(sprite_b)
        sprite_a.check_collide_edges(width, height)

    screen.fill(black)
    for sprite in sprites:
        sprite.display(screen)
    pygame.display.flip()
