import pygame  # Import the pygame module for game development
from pygame.locals import *  # Import all constants from pygame.locals
from vector import Vector2  # Import the Vector2 class from the vector module
from constants import *  # Import all constants from the constants module

class Pacman(object):  # Define a class for Pacman
    def __init__(self, node):  # Initialize Pacman with a starting node
        self.name = PACMAN  # Set the name of the character to Pacman
        self.directions = {  # Define possible directions for Pacman
            STOP: Vector2(),  # No movement
            UP: Vector2(0, -1),  # Upward movement
            DOWN: Vector2(0, 1),  # Downward movement
            LEFT: Vector2(-1, 0),  # Leftward movement
            RIGHT: Vector2(1, 0)  # Rightward movement
        }
        self.direction = STOP  # Initialize the direction to stop
        self.speed = 100 * TILEWIDTH / 16  # Set the speed of Pacman
        self.radius = 10  # Set the radius for rendering Pacman
        self.color = YELLOW  # Set the color of Pacman
        self.node = node  # Set the starting node
        self.setPosition()  # Set the initial position
        self.target = node  # Set the initial target node
        self.collideRadius = 5  # Set the collision radius

    def setPosition(self):  # Define a method to set Pacman's position
        self.position = self.node.position.copy()  # Copy the node's position

    def update(self, dt):  # Define a method to update Pacman's state
        self.position += self.directions[self.direction] * self.speed * dt  # Update the position based on direction and speed
        direction = self.getValidKey()  # Get the direction from the key press
        if self.overshotTarget():  # Check if Pacman has overshot the target node
            self.node = self.target  # Set the current node to the target
            if self.node.neighbors[PORTAL] is not None:  # Check for portal
                self.node = self.node.neighbors[PORTAL]  # Move to the portal node
            self.target = self.getNewTarget(direction)  # Get the new target node based on direction
            if self.target is not self.node:  # If the target is not the current node
                self.direction = direction  # Update the direction
            else:  # If the target is the current node
                self.target = self.getNewTarget(self.direction)  # Get the new target based on current direction
            if self.target is self.node:  # If the target is still the current node
                self.direction = STOP  # Stop the movement
            self.setPosition()  # Set the position to the node's position
        else:  # If Pacman hasn't overshot the target
            if self.oppositeDirection(direction):  # Check if the new direction is opposite
                self.reverseDirection()  # Reverse the direction

    def validDirection(self, direction):  # Define a method to check if a direction is valid
        if direction is not STOP:  # If the direction is not stop
            if self.node.neighbors[direction] is not None:  # Check if there is a neighboring node in that direction
                return True  # Return True if valid
        return False  # Return False if not valid

    def getNewTarget(self, direction):  # Define a method to get a new target node
        if self.validDirection(direction):  # Check if the direction is valid
            return self.node.neighbors[direction]  # Return the neighboring node in that direction
        return self.node  # Return the current node if the direction is not valid

    def getValidKey(self):  # Define a method to get the direction from key press
        key_pressed = pygame.key.get_pressed()  # Get the state of all keyboard keys
        if key_pressed[K_UP]:  # If the up key is pressed
            return UP  # Return the up direction
        if key_pressed[K_DOWN]:  # If the down key is pressed
            return DOWN  # Return the down direction
        if key_pressed[K_LEFT]:  # If the left key is pressed
            return LEFT  # Return the left direction
        if key_pressed[K_RIGHT]:  # If the right key is pressed
            return RIGHT  # Return the right direction
        return STOP  # Return stop if no direction key is pressed

    def overshotTarget(self):  # Define a method to check if Pacman has overshot the target
        if self.target is not None:  # If the target is not None
            vec1 = self.target.position - self.node.position  # Vector from current node to target
            vec2 = self.position - self.node.position  # Vector from current node to current position
            node2Target = vec1.magnitudeSquared()  # Squared distance from current node to target
            node2Self = vec2.magnitudeSquared()  # Squared distance from current node to current position
            return node2Self >= node2Target  # Return True if current position is beyond or at target
        return False  # Return False if no target

    def reverseDirection(self):  # Define a method to reverse the direction
        self.direction *= -1  # Reverse the direction
        temp = self.node  # Temporary variable to hold the current node
        self.node = self.target  # Swap current node with target
        self.target = temp  # Swap target with current node

    def oppositeDirection(self, direction):  # Define a method to check if a direction is opposite
        if direction is not STOP:  # If the direction is not stop
            if direction == self.direction * -1:  # If the direction is opposite to the current direction
                return True  # Return True if opposite
        return False  # Return False if not opposite

    def eatPellets(self, pelletList):  # Define a method for Pacman to eat pellets
        for pellet in pelletList:  # Iterate through each pellet in the list
            d = self.position - pellet.position  # Calculate the distance vector between Pacman and the pellet
            dSquared = d.magnitudeSquared()  # Calculate the squared distance
            rSquared = (pellet.radius + self.collideRadius) ** 2  # Calculate the squared collision radius
            if dSquared <= rSquared:  # If the squared distance is within the collision radius
                return pellet  # Return the pellet that has been eaten
        return None  # Return None if no pellet is eaten

    def render(self, screen):  # Define a method to render Pacman on the screen
        p = self.position.asInt()  # Get the integer position of Pacman
        pygame.draw.circle(screen, self.color, p, self.radius)  # Draw Pacman as a circle on the screen
