

import Globals
import random 
class Cell:
    def __init__(self, location, type, rumor_prob):
        self.location = location
        self.original_params = { "type" : type, "rumor_prob" : rumor_prob }
        self.type = type
        self.rumor_prob = rumor_prob
        self.can_spread = False
        self.rumor_counter = 0
        self.L = 0
        self.has_to_change = False
        self.rumor_received = False
        
    def recieve_rumor(self):
        if random.random() < self.rumor_prob:
            self.rumor_received = True
            self.can_spread = True
            self.rumor_counter += 1
        if self.rumor_counter >= 2:
            self.has_to_change = True
            self.change_type()
        return self.rumor_received
        

    def check_if_can_spread(self):
        return self.can_spread
        
    def generate_rumor_for_neighbors(self, grid):
        if self.can_spread:
            neighbors = self.get_neighbors(grid)
            self.L = Globals.COOL_DOWN
            print(f"self.L is {self.L}")
            self.can_spread = False
            return neighbors
        return None
    
    def get_neighbors(self, grid):
        row, col = self.location
        neighbors = []
        for r in range(max(0, row-1), min(row+2, grid.shape[0])):
            for c in range(max(0, col-1), min(col+2, grid.shape[1])):
                type = grid[r,c].type
                if r == row and c == col:
                    continue  # skip the current cell
                if type != 'X':
                    neighbors.append(grid[r, c])
        return neighbors

    
    def change_type(self):
        if self.type == 'S4':
            self.type = 'S3'
            self.rumor_prob = Globals.S3_RUMOR
        if self.type == 'S3':
            self.type = 'S2'
            self.rumor_prob = Globals.S2_RUMOR
        if self.type == 'S2':
            self.type = 'S1'
            self.rumor_prob = Globals.S1_RUMOR
        if self.type == 'S1':
            self.type = 'S1'
            self.rumor_prob = Globals.S1_RUMOR
            
    def apply_new_generation(self):
        self.rumor_counter = 0
        if self.L != 0:
            self.L -= 1
        else:
            self.can_spread = True
        if self.has_to_change:
            self.has_to_change = False
        else:
            self.type = self.original_params["type"]
            self.rumor_prob = self.original_params["rumor_prob"]
