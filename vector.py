import math  # Import the math module for mathematical operations

class Vector2(object):  # Define a class for 2D vectors
    def __init__(self, x=0, y=0):  # Initialize the vector with x and y coordinates
        self.x = x  # Assign the x coordinate
        self.y = y  # Assign the y coordinate
        self.thresh = 0.000001  # Set a threshold for comparison to determine equality

    def __add__(self, other):  # Define addition of two vectors
        return Vector2(self.x + other.x, self.y + other.y)  # Return the sum of two vectors

    def __sub__(self, other):  # Define subtraction of two vectors
        return Vector2(self.x - other.x, self.y - other.y)  # Return the difference of two vectors

    def __neg__(self):  # Define negation of a vector
        return Vector2(-self.x, -self.y)  # Return the negated vector

    def __mul__(self, scalar):  # Define multiplication of a vector by a scalar
        return Vector2(self.x * scalar, self.y * scalar)  # Return the scaled vector

    def __div__(self, scalar):  # Define division of a vector by a scalar
        if scalar != 0:  # Check if the scalar is not zero
            return Vector2(self.x / float(scalar), self.y / float(scalar))  # Return the divided vector
        return None  # Return None if scalar is zero

    def __truediv__(self, scalar):  # Define true division for Python 3 compatibility
        return self.__div__(scalar)  # Use the __div__ method for division

    def __eq__(self, other):  # Define equality check between two vectors
        if abs(self.x - other.x) < self.thresh:  # Check if x coordinates are approximately equal
            if abs(self.y - other.y) < self.thresh:  # Check if y coordinates are approximately equal
                return True  # Return True if both coordinates are approximately equal
        return False  # Return False otherwise

    def magnitudeSquared(self):  # Define method to calculate the squared magnitude of the vector
        return self.x**2 + self.y**2  # Return the sum of squares of the coordinates

    def magnitude(self):  # Define method to calculate the magnitude of the vector
        return math.sqrt(self.magnitudeSquared())  # Return the square root of the squared magnitude

    def copy(self):  # Define method to create a copy of the vector
        return Vector2(self.x, self.y)  # Return a new vector with the same coordinates

    def asTuple(self):  # Define method to get the vector as a tuple
        return self.x, self.y  # Return the coordinates as a tuple

    def asInt(self):  # Define method to get the vector as integer coordinates
        return int(self.x), int(self.y)  # Return the coordinates as integers

    def __str__(self):  # Define string representation of the vector
        return "<"+str(self.x)+", "+str(self.y)+">"  # Return the coordinates in angle brackets as a string
