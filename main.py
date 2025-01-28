import sys
import pygame
import random  # For random perk spawning
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from speed_boost import SpeedPerk


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Perk-related variables
    perks = []  # List to hold active perks
    perk_spawn_timer = 0  # Timer for when to spawn the next perk

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update perk spawn timer and spawn new perks
        perk_spawn_timer -= dt
        if perk_spawn_timer <= 0:
            x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
            perks.append(SpeedPerk(x, y))
            perk_spawn_timer = random.randint(5, 10)  # Next perk spawns in 5-10 seconds

        # Update all game objects
        for obj in updatable:
            obj.update(dt)

        # Check collisions between player and perks
        for perk in perks[:]:
            if perk.check_collision(player):
                player.activate_boost(perk.duration)  # Activate the speed boost
                perks.remove(perk)  # Remove the perk after collection

        # Check collisions between asteroids, player, and shots
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                sys.exit()

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()

        # Draw everything
        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        # Draw perks
        for perk in perks:
            perk.draw(screen)

        pygame.display.flip()

        # Limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
