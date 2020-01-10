import random
import pygame


class Conway:

    def __init__(self, x, n, start_size):
        pygame.init()
        window_size = [x * 3, x * 3]
        black = (0, 0, 0)
        green = (34, 139, 34)
        self.n = n
        self.start_size = start_size
        self.dead = black
        self.alive = green
        self.width = 2
        self.height = 2
        self.margin = 1
        self.grid = self.random_square(self.make_grid(x))
        pygame.display.set_caption('Simple Conway')
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.clock.tick(60)

    @staticmethod
    def make_grid(x):
        #creates a square grid of size x
        grid = [[False for _ in range(x)] for _ in range(x)]
        return grid

    def random_square(self, grid):
        #creates a square of random true or false vales, start_size is a divisor of total grid size
        placement = int((len(grid) /  2) - ((len(grid) / self.start_size) / 2))
        for x in range(int(len(grid) / self.start_size)):
            for y in range(int(len(grid) / self.start_size)):
                grid[x + placement][y + placement] = random.choice([True, False])
        return grid

    @staticmethod
    def check_neighbors(grid, x, y):
        #check a specific coord to return sum of 8 neighbors alive/dead status
        #first part allows grid to wrap into toroid shape or donut shape (no edges!)
        values = [x - 1, y - 1, x + 1, y + 1]
        for i in range(len(values)):
            if values[i] < 0:
                values[i] = len(grid) - 1
            elif values[i] > len(grid) - 1:
                values[i] = 0
        #true/false status of all neighbors is collected
        neighbors = [grid[values[0]][values[1]],  # First Row
                     grid[values[0]][y],  # First Row
                     grid[values[0]][values[3]],  # First Row
                     grid[x][values[1]],  # Second Row
                     grid[x][values[3]],  # Second Row
                     grid[values[2]][values[1]],  # Third Row
                     grid[values[2]][y],  # Third Row
                     grid[values[2]][values[3]]]  # Third Row
        return neighbors.count(True)

    def alive_or_dead(self, grid):
        #iterates through grid and returns updated grid for next tick
        new_grid = self.make_grid(len(grid))
        for x in range(len(grid)):
            for y in range(len(grid)):
                a_or_d = self.check_neighbors(grid, x, y)
                if not grid[x][y]:
                    if a_or_d == 3:
                        new_grid[x][y] = True
                    else:
                        new_grid[x][y] = False
                else:
                    if a_or_d < 2:
                        new_grid[x][y] = False
                    elif a_or_d == 2 or a_or_d == 3:
                        new_grid[x][y] = True
                    else:
                        new_grid[x][y] = False
        return new_grid

    def mouse_event(self, grid):
        #returns mouse input as alive cells
        pos = pygame.mouse.get_pos()
        try:
            column = pos[0] // (self.width + self.margin)
            row = pos[1] // (self.height + self.margin)
            grid[row][column] = True
        except IndexError:
            pass
        return grid

    def pause_event(self, grid):
        #pauses game until space bar pressed again
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    grid = self.mouse_event(grid)
                elif event.type == pygame.KEYDOWN:
                    if event.key == 32:
                        return grid
                self.draw_screen(grid)

    def draw_screen(self, grid):
        #updates the screen every tick
        self.screen.fill(self.dead)
        for row in range(len(grid)):
            for column in range(len(grid)):
                rect_measurements = [(self.margin + self.width) * column + self.margin,
                                     (self.margin + self.height) * row + self.margin,
                                      self.width, self.height]
                if grid[row][column]:
                    color = self.alive
                else:
                    color = self.dead
                pygame.draw.rect(self.screen, color, rect_measurements)
        pygame.display.flip()

    def main_loop(self):
        #game loop that handles number of iterations and events
        grid = self.grid
        n = self.n
        for i in range(n):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    grid = self.mouse_event(grid)
                elif event.type == pygame.KEYDOWN:
                    if event.key == 32:
                        grid = self.pause_event(grid)
            self.draw_screen(grid)
            grid = self.alive_or_dead(grid)


if __name__ == '__main__':
    #inputs are grid size, number of generations, and starting square divisor
    conway = Conway(200, 100000, 4)
    conway.main_loop()
