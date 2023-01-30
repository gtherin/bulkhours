import pygame
from simulation import PyGameRendering
from button import Button


def main():

    rendering = PyGameRendering()
    rendering.add_boids("boid_list", 70, obstacle_avoidance_weight=15, goal_weight=0, field_of_view=70)
    rendering.add_boids("predator_list", 5, obstacle_avoidance_weight=0, goal_weight=50, field_of_view=70, max_speed=8.5)
    rendering.add_obstacle(3)

    but = Button('Yo man', rendering.screen)

    rendering.prepare()

    while rendering.running:

        rendering.get_event()
        pos = pygame.mouse.get_pos()

        # Scan for boids and predators to pay attention to
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

            for predator in rendering.predator_list:
                distance = boid.distance(predator)
                if distance < boid.field_of_view:
                    avoid = True

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
            if avoid:
                boid.flee(predator)
            else:
                #boid.goal(*pos)
                boid.go_to_middle()
            boid.update(True)

        for predator in rendering.predator_list:
            closeboid = []
            rendering.close_prey.empty()
            for otherboid in rendering.predator_list:
                if otherboid == predator:
                    continue
                distance = predator.distance(otherboid)
                if distance < predator.field_of_view:
                    closeboid.append(otherboid)
            for boid in rendering.boid_list:
                distance = boid.distance(boid)
                if distance < predator.field_of_view:
                    rendering.close_prey.add(boid)

            # Apply the rules of the boids
            predator.cohesion(closeboid)
            predator.alignment(closeboid)
            predator.separation(closeboid, 20)
            predator.attack(rendering.close_prey)
            predator.update(True)
            collisions = pygame.sprite.spritecollide(predator, rendering.close_prey, True)

        but.draw()
        rendering.update_rendering()
    rendering.quit()


if __name__ == "__main__":
    main()
