from bhtree import BHTree, Quad
from types1 import Body

class NBodySimulation:
    def __init__(self, bodies, quad_size, theta=0.5, G=1.0):
        self.bodies = bodies
        self.quad_size = quad_size
        self.theta = theta
        self.G = G

    def step(self, dt):
        # Build Barnes-Hut tree
        tree = BHTree(Quad(0.0, 0.0, self.quad_size))
        for body in self.bodies:
            tree.insert(body)
        # Update forces
        for body in self.bodies:
            body.reset_force()
            f = tree.update_force(body, self.theta, self.G)
            body.add_force(f)
        # Update positions and velocities
        for body in self.bodies:
            body.update(dt)