import pygame
import easygui as eg
from Grid import Grid
import Globals
import matplotlib.pyplot as plt


class SettingsPage:
    def __init__(self):
        self.title = 'Settings'
        self.msg = 'Enter the parameters'
        self.fieldNames = ['Grid size:', 'Population density:', 'S1:', 'S2:', 'S3:', 'S4:', 'Cool Down level:']
        self.fieldValues = [str(Globals.GRID_SIZE), str(Globals.POP_DENSITY), str(Globals.S1_SPREAD),
                            str(Globals.S2_SPREAD), str(Globals.S3_SPREAD), str(Globals.S4_SPREAD),
                            str(Globals.COOL_DOWN)]

    def start(self):
        # Show settings page window
        self.fieldValues = eg.multenterbox(self.msg, self.title, self.fieldNames, self.fieldValues)

        # Update global variables with user input
        Globals.GRID_SIZE = int(self.fieldValues[0])
        Globals.POP_DENSITY = float(self.fieldValues[1])
        Globals.S1_SPREAD = float(self.fieldValues[2])
        Globals.S2_SPREAD = float(self.fieldValues[3])
        Globals.S3_SPREAD = float(self.fieldValues[4])
        Globals.S4_SPREAD = float(self.fieldValues[5])
        Globals.COOL_DOWN = int(self.fieldValues[6])
        Globals.probs = [Globals.S1_SPREAD, Globals.S2_SPREAD, Globals.S3_SPREAD, Globals.S4_SPREAD]

        # Open grid display window
        pygame.init()
        grid_app = Grid()
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
