from vector import Vector

class Body:
    def __init__(self, mass, pos, vel):
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.force = Vector(0.0, 0.0)

    def reset_force(self):
        self.force = Vector(0.0, 0.0)

    def add_force(self, f):
        self.force += f

    def update(self, dt):
        acc = self.force / self.mass
        self.vel += acc * dt
        self.pos += self.vel * dt

    def __repr__(self):
        return f"Body(mass={self.mass}, pos={self.pos}, vel={self.vel})"