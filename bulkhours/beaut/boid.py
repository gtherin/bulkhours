import numpy as np
import random
import math


class Boid:
    def __init__(self, label="", move_to_middle_strength=None, alert_distance=None):
        self.label = label
        self.move_to_middle_strength = move_to_middle_strength
        self.alert_distance = alert_distance

        self.x = random.randrange(100, 900)
        self.y = random.randrange(100, 900)
        self.angle = random.uniform(0.0, 2.0 * math.pi)
        self.color = "black"
        self.positions = Boid.new_flock(100, np.array([100, 900]), np.array([200, 1100]))
        self.velocities = Boid.new_flock(100, np.array([0, -20]), np.array([10, 20]))

    def draw_boid(self, canvas):
        size = 18
        x1 = self.x + size * math.cos(self.angle)
        x2 = self.y + size * math.sin(self.angle)
        canvas.create_line(
            self.x, self.y, x1, x2, fill="black", arrow="last", arrowshape=(12.8, 16, 4.8), width=2, tags=self.label
        )

    def flock(self, canvas, screen_size):
        distance = 3
        # calculate next the drone moves to
        self.x += distance * math.cos(self.angle)
        self.y += distance * math.sin(self.angle)
        # when drone goes off screen, will come back from other side of screen
        self.x = self.x % screen_size
        self.y = self.y % screen_size
        canvas.delete(self.label)
        self.draw_boid(canvas)

    def euclidean_distance(self, neighbour_boid):
        return math.sqrt(
            (self.x - neighbour_boid.x) * (self.x - neighbour_boid.x)
            + (self.y - neighbour_boid.y) * (self.y - neighbour_boid.y)
        )

    @staticmethod
    def new_flock(count, lower_limits, upper_limits):
        width = upper_limits - lower_limits
        return lower_limits[:, np.newaxis] + np.random.rand(2, count) * width[:, np.newaxis]

    def add_mean_reversion_velocity(self):
        if not self.move_to_middle_strength:
            return
        middle = np.mean(self.positions, 1)
        direction_to_middle = self.positions - middle[:, np.newaxis]
        self.velocities -= direction_to_middle * self.move_to_middle_strength

    def forbid_collision(self):
        if not self.alert_distance:
            return

        separations = self.positions[:, np.newaxis, :] - self.positions[:, :, np.newaxis]
        squared_displacements = separations * separations
        square_distances = np.sum(squared_displacements, 0)
        far_away = square_distances > self.alert_distance
        separations_if_close = np.copy(separations)
        separations_if_close[0, :, :][far_away] = 0
        separations_if_close[1, :, :][far_away] = 0
        self.velocities += np.sum(separations_if_close, 1)

        middle = np.mean(self.positions, 1)
        direction_to_middle = self.positions - middle[:, np.newaxis]
        self.velocities -= direction_to_middle * self.move_to_middle_strength

    def update_boids(self):
        self.positions += self.velocities


def animate_boid(boid, figure, scatter, frames=50, interval=50):
    import matplotlib.pyplot as plt
    from matplotlib import animation

    def animate(frame):
        boid.update_boids()
        boid.add_mean_reversion_velocity()
        boid.forbid_collision()
        scatter.set_offsets(boid.positions.transpose())

    anim = animation.FuncAnimation(figure, animate, frames=frames, interval=interval)
    return anim.to_jshtml()
