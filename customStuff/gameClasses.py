import pygame

# class that represents a bullet in pygame
# It has an initial size, keeps track of it's circle object, and has a draw method
class Bullet:
    # static variable that keeps track of all bullets
    all_bullets = []

    def __init__(self, x, y, r, color):
        self.r = r
        self.circle = pygame.Rect(x, y, r, r)
        self.color = color
        # add the bullet to the list of bullets
        Bullet.all_bullets.append(self)
    
    # draw the bullet
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.circle)

    # destroy the bullet
    def destroy(self):
        Bullet.all_bullets.remove(self)