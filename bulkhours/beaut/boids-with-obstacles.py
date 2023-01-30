import sys, os.path as path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from modules.boid import *
from modules.obstacle import *


from boids import PyGameRendering


def main():

    rendering = PyGameRendering()

    rendering.add_boids("boid_list", 55, field_of_view=60)
    rendering.add_obstacle(17)

    rendering.prepare()

    while rendering.running:

        rendering.get_event()
        pos = pygame.mouse.get_pos()

        # Scan for boids and obstacles to pay attention to
        for boid in rendering.boid_list:
            closeboid = []
            visible_obstacles = []
            avoid = False
            for otherboid in rendering.boid_list:
                if otherboid == boid:
                    continue
                distance = boid.distance(otherboid)
                if distance < boid.field_of_view:
                    closeboid.append(otherboid)

            for obstacle in rendering.obstacle_list:
                distance = boid.distance(obstacle)
                if distance <= boid.field_of_view:
                    visible_obstacles.append(obstacle)

            # Apply the rules of the boids
            boid.cohesion(closeboid)
            boid.alignment(closeboid)
            boid.separation(closeboid, 20)
            if len(visible_obstacles) > 0:
                for obstacle in visible_obstacles:
                    boid.obstacle_avoidance(obstacle)
            boid.goal(*pos)
            boid.update(False)

        rendering.update_rendering()
    rendering.quit()


if __name__ == "__main__":
    main()
