import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Visualizer:
    def __init__(self, sim, xlim=(-1,1), ylim=(-1,1)):
        self.sim = sim
        self.xlim = xlim
        self.ylim = ylim

        self.fig, self.ax = plt.subplots()
        self.scat = self.ax.scatter([], [], s=10)
        self.ax.set_xlim(*xlim)
        self.ax.set_ylim(*ylim)
        self.ax.set_aspect('equal')

    def get_positions(self):
        xs = [body.pos.x for body in self.sim.bodies]
        ys = [body.pos.y for body in self.sim.bodies]
        return xs, ys

    def init(self):
        xs, ys = self.get_positions()
        self.scat.set_offsets(list(zip(xs, ys)))
        return self.scat,

    def update(self, frame):
        self.sim.step(frame)
        xs, ys = self.get_positions()
        self.scat.set_offsets(list(zip(xs, ys)))
        return self.scat,

    def animate(self, steps=1000, dt=0.01, interval=20):
        def stepper(_):
            self.sim.step(dt)
            xs, ys = self.get_positions()
            self.scat.set_offsets(list(zip(xs, ys)))
            return self.scat,

        anim = FuncAnimation(self.fig, stepper, frames=steps, 
                             init_func=self.init, blit=True, interval=interval)
        plt.show()