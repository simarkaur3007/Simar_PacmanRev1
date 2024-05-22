import pygame  # Import the pygame module for game development
from pygame.locals import *  # Import all constants from pygame.locals
from constants import *  # Import all constants from the constants module
from pacman import Pacman  # Import the Pacman class from the pacman module
from nodes import NodeGroup  # Import the NodeGroup class from the nodes module
from pellets import PelletGroup  # Import the PelletGroup class from the pellets module

class GameController(object):  # Define a class for game control
    def __init__(self):  # Initialize the game controller
        pygame.init()  # Initialize all imported pygame modules
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)  # Set up the display mode with screen size
        self.background = None  # Initialize the background to None
        self.clock = pygame.time.Clock()  # Create a clock object to manage time

    def setBackground(self):  # Define method to set the background
        self.background = pygame.surface.Surface(SCREENSIZE).convert()  # Create a surface for the background
        self.background.fill(BLACK)  # Fill the background with black color

    def startGame(self):  # Define method to start the game
        self.setBackground()  # Set the background for the game
        self.nodes = NodeGroup("maze1.txt")  # Initialize the node group with a maze file
        self.nodes.setPortalPair((0, 17), (27, 17))  # Set portal pairs in the maze
        self.pacman = Pacman(self.nodes.getStartTempNode())  # Initialize Pacman with the starting node
        self.pellets = PelletGroup("maze1.txt")  # Initialize the pellet group with the maze file

    def update(self):  # Define method to update the game state
        dt = self.clock.tick(30) / 1000.0  # Calculate the delta time since the last frame
        self.pacman.update(dt)  # Update Pacman's state
        self.pellets.update(dt)  # Update the pellet group's state
        self.checkPelletEvents()  # Check for pellet events
        self.checkEvents()  # Check for other events
        self.render()  # Render the game screen

    def checkEvents(self):  # Define method to check for events
        for event in pygame.event.get():  # Iterate through all events
            if event.type == QUIT:  # If the event is quitting the game
                exit()  # Exit the game

    def checkPelletEvents(self):  # Define method to check for pellet events
        pellet = self.pacman.eatPellets(self.pellets.pelletList)  # Check if Pacman eats a pellet
        if pellet:  # If a pellet is eaten
            self.pellets.numEaten += 1  # Increment the number of eaten pellets
            self.pellets.pelletList.remove(pellet)  # Remove the eaten pellet from the list

    def render(self):  # Define method to render the game screen
        self.screen.blit(self.background, (0, 0))  # Draw the background on the screen
        self.nodes.render(self.screen)  # Render the nodes on the screen
        self.pellets.render(self.screen)  # Render the pellets on the screen
        self.pacman.render(self.screen)  # Render Pacman on the screen
        pygame.display.update()  # Update the display with changes

if __name__ == "__main__":  # If this module is run as the main program
    game = GameController()  # Create a game controller object
    game.startGame()  # Start the game
    while True:  # Run the game loop indefinitely
        game.update()  # Update the game state in each loop iteration
