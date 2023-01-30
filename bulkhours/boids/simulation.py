import pygame
import random

from boid import Boid
from obstacle import Obstacle


class PyGameRendering:

    def __init__(self) -> None:

        pygame.init()
        Boid.width, Boid.height = pygame.display.Info().current_w, pygame.display.Info().current_h - 40
        self.border = 30
        self.screen = pygame.display.set_mode((Boid.width, Boid.height))
        pygame.display.set_caption('Boids')

        # Fill background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0)) # BLACK = (0, 0, 0)

        self.boid_list = pygame.sprite.Group()
        self.predator_list = pygame.sprite.Group()
        self.obstacle_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.LayeredDirty()
        self.close_prey = pygame.sprite.Group()
        self.rebound_on_border = False

    def get_init_pos(self, border=False):
        return [random.randint(0, Boid.width), random.randint(0, Boid.height)] if not border else [random.randint(self.border, Boid.width - self.border), random.randint(self.border, Boid.height - self.border)]

    def add_boids(self, boids_list, nboids, cohesion_weight=100, alignment_weight=40, separation_weight=5, obstacle_avoidance_weight=10, goal_weight=100, field_of_view=200, max_speed=8):
        img_file = "bulkhours/boids/predator.png" if "predator" in boids_list else "bulkhours/boids/boid.png"
        x, y = self.get_init_pos("predator" in boids_list)

        for _ in range(nboids):
            boid = Boid(x, y, cohesion_weight, alignment_weight, separation_weight, obstacle_avoidance_weight, goal_weight, field_of_view, max_speed, img_file)
            getattr(self, boids_list).add(boid)
            self.all_sprites_list.add(boid)

    def add_obstacle(self, nboids):
        for i in range(nboids):
            obstacle = Obstacle(random.randint(0 + self.border, Boid.width - self.border), random.randint(0 + self.border, Boid.height - self.border))
            # Add the obstacle to the lists of objects
            self.obstacle_list.add(obstacle)
            self.all_sprites_list.add(obstacle)

    def quit(self):
        pygame.quit()

    def prepare(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites_list.clear(self.screen, self.background)

    def update_rendering(self):
        if self.rebound_on_border:
            self.rebound()

        # Create list of dirty sprites
        rects = self.all_sprites_list.draw(self.screen)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.update(rects)
        # pygame.time.delay(10)
        # Used to manage how fast the screen updates
        self.clock.tick(60)

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("QUIT FIRST")
                self.running = False
            if event.type != pygame.KEYDOWN:
                return
            
            mods = pygame.key.get_mods()

            if event.key == pygame.K_p:
                if (mods and pygame.KMOD_LSHIFT) or (mods and pygame.KMOD_CAPS):
                    print("Add predator", self.predator_list)
                    self.add_boids("predator_list", 1, obstacle_avoidance_weight=0, goal_weight=50, field_of_view=70, max_speed=8.5)
                else:
                    print("Delete predator", self.predator_list)
                    self.predator_list.sprites()[-1].kill()
                self.prepare()
            elif event.key == pygame.K_b:
                if (mods and pygame.KMOD_LSHIFT) or (mods and pygame.KMOD_CAPS):
                    print("Add boid", self.boid_list)
                    self.add_boids("boid_list", 1, obstacle_avoidance_weight=15, goal_weight=0, field_of_view=70)
                else:
                    print("Delete boid", self.boid_list)
                    self.boid_list.sprites()[-1].kill()
                self.prepare()
            elif event.key == pygame.K_o:
                if (mods and pygame.KMOD_LSHIFT) or (mods and pygame.KMOD_CAPS):
                    print("Add obstacle", self.obstacle_list)
                    self.add_obstacle(1)
                else:
                    print("Delete obstacle", self.obstacle_list)
                    self.obstacle_list.sprites()[-1].kill()
                self.prepare()
            elif event.key == pygame.K_r:
                print("rebound_on_border")
                self.rebound_on_border = not self.rebound_on_border
            elif event.key == pygame.K_ESCAPE:
                print("QUIT K_ESCAPE")
                self.running = False


    def rebound(self):
        # TODO Either make this work or add a genetic algorithm and kill them
        # If a predator manages to touch a prey, the prey gets eaten!
        for boid in self.boid_list:
            #collisions = pygame.sprite.spritecollide(predator, self.close_prey, True)
            collisions = pygame.sprite.spritecollide(boid, self.obstacle_list, False)
            for obstacle in collisions:
                boid.velocityX += -1 * (obstacle.real_x - boid.rect.x)
                boid.velocityY += -1 * (obstacle.real_y - boid.rect.y)
