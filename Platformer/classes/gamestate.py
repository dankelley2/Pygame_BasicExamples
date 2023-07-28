import pygame

class GameState:
    def __init__(self):
        # Initialize pygame when this class is instantiated
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        # set up game loop variable, may move this to a function later
        self.running = True
        # set FPS to something reasonable
        self.FPS = 60
        # other setup stuff, will move this to a function later
        self.GRAVITY = 0.25