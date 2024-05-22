import pygame  # Import the pygame module for game development
from vector import Vector2  # Import the Vector2 class from the vector module
from constants import *  # Import all constants from the constants module
import numpy as np  # Import the numpy module for numerical operations

class Node(object):  # Define a class for a node in the maze
    def __init__(self, x, y):  # Initialize the node with x and y coordinates
        self.position = Vector2(x, y)  # Set the position of the node as a Vector2 object
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None, PORTAL: None}  # Initialize neighbor nodes

    def render(self, screen):  # Define the method to render the node on the screen
        for n in self.neighbors.keys():  # Iterate through each neighbor direction
            if self.neighbors[n] is not None:  # If the neighbor exists
                line_start = self.position.asTuple()  # Get the start position of the line
                line_end = self.neighbors[n].position.asTuple()  # Get the end position of the line
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)  # Draw the line between nodes
        pygame.draw.circle(screen, RED, self.position.asInt(), 12)  # Draw the node as a red circle

class NodeGroup(object):  # Define a class for a group of nodes
    def __init__(self, level):  # Initialize the node group with a level file
        self.level = level  # Set the level file
        self.nodesLUT = {}  # Initialize a lookup table for nodes
        self.nodeSymbols = ['+', 'P', 'n']  # Define symbols representing nodes
        self.pathSymbols = ['.', '-', '|', 'p']  # Define symbols representing paths
        data = self.readMazeFile(level)  # Read the maze file data
        self.createNodeTable(data)  # Create the node table from the data
        self.connectHorizontally(data)  # Connect nodes horizontally
        self.connectVertically(data)  # Connect nodes vertically

    def readMazeFile(self, textfile):  # Define the method to read the maze file
        return np.loadtxt(textfile, dtype='<U1')  # Load the file into a numpy array of strings

    def createNodeTable(self, data, xoffset=0, yoffset=0):  # Define the method to create the node table
        for row in list(range(data.shape[0])):  # Iterate through each row in the data
            for col in list(range(data.shape[1])):  # Iterate through each column in the data
                if data[row][col] in self.nodeSymbols:  # If the cell contains a node symbol
                    x, y = self.constructKey(col + xoffset, row + yoffset)  # Construct the key for the node
                    self.nodesLUT[(x, y)] = Node(x, y)  # Add the node to the lookup table

    def constructKey(self, x, y):  # Define the method to construct a key from x and y coordinates
        return x * TILEWIDTH, y * TILEHEIGHT  # Return the coordinates multiplied by tile dimensions

    def connectHorizontally(self, data, xoffset=0, yoffset=0):  # Define the method to connect nodes horizontally
        for row in list(range(data.shape[0])):  # Iterate through each row in the data
            key = None  # Initialize the key to None
            for col in list(range(data.shape[1])):  # Iterate through each column in the data
                if data[row][col] in self.nodeSymbols:  # If the cell contains a node symbol
                    if key is None:  # If no key is set
                        key = self.constructKey(col + xoffset, row + yoffset)  # Set the key to the current node
                    else:  # If a key is already set
                        otherkey = self.constructKey(col + xoffset, row + yoffset)  # Set the other key to the current node
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherkey]  # Connect right neighbor
                        self.nodesLUT[otherkey].neighbors[LEFT] = self.nodesLUT[key]  # Connect left neighbor
                        key = otherkey  # Update the key to the current node
                elif data[row][col] not in self.pathSymbols:  # If the cell is not a path symbol
                    key = None  # Reset the key to None

    def connectVertically(self, data, xoffset=0, yoffset=0):  # Define the method to connect nodes vertically
        dataT = data.transpose()  # Transpose the data for vertical connection
        for col in list(range(dataT.shape[0])):  # Iterate through each column in the transposed data
            key = None  # Initialize the key to None
            for row in list(range(dataT.shape[1])):  # Iterate through each row in the transposed data
                if dataT[col][row] in self.nodeSymbols:  # If the cell contains a node symbol
                    if key is None:  # If no key is set
                        key = self.constructKey(col + xoffset, row + yoffset)  # Set the key to the current node
                    else:  # If a key is already set
                        otherkey = self.constructKey(col + xoffset, row + yoffset)  # Set the other key to the current node
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherkey]  # Connect down neighbor
                        self.nodesLUT[otherkey].neighbors[UP] = self.nodesLUT[key]  # Connect up neighbor
                        key = otherkey  # Update the key to the current node
                elif dataT[col][row] not in self.pathSymbols:  # If the cell is not a path symbol
                    key = None  # Reset the key to None

    def getNodeFromPixels(self, xpixel, ypixel):  # Define the method to get a node from pixel coordinates
        if (xpixel, ypixel) in self.nodesLUT.keys():  # Check if the key exists in the lookup table
            return self.nodesLUT[(xpixel, ypixel)]  # Return the node from the lookup table
        return None  # Return None if the key does not exist

    def getNodeFromTiles(self, col, row):  # Define the method to get a node from tile coordinates
        x, y = self.constructKey(col, row)  # Construct the key from the tile coordinates
        if (x, y) in self.nodesLUT.keys():  # Check if the key exists in the lookup table
            return self.nodesLUT[(x, y)]  # Return the node from the lookup table
        return None  # Return None if the key does not exist

    def getStartTempNode(self):  # Define the method to get the starting node
        nodes = list(self.nodesLUT.values())  # Get all nodes as a list
        return nodes[0]  # Return the first node as the starting node

    def setPortalPair(self, pair1, pair2):  # Define the method to set portal pairs
        key1 = self.constructKey(*pair1)  # Construct the key for the first portal
        key2 = self.constructKey(*pair2)  # Construct the key for the second portal
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():  # Check if both keys exist in the lookup table
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]  # Set the portal neighbor for the first node
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]  # Set the portal neighbor for the second node

    def render(self, screen):  # Define the method to render all nodes on the screen
        for node in self.nodesLUT.values():  # Iterate through each node in the lookup table
            node.render(screen)  # Render the node on the screen
