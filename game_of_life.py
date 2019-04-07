import collections
import platform
import random
import statistics

import psutil
import pygame
from pygame.rect import Rect

pygame.init()
clock = pygame.time.Clock()

min_fps = 1
max_fps = 60
fps = 30

max_cpu = 25
min_cpu = 5

# The screen size in pixels
screen_x = 800
screen_y = 480  # Height of screen in pixels

_platform = platform.platform()
print(_platform)
is_linux = _platform.startswith('Linux')
_node = platform.node()
print(_node)
is_full_screen = is_linux

display_flags = 0
if is_full_screen:
    display_flags += pygame.FULLSCREEN
screen = pygame.display.set_mode((screen_x, screen_y), display_flags)

# The size of each cell in pixels
cell_x = 16
cell_y = 12

# the number of cells in each direction
n_cells_x = int(screen_x / cell_x)
n_cells_y = int(screen_y / cell_y)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def one_in(n):
    return random.randint(0, n) == 0


def all_same(items):
    return all(x == items[0] for x in items)


class Cell(object):
    def __init__(self, x, y, alive):
        self.x = x
        self.y = y
        self.x_pixels = x * cell_x
        self.y_pixels = y * cell_y

        self.rect = Rect(self.x_pixels, self.y_pixels, cell_x, cell_y)

        self.is_alive = alive
        self.was_alive = alive
        self.changed = False
        self.age = 0

        self.neighbours = None

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def before_evolve(self):
        self.changed = False
        self.was_alive = self.is_alive

    def evolve(self):
        alive_neighbour_count = sum(map(lambda n: n.was_alive, self.neighbours))
        self.is_alive = (self.was_alive and 2 <= alive_neighbour_count <= 3) \
                        or (not self.was_alive and alive_neighbour_count == 3)
        self.changed = self.is_alive != self.was_alive
        if self.changed:
            self.age = 0
        else:
            self.age += 1
        return self.changed

    def render(self, colour=None):
        if not colour:
            if self.is_alive:
                if self.age < 2:
                    colour = GREEN
                elif self.age < 4:
                    colour = YELLOW
                else:
                    colour = RED
            else:
                colour = BLACK
        pygame.draw.rect(screen, colour, self.rect, 0)

    def is_collision(self, pos):
        collision = self.rect.collidepoint(pos)
        return collision

    def on_click(self):
        self.toggle()

    def toggle(self):
        self.is_alive = not self.is_alive


class Grid(object):
    def __init__(self, init_alive):

        self.cells = [[Cell(x, y, init_alive[x][y]) for y in range(n_cells_y)] for x in range(n_cells_x)]

        for x in range(n_cells_x):
            for y in range(n_cells_y):
                neighbour_cell_positions = [
                    (x - 1, y - 1), (x - 1, y + 0), (x - 1, y + 1),
                    (x + 0, y - 1), (x + 0, y + 1),
                    (x + 1, y - 1), (x + 1, y + 0), (x + 1, y + 1)
                ]
                neighbours = list(
                    map(lambda other: self.cells[other[0] % n_cells_x][other[1] % n_cells_y], neighbour_cell_positions))
                self.cells[x][y].set_neighbours(neighbours)

    def evolve(self):
        for x in range(n_cells_x):
            for y in range(n_cells_y):
                self.cells[x][y].before_evolve()
        n_changed = 0
        for x in range(n_cells_x):
            for y in range(n_cells_y):
                n_changed += self.cells[x][y].evolve()
        return n_changed

    def render(self):
        for x in range(n_cells_x):
            for y in range(n_cells_y):
                self.cells[x][y].render()
        pygame.display.flip()
        clock.tick(fps)

    def handle_click(self, position):
        for x in range(n_cells_x):
            for y in range(n_cells_y):
                cell = self.cells[x][y]
                if cell.is_collision(position):
                    cell.on_click()

    def add_noise(self, n):
        for _ in range(n):
            cell = self.get_random_cell()
            cell.toggle()

    def get_random_cell(self):
        x = random.randint(0, n_cells_x - 1)
        y = random.randint(0, n_cells_y - 1)
        cell = self.cells[x][y]
        return cell


class GameOfLife(object):
    def __init__(self):

        init_alive = [[0 for _ in range(n_cells_y)] for _ in range(n_cells_x)]

        # for x in range(n_cells_x):
        #     for y in range(n_cells_y):
        #         init_alive[x][y] = one_in(6)

        self.grid = Grid(init_alive)

    def run(self):
        global fps
        self.grid.render()
        done = False
        activity_monitor = collections.deque(maxlen=5)
        cpu_monitor = collections.deque(maxlen=30)
        while not done:
            n_changed = self.grid.evolve()

            cpu_percent = psutil.cpu_percent()
            cpu_monitor.append(cpu_percent)
            mean_cpu = statistics.mean(cpu_monitor)
            print("fps: {}, cpu: {}, avg: {}".format(fps, cpu_percent, mean_cpu))
            if mean_cpu > max_cpu and fps > min_fps:
                fps -= 1
            elif mean_cpu < min_cpu and fps < max_fps:
                fps += 1

            activity_monitor.append(n_changed)
            if all_same(activity_monitor):
                self.grid.add_noise(int(n_cells_y * n_cells_y / 3))

            self.grid.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    self.grid.handle_click(position)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        done = True


def main():
    gol = GameOfLife()
    try:
        gol.run()
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
