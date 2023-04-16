import tkinter as tk
import numpy as np
import random
from Cell import Cell
import Globals
import queue


class Grid:
    def __init__(self, master):
        self.q = queue.Queue()
        self.master = master
        master.title('Grid Display')

        # Set grid size and population density
        self.grid_size = Globals.GRID_SIZE
        self.population_density = Globals.POP_DENSITY

        # Set levels of skepticism
        self.skepticism_levels = ['S1', 'S2', 'S3', 'S4']
        self.transmission_probability = Globals.transmission_probability
        
        self.create_grid()
        

            
    def create_grid(self):
        # Create a grid of size grid_size x grid_size with skepticism levels assigned randomly
        self.grid = np.empty((self.grid_size, self.grid_size), dtype=object)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.grid[i, j] = Cell((i, j), 'X', None)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.grid[i, j]
                if random.random() < self.population_density:
                    skepticism_level = np.random.choice(self.skepticism_levels, p=Globals.probs)
                    cell.type = skepticism_level
                    cell.rumor_prob = Globals.transmission_probability.get(skepticism_level, None)


        # Create canvas to display grid
        self.canvas = tk.Canvas(self.master, width=800, height=800)
        self.canvas.pack(padx=5, pady=5)



                


    def start(self):
        chosen_cell = self.get_random_cell()
        chosen_cell.recieve_rumor()
        neighbors = chosen_cell.generate_rumor_for_neighbors(self.grid)
        if neighbors is not None:
            for n in neighbors:
                self.q.put(n)
        while(not self.q.empty()):
            cell = self.q.get()
            cell.recieve_rumor()
            neighbors = cell.generate_rumor_for_neighbors(self.grid)
            if neighbors is not None:
                for n in neighbors:
                    self.q.put(n)
        self.display_grid()
        

    def display_grid(self):
        # Calculate cell size and padding to center grid on canvas
        cell_size = 600 // self.grid_size
        canvas_padding = (800 - cell_size * self.grid_size) // 2

        # Display grid on canvas
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0 = j * cell_size + canvas_padding
                y0 = i * cell_size + canvas_padding
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                color = {'S1': 'red', 'S2': 'orange', 'S3': 'green', 'S4': 'blue'}.get(self.grid[i, j].type, 'black')
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
                
    def get_random_cell(self):
        while True:
            i, j = np.random.randint(0, self.grid_size, 2)
            cell = self.grid[i, j]
            if cell.type != 'X':
                return cell