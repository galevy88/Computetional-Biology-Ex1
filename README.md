# Rumor Spread
The project is called "Rumor Spread" and is a simulation of rumor spreading in a grid, where each cell has a different level of skepticism.

# Project Description
The "Rumor Spread" is a Python project that simulates the spreading of a rumor in a grid. The grid is made up of cells, each of which has a different level of skepticism. The project uses the Pygame library to create a graphical representation of the grid.

The user is presented with a settings page where they can set the grid size, population density, skepticism levels, and cool-down level. The user can also choose to create a fast grid or a slow grid. The fast and slow grids have different proportions of skepticism levels, which affects the spread of the rumor.

Once the user has set the parameters and chosen a grid type, they can start the simulation. The simulation shows the spreading of the rumor through the grid, with each generation represented on the graphical display. The simulation continues until the queue size is the same for five generations in a row.

The simulation also includes a graph of the queue size by generation, using the Matplotlib library.

# How to Run the Project
1. Open Google Drive folder:
https://drive.google.com/drive/folders/1VCIMR0W-ekvby8f06Eo-T54jR6jRLQZY?usp=sharing
2. Download this folder to your pc
2. Go into dist folder and you will be able to see main.exe file
4. doublie click on main.exe file and wait 10-15 seconds

Set the parameters on the settings page.
Choose a grid type (fast, slow, or custom).
Start the simulation.
Watch the graphical display and the queue size graph.
When the simulation ends, the graph is displayed.

# Project Files
main.py: The main file that sets up the settings page and starts the simulation.
Grid.py: The file that contains the Grid class and the Cell class, which represent the grid and its cells.
Globals.py: The file that contains the global variables used in the project.
README.md: The file that contains the project description, instructions, and other information.
