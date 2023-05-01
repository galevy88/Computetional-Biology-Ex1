import pygame
import easygui as eg
from Grid import Grid
import Globals
import matplotlib.pyplot as plt


class SettingsPage:
    def __init__(self):
        self.title = 'Settings'
        self.msg = 'Choose an option'
        self.choices = ['Set Parameters', 'Create Fast Grid', 'Create Slow Grid']

    def start(self):
        # Show options window
        choice = eg.buttonbox(self.msg, self.title, self.choices)

        # Call corresponding function based on user choice
        if choice == 'Set Parameters':
            self.set_parameters()
            self.start_simulation()
        elif choice == 'Create Fast Grid':
            Globals.probs = [0.2, 0.2, 0.4, 0.2]
            self.start_simulation(fast=True)
        elif choice == 'Create Slow Grid':
            Globals.probs = [0.1, 0.1, 0.4, 0.4]
            self.start_simulation(slow=True)

    def set_parameters(self):
        # Show settings page window
        fieldNames = ['Grid size:', 'Population density:', 'S1:', 'S2:', 'S3:', 'S4:', 'Cool Down level:']
        fieldValues = [str(Globals.GRID_SIZE), str(Globals.POP_DENSITY), str(Globals.S1_SPREAD),
                            str(Globals.S2_SPREAD), str(Globals.S3_SPREAD), str(Globals.S4_SPREAD),
                            str(Globals.COOL_DOWN)]
        fieldValues = eg.multenterbox(self.msg, self.title, fieldNames, fieldValues)

        # Update global variables with user input
        Globals.GRID_SIZE = int(fieldValues[0])
        Globals.POP_DENSITY = float(fieldValues[1])
        Globals.S1_SPREAD = float(fieldValues[2])
        Globals.S2_SPREAD = float(fieldValues[3])
        Globals.S3_SPREAD = float(fieldValues[4])
        Globals.S4_SPREAD = float(fieldValues[5])
        Globals.COOL_DOWN = int(fieldValues[6])
        Globals.probs = [Globals.S1_SPREAD, Globals.S2_SPREAD, Globals.S3_SPREAD, Globals.S4_SPREAD]

    def start_simulation(self, fast=False, slow=False):
        # Open grid display window
        pygame.init()
        grid_app = Grid()
        if fast:
            grid_app.create_fast_grid()
        elif slow:
            grid_app.create_slow_grid()
        else:
            grid_app.create_grid()
        generation_data = grid_app.start()
        
        # extract x and y values from generation_data
        x_values = [tup[0] for tup in generation_data]
        y_values = [tup[1] for tup in generation_data]

        # plot the graph
        plt.plot(x_values, y_values)

        # add labels and title
        plt.xlabel('Generation')
        plt.ylabel('Queue Size')
        plt.title('Queue Size by Generation')

        # display the plot
        plt.show()


app = SettingsPage()
app.start()
