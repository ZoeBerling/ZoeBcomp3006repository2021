import numpy as np

"""Zoe Berling DU ID 872608482 card_classes.py"""
"""Part 1:
Shape classes for:
Rectangle
Oval
Polygon
Square
Triangle
Pentagon
Circle
Parallelogram
Rhombus
Part 2:
Using a list of Suits and Values, take advantage of the zip function to create a list of tuples of a standard set of cards"""

# Part 1: Shape Classes:


# Create a shape class to be the basis for later classes extending from it.
class Shape:
    def __init__(self, width, height, num_sides=None):
        # Include any variables that you believe are universal to all shapes.
        self.width = width
        self.height = height
        self.num_sides = num_sides
        # self.length_side = length_side

    def Area(self):  # area method default wxh
        """placeholder"""
        print(f"The area is the size of a shape's surface.")

    def Perimeter(self):  # other methods that are universal to all shapes
        """placeholder"""
        print(f"The perimeter is the distance around a two dimensional shape.")


class Polygon(Shape):  # Polygon
    def __str__(self):
        if self.num_sides > 3:
            return f"A Polygon with {self.num_sides} that is {self.width} {self.measurement} by {self.height} " \
                   f"{self.measurement}"
        else:
            return f"A Polygon has > 3 sides. This shape has {self.num_sides}"

    def Area(self):
        # radians = np.pi/180
        if self.num_sides <= 2:  # if it is an oval/ circle
            return f"A polygon with {self.num_sides} is not possible"
        elif self.num_sides == 4:
            area = self.width * self.height
            return area
        elif self.num_sides == 3:
            area = (self.width * self.height)/2
            return area
        else: # for normal polygons with sides > 4
            area = self.width * (self.num_sides **2 ) / (4*np.tan(np.pi / self.num_sides))  # Assuming a normal polygon
            return area

    def Perimeter(self):  # assuming a regular polygon w/ sides of equal length
        return self.width * self.num_sides


class Parallelogram(Polygon):  # Parallelogram
    """A Polygon (Quadrilateral) with 2 pairs of parallel sides"""
    # def __init__(self, width, height, length_side = 0):
        # super(Parallelogram, self).__init__(width, height, 4, length_side)
    def __init__(self, width, height):
        super(Parallelogram, self).__init__(width, height, 4)

    def Perimeter(self):
        return 2 * self.width + (2 * self.height)


class Rectangle(Parallelogram):  # Rectangle
    """A Parallelogram with 4 90 degree angles"""
    def __init__(self, width, height):
        super(Rectangle, self).__init__(width, height)


class Square(Rectangle):  # Square
    """A Rectangle with 4 equal sides"""
    def __init__(self, width):
        super(Rectangle, self).__init__(width, width)


class Triangle(Polygon):  # Triangle
    """Polygon with 3 sides"""
    def __init__(self, base, height):
        self.base = base
        self.height = height
        super(Triangle, self).__init__(base, height, 3)

    def Perimeter(self):  # calculate the smallest possible perimeter based on base and height
        return f"The smallest possible perimeter is {np.sqrt(((self.height**2) * 4) + (self.base ** 2)) + self.base}."

class Pentagon(Polygon):  # Parallelogram
    """A Polygon with 5 sides (Pentagon)"""
    def __init__(self, width, height=None):
        super(Pentagon, self).__init__(width, height, 5)


class Oval(Shape):  # Oval
    """The most general term for round shapes. Takes in radius a and radius b"""
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __str__(self):
        return f"An Oval where a = {self.width} and b = {self.height}"

    def Area(self):
        return (self.width * self.height) * np.pi

    def Circumference(self):
        return (2 * np.pi) * np.sqrt(((self.width**2) + (self.height**2))/2)

    def Perimeter(self):
        return self.Circumference()

class Circle(Oval):  # Circle
    """Takes in a value for the radius"""
    def __init__(self, radius):
        self.radius = radius
        super(Circle, self).__init__(radius, radius)

    def Circumference(self):
        return (self.radius * 2) * np.pi

    def Perimeter(self):
        return self.Circumference()


class Rhombus(Parallelogram):  # Rhombus
    """A Rhombus is a square with two opposite equal acute angles, implying two opposite equal obtuse angles"""
    def __init__(self, width):
        super(Rhombus, self).__init__(width, width)

def main():

    hi = Rectangle(8,10)

    bye = Parallelogram(9,9)

    aloha = Square(10)

    ciao = Pentagon(5)

    hello = Triangle(10, 3)

    yo = Oval(5, 10)

    hey = Circle(90)

    farewell = Rhombus(10)

    print(hi.Area())
    print(hi.Perimeter())

    print(bye.Area())
    print(bye.Perimeter())

    print(aloha.Area())
    print(aloha.Perimeter())

    print(ciao.Area())
    print(ciao.Perimeter())

    print(hello.Area())
    print(hello.Perimeter())

    print(yo.Area())
    print(yo.Perimeter())

    print(hey.Area())
    print(hey.Circumference())

    print(farewell.Area())
    print(farewell.Perimeter())

    # Part 2: Zip Function Practice

    # Using a list of Suits and Values, take advantage of the zip function to create a list of tuples of a standard set of
    # cards
    """iterate over values x number of suits. zip togethert"""

    suits = ['hearts', 'spades', 'diamonds', 'clubs']
    type = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    suitlist = [suit for suit in suits for i in range(13)]
    valuelist = []
    for i in range(len(suits)):
        for t in type:
            valuelist.append(t)
    set = list(zip(suitlist, valuelist))
    print(set)



if __name__ == '__main__':
    main()
