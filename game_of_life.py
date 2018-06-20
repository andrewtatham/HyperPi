import pprint
import random
from time import sleep
from random import randint
import pygame
from pygame.rect import Rect

pygame.init()

# The screen size in pixels
screen_x = 800
screen_y = 600  # Height of screen in pixels
screen = pygame.display.set_mode((screen_x, screen_y), 0, 24)  # New 24-bit screen

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


def one_in(n):
    return random.randint(0, n) == 0


class Cell(object):
    def __init__(self, x, y, alive):
        self.x = x
        self.y = y
        self.x_pixels = x * cell_x
        self.y_pixels = y * cell_y
        self.top_left = [self.x_pixels, self.y_pixels]
        self.bottom_right = [self.x_pixels + cell_x, self.y_pixels + cell_y]
        self.rect = Rect(self.top_left, self.bottom_right)
        self.is_alive = alive
        self.was_alive = alive
        self.neighbours = None

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def before_evolve(self):
        self.was_alive = self.is_alive

    def evolve(self):
        alive_neighbour_count = sum(map(lambda n: n.was_alive, self.neighbours))
        self.is_alive = (self.was_alive and 2 <= alive_neighbour_count <= 3) \
                        or (not self.was_alive and alive_neighbour_count == 3)


    def render(self, force=False):
        changed = self.is_alive != self.was_alive
        if changed or force:
            if self.is_alive:
                colour = GREEN
            else:
                colour = BLACK
            pygame.draw.rect(screen, colour, self.rect, 0)

    def is_collision(self, pos):
        return self.rect.collidepoint(pos)

    def on_click(self):
        print("on_click")
        self.is_alive = not self.is_alive
        self.render(force=True)


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
                # Remove offscreen cells
                # neighbour_cell_positions = list(filter(
                #    lambda other: 0 <= other[0] < n_cells_x and 0 <= other[1] < n_cells_y, neighbour_cell_positions))
                neighbours = list(
                    map(lambda other: self.cells[other[0] % n_cells_x][other[1] % n_cells_y], neighbour_cell_positions))
                self.cells[x][y].set_neighbours(neighbours)

    def evolve(self):
        for x in range(n_cells_x):
            for y in range(n_cells_y):
                self.cells[x][y].before_evolve()
        for x in range(n_cells_x):
            for y in range(n_cells_y):
                self.cells[x][y].evolve()

    def render(self, force=False):
        for x in range(n_cells_x):
            for y in range(n_cells_y):
                self.cells[x][y].render(force)

    def handle_click(self, position):
        for x in range(n_cells_x):
            for y in range(n_cells_y):
                cell = self.cells[x][y]
                if cell.is_collision(position):
                    cell.on_click()


class GameOfLife(object):
    def __init__(self):

        init_alive = [[0 for _ in range(n_cells_y)] for _ in range(n_cells_x)]

        for x in range(n_cells_x):
            for y in range(n_cells_y):
                init_alive[x][y] = one_in(10)

        self.grid = Grid(init_alive)
        self.clock = pygame.time.Clock()

    def run(self, fps=60):
        # force initial render for first frame

        self.grid.render(force=True)
        pygame.display.flip()
        self.clock.tick(fps)
        done = False
        while not done:
            self.grid.evolve()
            self.grid.render(force=True)
            pygame.display.flip()
            self.clock.tick(fps)
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    position = pygame.mouse.get_pos()
                    self.grid.handle_click(position)


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
