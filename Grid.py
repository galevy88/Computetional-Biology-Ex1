import pygame
import numpy as np
import random
from Cell import Cell
import Globals
import queue


class Grid:
    def __init__(self):
        self.q = queue.Queue()
        self.hold_q = queue.Queue()
        self.clock = pygame.time.Clock()

        # Set grid size and population density
        self.grid_size = Globals.GRID_SIZE
        self.population_density = Globals.POP_DENSITY

        # Set levels of skepticism
        self.skepticism_levels = ['S1', 'S2', 'S3', 'S4']
        self.transmission_probability = Globals.transmission_probability
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Grid Display')
        self.font = pygame.font.SysFont('Arial', 14)
        self.create_grid()
        self.running = True
        self.grid
        self.generation_data = []

    def create_grid(self):
        # Create a grid of size grid_size x grid_size with skepticism levels assigned randomly
        self.grid = np.empty((self.grid_size, self.grid_size), dtype=object)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.grid[i, j] = Cell((i, j), 'X', None)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if random.random() < self.population_density:
                    skepticism_level = np.random.choice(self.skepticism_levels, p=Globals.probs)
                    self.grid[i, j].type = skepticism_level
                    self.grid[i, j].rumor_prob = Globals.transmission_probability.get(skepticism_level, None)
                    self.grid[i, j].original_params["type"] = skepticism_level
                    self.grid[i, j].original_params["rumor_prob"] = Globals.transmission_probability.get(skepticism_level, None)

    def start(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Grid Display")
        first_iteration = True
        gen = 1
        while self.running:
            gen+=1
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            if first_iteration:
                chosen_cell = self.get_random_cell()
                status = chosen_cell.recieve_rumor()
                while not status:
                    chosen_cell = self.get_random_cell()
                    status = chosen_cell.recieve_rumor()
                neighbors = chosen_cell.get_neighbors(self.grid)
                cells_for_next_generation = self.spread_rumor(neighbors)
                for c in cells_for_next_generation:
                    self.q.put(c)
                first_iteration = False
            
            cells_for_next_generation = []
            hold_cells = []
            while not self.q.empty():
                current_cell = self.q.get()
                neighbors = current_cell.get_neighbors(self.grid)
                cells_for_next_generation.extend(self.spread_rumor(neighbors))
                hold_cells.append(current_cell)
            for c in cells_for_next_generation:
                if c not in self.q.queue:
                    if c.L < 1:
                        self.q.put(c)
                        c.L = Globals.COOL_DOWN
                        cells_for_next_generation.remove(c)
            for c in hold_cells:
                if c not in self.q.queue and c.L < 1:
                    self.q.put(c)
                    c.L = 0
                    hold_cells.remove(c)
            size = self.apply_new_generation()
            self.display_grid(self.screen, gen, size)
            pygame.display.flip()
            self.generation_data.append((gen, size))
            if self.check_for_convergence(self.generation_data):
                return self.generation_data

                

        pygame.quit()
    
    def check_for_convergence(self, generation_data):
        """
        Check if the queue size is the same for 20 generations in a row
        """
        if len(generation_data) < 20:
            return False
            
        queue_sizes = [data[1] for data in generation_data[-20:]]
        if len(set(queue_sizes)) != 1:
            return False
            
        return True



    def display_grid(self, screen, gen, size):
        screen.fill(pygame.Color('black'))
        # Calculate cell size and padding to center grid on screen
        cell_size = 600 // self.grid_size
        screen_padding = (800 - cell_size * self.grid_size) // 2

        # Create a list of rectangles that need to be updated
        dirty_rects = []

        # Display grid on screen
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0 = j * cell_size + screen_padding
                y0 = i * cell_size + screen_padding + 10
                color = {'S1': 'red', 'S2': 'orange', 'S3': 'green', 'S4': 'blue'}.get(self.grid[i, j].type, 'black')
                pygame.draw.rect(screen, pygame.Color(color), (x0, y0, cell_size, cell_size))
                dirty_rects.append(pygame.Rect(x0, y0, cell_size, cell_size))

                # Add rumor indicator if the cell has received a rumor
                if self.grid[i, j].rumor_received:
                    x_w = x0 + cell_size//2
                    y_w = y0 + cell_size//4
                    las = 3
                    pygame.draw.circle(screen, pygame.Color('white'), (x_w,y_w), las)
                    dirty_rects.append(pygame.Rect(x_w-las, y_w-las, las*2, las*2))

        # Display current parameter values on screen
        settings_text = f"Grid Size: {self.grid_size}\nPopulation Density: {self.population_density}\n" \
                        f"Skepticism Levels: {Globals.probs}\nCool Down Level: {Globals.COOL_DOWN}"
        settings_lines = settings_text.split('\n')
        for i, line in enumerate(settings_lines):
            line_surface = self.font.render(line, True, pygame.Color('white'))
            screen.blit(line_surface, (30, 30 + i * 20))
            dirty_rects.append(line_surface.get_rect(topleft=(30, 30 + i * 20)))

        status_text = f"Generation: {gen}\nRecieved Rumor: {size}\n"
        status_lines = status_text.split('\n')
        for i, line in enumerate(status_lines):
            line_surface = self.font.render(line, True, pygame.Color('white'))
            screen.blit(line_surface, (300, 30 + i * 20))
            dirty_rects.append(line_surface.get_rect(topleft=(300, 30 + i * 20)))
        

        # Update only the dirty rectangles
        pygame.display.update(dirty_rects)


    def get_random_cell(self):
        while True:
            i, j = np.random.randint(0, self.grid_size, 2)
            cell = self.grid[i, j]
            if cell.type != 'X':
                return cell
            
    def spread_rumor(self, neighbors):
        cells_for_next_gen = []
        for n in neighbors:
            if n.recieve_rumor():
                cells_for_next_gen.append(n)
        return cells_for_next_gen
    
    def apply_new_generation(self):
        counter = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.grid[i, j].apply_new_generation()
                if self.grid[i, j].rumor_received:
                   counter += 1 
        return counter