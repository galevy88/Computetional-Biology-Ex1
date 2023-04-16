import tkinter as tk
from Grid import Grid
import Globals
import time

class SettingsPage:
    def __init__(self, master):
        self.master = master
        master.title('Settings')

        # Grid size
        tk.Label(master, text='Grid size:').grid(row=0, column=0)
        self.grid_size_var = tk.IntVar(value=Globals.GRID_SIZE)
        tk.Entry(master, textvariable=self.grid_size_var).grid(row=0, column=1)

        # Population density
        tk.Label(master, text='Population density:').grid(row=1, column=0)
        self.pop_density_var = tk.DoubleVar(value=Globals.POP_DENSITY)
        tk.Entry(master, textvariable=self.pop_density_var).grid(row=1, column=1)

        # Skepticism levels
        tk.Label(master, text='Skepticism levels:').grid(row=2, column=0)
        self.s1_var = tk.DoubleVar(value=Globals.S1_SPREAD)
        tk.Label(master, text='S1').grid(row=3, column=0)
        tk.Entry(master, textvariable=self.s1_var).grid(row=3, column=1)
        self.s2_var = tk.DoubleVar(value=Globals.S2_SPREAD)
        tk.Label(master, text='S2').grid(row=4, column=0)
        tk.Entry(master, textvariable=self.s2_var).grid(row=4, column=1)
        self.s3_var = tk.DoubleVar(value=Globals.S3_SPREAD)
        tk.Label(master, text='S3').grid(row=5, column=0)
        tk.Entry(master, textvariable=self.s3_var).grid(row=5, column=1)
        self.s4_var = tk.DoubleVar(value=Globals.S4_SPREAD)
        tk.Label(master, text='S4').grid(row=6, column=0)
        tk.Entry(master, textvariable=self.s4_var).grid(row=6, column=1)
        tk.Label(master, text='Cool Down level:').grid(row=7, column=0)
        self.coolo_down_var = tk.IntVar(value=Globals.COOL_DOWN)
        tk.Label(master, text='L').grid(row=8, column=0)
        tk.Entry(master, textvariable=self.coolo_down_var).grid(row=8, column=1)

        # Start button
        tk.Button(master, text='Start', command=self.start).grid(row=9, column=0, columnspan=2)

    def start(self):
        # Update global variables with user input
        Globals.GRID_SIZE = self.grid_size_var.get()
        Globals.POP_DENSITY = self.pop_density_var.get()
        Globals.S1_SPREAD = self.s1_var.get()
        Globals.S2_SPREAD = self.s2_var.get()
        Globals.S3_SPREAD = self.s3_var.get()
        Globals.S4_SPREAD = self.s4_var.get()
        Globals.COOL_DOWN = self.coolo_down_var.get()
        Globals.probs = [Globals.S1_SPREAD, Globals.S2_SPREAD, Globals.S3_SPREAD, Globals.S4_SPREAD]

        # Open grid display window
        root.destroy()
        grid_root = tk.Tk()
        grid_app = Grid(grid_root)
        ITERATIONS = 30
        for i in range(0,ITERATIONS):
            print(f"iteration {i}/{ITERATIONS}")
            grid_app.start()
            grid_root.update()


# Open settings page window
root = tk.Tk()
app = SettingsPage(root)
root.mainloop()
