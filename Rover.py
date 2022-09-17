"""
The Rover class handles everything concerning the rover.
Meaning it handles the initialization of new rovers,
the movement and resetting of it.

A rover is initialized with two integers (its x- and y-values)
a direction (N, E, S, W) and what Mars it is related to (a many-to-one relationship).

The reason I added Mars to the initialization is mainly due to the fact
that it would be easy to add multiple rectangles if that was in the test-case
and at the same time move a Rover from one Mars to another.

It also makes it easier when validating the Rover to its assigned Mars as
we can ensure that it is in that particular Mars size.

I also decided to use the operator library as I wanted to show
that I understand the concept of working with getters and setters.
Even though that isn't necessary to use in Python it does make
the validation of attributes a bit 'neater' in my opinion.
"""

import operator

directions = ("N", "E", "S", "W")  # Use tuple since we don't need to manipulate


# the direction after initializing it (immutable)
class Rover(object):
    """
    As mentioned above, creates a Rover-object.
    """

    def __init__(self, x, y, direction, mars):
        """
        Initialize a rover
        """
        self.Mars = mars
        self.direction = direction
        self.x = x
        self.y = y
        self.initial = (self._x, self._y, self._direction)

    direction = property(operator.attrgetter('_direction'))

    """
    Setters, uses basic validation to ensure type-integrity.
    In directions uses tuple to ensure that direction is indeed correct.
    """

    @direction.setter
    def direction(self, d):
        """
        Checks if the direction exists in the
        defined directions.
        If the direction doesn't exist a
        ValueError is raised.
        Otherwise the direction is set.
        """
        if d.upper() not in directions:
            raise ValueError("Direction not correct, use 'N, E, S or W'")
        self._direction = d.upper()

    x = property(operator.attrgetter('_x'))

    @x.setter
    def x(self, x):
        """
        Checks if x is within acceptable
        bounds (higher than 0 and lower than
        Mars surface)
        """
        if (x < 0 or x > self.Mars.x):
            raise ValueError("""This rover's x-value is out of bounds.
It should be value should be < 0 and > {}""".format(str(self.Mars.x)))
        self._x = x

    y = property(operator.attrgetter('_y'))

    @y.setter
    def y(self, y):
        """
        Checks if y is within acceptable
        bounds (higher than 0 and lower than
        Mars surface).
        """
        if (y < 0 or y > self.Mars.y):
            raise ValueError("This rover's y-valueis out of bounds.\
It should be value should be < 0 and > " + str(self.Mars.y))
        self._y = y

    initial = property(operator.attrgetter('_initial'))

    @initial.setter
    def initial(self, tup):
        """
        Checks if the two first items in the
        passed tupple tup exist
        in the occupied spaces in the rover's
        assigned Mars.
        If it does exist that means the
        space is already taken and an error
        is raised.
        If the space is empty, the space is
        set to the initial space (used
        if the Rover goes out of bounds).
        """
        for spaces in self.Mars.occupied:
            if (tup[0], tup[1]) == (spaces[0], spaces[1]): raise RuntimeError("This position is \
already occupied by another rover")
        # if (tup[0], tup[1]) in self.Mars.occupied: raise IndexError("This position is already occupied by another
        # rover")
        self._initial = tup

    def get_formatted_position(self):
        """
        Returns a formatted string containing the
        Rover's position (as used in output).
        """
        return "{} {} {}".format(self._x, self._y, self._direction)

    def get_current_position(self):
        """
        Get the current position of the rover.
        Usually we don't need getters in Python,
        but I wanted to return a formatted string.

        This is also used in the unittest-cases to
        assert the position of the Rover.
        """
        return self._x, self._y

    """
    Re-initializes the object's positioning
    in case the rover goes out of bound.
    """

    def return_to_start(self):
        self.x = self._initial[0]
        self.y = self._initial[1]
        self.direction = self._initial[2]

    """
    Movement functions used to move the rover.
    """

    def turnRight(self):
        """
        Checks if the current direction is in the
        end of the tuple.
        If it's in the end of the
        tuple we take the first item in the tuple
        to be the new direction.
        Otherwise we take the element on index + 1.
        Basically attempts to mimic a compass by
        simulating a 'circular' list.
        """
        self.direction = directions[0] \
            if directions.index(self._direction) == 3 \
            else directions[directions.index(self._direction) + 1]

    def turnLeft(self):
        """
        Does the opposite of turnRight
        by checking if the item is in
        the beginning of the list.
        """
        self.direction = directions[3] \
            if directions.index(self._direction) == 0 \
            else directions[directions.index(self._direction) - 1]

    def forward(self):
        """
        Move the Rover forward in the direction it is facing
        by setting its Y- or X-value.
        This will use the class setters, so if the
        Rover goes outside of bounds it will raise an
        exception, which in turn will reset its position!

        It also raises an exception in case a forward Movement
        means it hits another rover already occupying its
        new space.
        """
        if self._direction == "N":
            self.y = self._y + 1
        elif self._direction == "S":
            self.y = self._y - 1
        elif self._direction == "E":
            self.x = self._x + 1
        else:
            self.x = self._x - 1
        # Test the current space
        for spaces in self.Mars.occupied:
            if self.get_current_position() == (spaces[0], spaces[1]):
                raise RuntimeErrorjk("I've hit a position that is already taken.\n\
Returning to my initial position. Please try again!\n")
                self.return_to_start()
