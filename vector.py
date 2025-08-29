import math

class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def norm(self):
        return math.hypot(self.x, self.y)

    def distance(self, other):
        return (self - other).norm()

    def __repr__(self):
        return f"Vector({self.x:.3f}, {self.y:.3f})"