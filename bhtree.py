from vector import Vector
from types1 import Body

class Quad:
    def __init__(self, xmid, ymid, length):
        self.xmid = xmid
        self.ymid = ymid
        self.length = length

    def contains(self, point):
        x, y = point.x, point.y
        half = self.length / 2
        return (self.xmid - half <= x <= self.xmid + half) and (self.ymid - half <= y <= self.ymid + half)

    def NW(self):
        return Quad(self.xmid - self.length / 4, self.ymid + self.length / 4, self.length / 2)

    def NE(self):
        return Quad(self.xmid + self.length / 4, self.ymid + self.length / 4, self.length / 2)

    def SW(self):
        return Quad(self.xmid - self.length / 4, self.ymid - self.length / 4, self.length / 2)

    def SE(self):
        return Quad(self.xmid + self.length / 4, self.ymid - self.length / 4, self.length / 2)

class BHTree:
    def __init__(self, quad):
        self.quad = quad
        self.body = None
        self.total_mass = 0.0
        self.center_of_mass = Vector(0.0, 0.0)
        self.NW = self.NE = self.SW = self.SE = None

    def is_external(self):
        return not any([self.NW, self.NE, self.SW, self.SE])

    def insert(self, body):
        if self.body is None and self.is_external():
            self.body = body
            self.total_mass = body.mass
            self.center_of_mass = body.pos
            return

        if self.is_external():
            b = self.body
            self.body = None
            self._subdivide()
            self._place_body(b)
            self._place_body(body)
        else:
            self._place_body(body)

        # Update center of mass and total mass
        total_mass = self.total_mass + body.mass
        self.center_of_mass = (self.center_of_mass * self.total_mass + body.pos * body.mass) / total_mass
        self.total_mass = total_mass

    def _subdivide(self):
        self.NW = BHTree(self.quad.NW())
        self.NE = BHTree(self.quad.NE())
        self.SW = BHTree(self.quad.SW())
        self.SE = BHTree(self.quad.SE())

    def _place_body(self, body):
        if self.quad.NW().contains(body.pos):
            self.NW.insert(body)
        elif self.quad.NE().contains(body.pos):
            self.NE.insert(body)
        elif self.quad.SW().contains(body.pos):
            self.SW.insert(body)
        elif self.quad.SE().contains(body.pos):
            self.SE.insert(body)

    def update_force(self, body, theta=0.5, G=6.6743e-11, eps=0.2):
        force = Vector(0.0, 0.0)
        if self.body is not None and self.body != body:
            r = self.body.pos - body.pos
            dist = r.norm() + eps
            f = G * body.mass * self.body.mass / (dist * dist + eps * eps)
            return r * (f / dist)
        elif not self.is_external():
            s = self.quad.length
            d = self.center_of_mass.distance(body.pos)
            if s / d < theta:
                r = self.center_of_mass - body.pos
                dist = r.norm() + eps
                f = G * body.mass * self.total_mass / (dist * dist + eps * eps)
                return r * (f / dist)
            else:
                # Recursively calculate force
                for child in [self.NW, self.NE, self.SW, self.SE]:
                    if child:
                        force += child.update_force(body, theta, G, eps)
        return force