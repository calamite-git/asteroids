import pygame

class SpeedPerk:
    def __init__(self, x, y, duration=5):
        self.position = pygame.Vector2(x, y)
        self.radius = 10
        self.duration = duration  # How long the boost lasts in seconds

    def draw(self, screen):
        pygame.draw.circle(screen, "yellow", (int(self.position.x), int(self.position.y)), self.radius)

    def check_collision(self, player):
        distance = self.position.distance_to(player.position)
        return distance < self.radius + player.radius
