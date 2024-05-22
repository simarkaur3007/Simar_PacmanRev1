import pygame  # Import the pygame module for game development
from vector import Vector2  # Import the Vector2 class from the vector module
from constants import *  # Import all constants from the constants module
import numpy as np  # Import the numpy module for numerical operations

class Pellet(object):  # Define a class for regular pellets
    def __init__(self, row, column):  # Initialize the pellet with row and column positions
        self.name = PELLET  # Set the name of the pellet type
        self.position = Vector2(column * TILEWIDTH, row * TILEHEIGHT)  # Calculate the pellet's position
        self.color = WHITE  # Set the color of the pellet
        self.radius = int(4 * TILEWIDTH / 16)  # Set the radius of the pellet for rendering
        self.collideRadius = int(4 * TILEWIDTH / 16)  # Set the radius for collision detection
        self.points = 10  # Set the points awarded for collecting the pellet
        self.visible = True  # Set the visibility of the pellet

    def render(self, screen):  # Define the method to render the pellet on the screen
        if self.visible:  # Only render the pellet if it is visible
            p = self.position.asInt()  # Get the integer position of the pellet
            pygame.draw.circle(screen, self.color, p, self.radius)  # Draw the pellet as a circle on the screen

class PowerPellet(Pellet):  # Define a class for power pellets, inheriting from Pellet
    def __init__(self, row, column):  # Initialize the power pellet with row and column positions
        Pellet.__init__(self, row, column)  # Call the initializer of the parent Pellet class
        self.name = POWERPELLET  # Set the name of the pellet type to power pellet
        self.radius = int(8 * TILEWIDTH / 16)  # Set a larger radius for the power pellet
        self.points = 50  # Set higher points awarded for collecting the power pellet
        self.flashTime = 0.2  # Set the time interval for flashing visibility
        self.timer = 0  # Initialize the timer for flashing

    def update(self, dt):  # Define the method to update the power pellet's state
        self.timer += dt  # Increment the timer by the delta time
        if self.timer >= self.flashTime:  # Check if the timer exceeds the flash time
            self.visible = not self.visible  # Toggle the visibility of the power pellet
            self.timer = 0  # Reset the timer

class PelletGroup(object):  # Define a class for a group of pellets
    def __init__(self, pelletfile):  # Initialize the pellet group with a file containing pellet positions
        self.pelletList = []  # Create an empty list to store regular pellets
        self.powerpellets = []  # Create an empty list to store power pellets
        self.createPelletList(pelletfile)  # Populate the lists by reading the pellet file
        self.numEaten = 0  # Initialize the count of eaten pellets

    def update(self, dt):  # Define the method to update the pellet group
        for powerpellet in self.powerpellets:  # Iterate through all power pellets
            powerpellet.update(dt)  # Update each power pellet's state

    def createPelletList(self, pelletfile):  # Define the method to create pellet lists from a file
        data = self.readPelletfile(pelletfile)  # Read the pellet file into a data array
        for row in range(data.shape[0]):  # Iterate through each row in the data
            for col in range(data.shape[1]):  # Iterate through each column in the data
                if data[row][col] in ['.', '+']:  # Check if the cell represents a regular pellet
                    self.pelletList.append(Pellet(row, col))  # Add a regular pellet to the list
                elif data[row][col] in ['P', 'p']:  # Check if the cell represents a power pellet
                    pp = PowerPellet(row, col)  # Create a power pellet
                    self.pelletList.append(pp)  # Add the power pellet to the list
                    self.powerpellets.append(pp)  # Also add the power pellet to the power pellet list

    def readPelletfile(self, textfile):  # Define the method to read the pellet file
        return np.loadtxt(textfile, dtype='<U1')  # Load the file into a numpy array of strings

    def isEmpty(self):  # Define the method to check if the pellet list is empty
        if len(self.pelletList) == 0:  # Check if the list has no pellets
            return True  # Return True if empty
        return False  # Return False otherwise

    def render(self, screen):  # Define the method to render all pellets on the screen
        for pellet in self.pelletList:  # Iterate through each pellet in the list
            pellet.render(screen)  # Render the pellet on the screen
