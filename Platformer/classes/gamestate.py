import pygame

class GameState:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), vsync=True)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.FPS = 60 # set FPS to something reasonable, Physics is locked to FPS at the moment
        self.GRAVITY = 0.15
