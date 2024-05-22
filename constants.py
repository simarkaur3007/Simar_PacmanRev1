TILEWIDTH = 16  # Define the width of a tile in pixels
TILEHEIGHT = 16  # Define the height of a tile in pixels
NROWS = 36  # Define the number of rows in the game grid
NCOLS = 28  # Define the number of columns in the game grid
SCREENWIDTH = NCOLS * TILEWIDTH  # Calculate the width of the screen in pixels
SCREENHEIGHT = NROWS * TILEHEIGHT  # Calculate the height of the screen in pixels
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)  # Define the screen size as a tuple (width, height)

BLACK = (0, 0, 0)  # Define the color black as an RGB tuple
YELLOW = (255, 255, 0)  # Define the color yellow as an RGB tuple
WHITE = (255, 255, 255)  # Define the color white as an RGB tuple
RED = (255, 0, 0)  # Define the color red as an RGB tuple

STOP = 0  # Define a constant for the stop direction
UP = 1  # Define a constant for the up direction
DOWN = -1  # Define a constant for the down direction
LEFT = 2  # Define a constant for the left direction
RIGHT = -2  # Define a constant for the right direction

PACMAN = 0  # Define a constant representing Pacman
PORTAL = 3  # Define a constant representing a portal
PELLET = 1  # Define a constant representing a regular pellet
POWERPELLET = 2  # Define a constant representing a power pellet
