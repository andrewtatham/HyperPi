import os
import pygame
import sys
import platform
import random
import math


def rotate(vector):
    angle = 180 + math.atan2(vector[0], vector[1]) * 180 / math.pi
    return angle


def random_position():
    return [
        random.randint(0, width),
        random.randint(0, height)
    ]


def random_speed():
    return [
        random.randint(-5, 5),
        random.randint(-5, 5)
    ]


def initialize():
    global black, screen

    _platform = platform.platform()
    print(_platform)
    is_linux = _platform.startswith('Linux')
    _node = platform.node()
    print(_node)
    is_full_screen = is_linux

    display_flags = 0
    if is_full_screen:
        display_flags += pygame.FULLSCREEN
    screen = pygame.display.set_mode(size, display_flags)


class Sprite(object):
    def __init__(self, image_path, origin, speed):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move([origin[0], origin[1]])
        self.speed = speed

    def move(self):
        self.rect = self.rect.move(self.speed)

    def check_collide_sprite(self, other):
        if self.is_collision(other):
            self.collide_sprite(other)

    def is_collision(self, other):
        left = self.rect.left < other.rect.right
        right = self.rect.right > other.rect.left
        top = self.rect.top < other.rect.bottom
        bottom = self.rect.bottom > other.rect.top
        is_collision = left and right and top and bottom
        return is_collision

    def collide_sprite(self, other):
        pass

    def collide_left_edge(self):
        self.rect.left = 0
        self.bounce_horizontal()

    def collide_right_edge(self):
        self.rect.right = width
        self.bounce_horizontal()

    def collide_top_edge(self):
        self.rect.top = 0
        self.bounce_vertical()

    def collide_bottom_edge(self):
        self.rect.bottom = height
        self.bounce_vertical()

    def bounce_horizontal(self):
        self.speed[0] = -self.speed[0]

    def bounce_vertical(self):
        self.speed[1] = -self.speed[1]

    def check_collide_edges(self, width, height):
        if self.rect.left < 0:
            self.collide_left_edge()
        if self.rect.right > width:
            self.collide_right_edge()
        if self.rect.top < 0:
            self.collide_top_edge()
        if self.rect.bottom > height:
            self.collide_bottom_edge()

    def display(self, surface):
        surface.blit(self.image, self.rect)

    def kill(self):
        all_sprites.remove(self)


class SpriteGroup(object):
    def __init__(self, sprites=[]):
        self._sprites = []
        self._sprites.extend(sprites)

    def extend(self, sprites):
        self._sprites.extend(sprites)

    def __iter__(self):
        return self._sprites.__iter__()

    def remove(self, sprite):
        if sprite in self._sprites:
            self._sprites.remove(sprite)

    def add(self, bullet):
        self._sprites.append(bullet)


class NonPlayer(Sprite):
    pass


class Player(Sprite):
    pass


class Asteroid(NonPlayer):
    def __init__(self):

        self.animation_frame = random.randint(0, 58)

        Sprite.__init__(
            self,
            os.path.join("images", "Asteroid-A-10-59", "Asteroid-A-10-00.png"),
            random_position(),
            random_speed())

    def collide_sprite(self, other):
        # if other in asteriods:
        #     self.kill()
        if other in bullets:
            self.kill()
        pass

    def display(self, surface):
        self.image = asteroid_frames[self.animation_frame]
        self.animation_frame += 1
        if self.animation_frame > 58:
            self.animation_frame = 0
        Sprite.display(self, surface)


class Bullet(NonPlayer):
    def __init__(self, origin, speed):
        Sprite.__init__(
            self,
            os.path.join("images", "magic-missile.png"),
            origin,
            speed)

    def collide_sprite(self, other):
        if other in asteriods:
            self.kill()
        pass


class Ship(Player):
    def __init__(self):
        self.original_image = pygame.image.load(os.path.join("images", "DurrrSpaceShip_2.png"))
        Sprite.__init__(
            self,
            os.path.join("images", "DurrrSpaceShip_2.png"),
            random_position(),
            random_speed())

    def collide_sprite(self, other):
        # if other in asteriods:
        #     self.kill()
        pass

    def fire(self):
        origin = self.rect
        bullet = Bullet(origin, random_speed())
        bullets.add(bullet)
        all_sprites.add(bullet)

    def display(self, surface):
        angle = rotate(self.speed)
        self.image = pygame.transform.rotate(self.original_image, angle)
        Sprite.display(self, surface)

    def change_speed(self):
        self.speed = random_speed()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 480
    black = 0, 0, 0
    clock = pygame.time.Clock()
    asteroid_frames = []
    for i in range(0, 59):
        name = "Asteroid-A-10-{0:02d}.png".format(i)
        path = os.path.join("images", "Asteroid-A-10-59", name)
        image = pygame.image.load(path)
        asteroid_frames.append(image)

    initialize()

    all_sprites = SpriteGroup([

    ])

    asteriods = SpriteGroup([
        Asteroid(),
        Asteroid(),
        Asteroid(),
        Asteroid(),
        Asteroid(),
        Asteroid(),
        Asteroid(),
        Asteroid(),
        Asteroid(),
        Asteroid(),
        Asteroid(),
        Asteroid(),
        Asteroid()
    ])
    bullets = SpriteGroup([

    ])

    player1 = Ship()
    players = SpriteGroup([
        player1
    ])

    all_sprites.extend(asteriods)
    all_sprites.extend(bullets)
    all_sprites.extend(players)

    frame = 0
    while 1:
        frame += 1
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

        for sprite in all_sprites:
            sprite.move()

        if frame % 30 == 0:
            player1.fire()

        if frame % 120 == 0:
            player1.change_speed()
        if frame % 15 == 0:
            asteroid = Asteroid()
            asteriods.add(asteroid)
            all_sprites.add(asteroid)

        for sprite_a in all_sprites:
            for sprite_b in all_sprites:
                if sprite_a != sprite_b:
                    sprite_a.check_collide_sprite(sprite_b)
            sprite_a.check_collide_edges(width, height)

        screen.fill(black)
        for sprite in all_sprites:
            sprite.display(screen)
        pygame.display.flip()
        clock.tick(60)
