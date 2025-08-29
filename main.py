from types1 import Body
from vector import Vector
from model_nbody import NBodySimulation
from visualizer import Visualizer
import random
import math

def create_galaxy(center, velocity, n_stars, spread, mass_range):
    bodies = []
    for _ in range(n_stars):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.gauss(0, spread)
        x = center.x + radius * math.cos(angle)
        y = center.y + radius * math.sin(angle)
        # Give each star a velocity similar to the galaxy's bulk velocity, plus a small random component
        vx = velocity.x + random.gauss(0, 0.02)
        vy = velocity.y + random.gauss(0, 0.02)
        mass = random.uniform(*mass_range)
        bodies.append(Body(mass=mass, pos=Vector(x, y), vel=Vector(vx, vy)))
    return bodies

def main():
    # Galaxy 1: centered at (-0.5, 0), moving right
    galaxy1 = create_galaxy(center=Vector(-0.5, 0), velocity=Vector(0.05, 0), n_stars=50, spread=0.1, mass_range=(0.5, 2.0))
    # Galaxy 2: centered at (0.5, 0), moving left
    galaxy2 = create_galaxy(center=Vector(0.5, 0), velocity=Vector(-0.05, 0), n_stars=50, spread=0.1, mass_range=(0.5, 2.0))

    bodies = galaxy1 + galaxy2

    sim = NBodySimulation(bodies, quad_size=2.0)
    visual = Visualizer(sim, xlim=(-1,1), ylim=(-1,1))
    visual.animate(steps=1000, dt=0.01, interval=20)

if __name__ == "__main__":
    main()