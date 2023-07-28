from . import entities, physics, controllers, gamestate
from abc import ABC, abstractmethod
import pygame

class Scene(ABC):
    def __init__(self, game_state : gamestate.GameState):
        self.game_state = game_state

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def run_engine(self):
        pass

    @abstractmethod
    def next_scene(self):
        pass

class Level_1(Scene):
    def setup(self):
        # clear all entities from the game state
        clear_entities(self.game_state)

        # add walls around the edges of the screen
        entities.Wall(0, 0, self.game_state.WIDTH, 20, color=(50, 50, 200))
        entities.Wall(0, 0, 20, self.game_state.HEIGHT, color=(50, 50, 200))
        entities.Wall(self.game_state.WIDTH - 20, 0, 20, self.game_state.HEIGHT, color=(50, 50, 200))
        entities.Wall(0, self.game_state.HEIGHT - 20, self.game_state.WIDTH, 20, color=(50, 50, 200))

        # make a wall that spans half the screen horizontally
        entities.Wall(self.game_state.WIDTH // 4, self.game_state.HEIGHT // 2, self.game_state.WIDTH // 2, 20, color=(50, 50, 200))

        # make 20x20 walls in a staircase pattern
        for i in range(20):
            entities.Wall(10 + i * 10, 10 + i * 10, 10, 10, color=(50, 50, 200))

        # make a Goal that is 100 px from the bottom, and 80 px from the right
        entities.Goal(self.game_state.WIDTH - 80, self.game_state.HEIGHT - 100)
        # make a Gola that is 100 px from the bottom, and 40 px from the left
        entities.Goal(40, self.game_state.HEIGHT - 100)

        # Create Character controller    
        self.player = entities.Player(self.game_state.WIDTH // 2, 50, 20, 20, color=(255, 50, 50))
        self.game_state.character_controller = controllers.CharacterController(self.player)

    # run the engine for this scene
    def run_engine(self):
        while True and self.game_state.running:
            basic_engine(self.game_state)
            basic_draw(self.game_state)
            self.game_state.clock.tick(self.game_state.FPS)
            if self.player.score == 2:
                break

    # determine the next scene, implment this later
    def next_scene(self):
        # determine and return the next scene
        return Level_2(self.game_state)


#Level 2 is the same as level 1, but with a different background color
class Level_2(Scene):
    def setup(self):
        # clear all entities from the game state
        clear_entities(self.game_state)

        # add walls around the edges of the screen
        entities.Wall(0, 0, self.game_state.WIDTH, 20, color=(200, 200, 200))
        entities.Wall(0, 0, 20, self.game_state.HEIGHT, color=(200, 200, 200))
        entities.Wall(self.game_state.WIDTH - 20, 0, 20, self.game_state.HEIGHT, color=(200, 200, 200))
        entities.Wall(0, self.game_state.HEIGHT - 20, self.game_state.WIDTH, 20, color=(200, 200, 200))

        # make a wall that spans half the screen horizontally
        entities.Wall(self.game_state.WIDTH // 4, self.game_state.HEIGHT // 2, self.game_state.WIDTH // 2, 20, color=(50, 50, 0))

        # make 20x20 walls in a staircase pattern
        for i in range(20):
            entities.Wall(10 + i * 10, 10 + i * 10, 10, 10, color=(50, 50, 200))

        # Create Character controller    
        player = entities.Player(self.game_state.WIDTH // 2, 50, 20, 20, color=(255, 50, 50))
        self.game_state.character_controller = controllers.CharacterController(player)

    # run the engine for this scene
    def run_engine(self):
        while True and self.game_state.running:
            basic_engine(self.game_state)
            basic_draw(self.game_state)
            self.game_state.clock.tick(self.game_state.FPS)

    # determine the next scene, implment this later
    def next_scene(self):
        # determine and return the next scene
        return None

# clear Wall and Physical of all entities
def clear_entities(game_state: gamestate.GameState):
    entities.Wall.list_of_walls.clear()
    entities.Physical.all_objects.clear()

def basic_engine(game_state: gamestate.GameState):
    # Process game events
    # Set up character controller input object
    game_state.input = controllers.Input()

    # Event handling (Conrols etc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False # quit the game when the user clicks the X
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_state.input.jump = True
            if event.key == pygame.K_ESCAPE:
                game_state.running = False # can also quit using escape key

        # check for mouse left click
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # get the position of the mouse
            pos = pygame.mouse.get_pos()
            # create a wall at the mouse position snapped to the nearest 20x20 grid
            entities.Wall(pos[0] - pos[0] % 20, pos[1] - pos[1] % 20, 20, 20, color=(50, 50, 255))
            entities.Wall.try_merge_walls()

    # Get a list of all pressed keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        game_state.input.left = True
    if keys[pygame.K_d]:
        game_state.input.right = True
    
    # Run character controller
    game_state.character_controller.set_input(game_state.input)

    # Run physics Simulation
    for obj in entities.Physical.all_objects:
        # add gravity to all objects
        if not obj.locked:
            obj.add_velocity(0, game_state.GRAVITY)
        # move all objects
        obj.step()
        # Check for and resolve collisions
        collision_manifolds = physics.generate_collision_pairs(entities.Physical.all_objects)
        if len(collision_manifolds) > 0:
            physics.resolve_collision_pairs(collision_manifolds)

            

# draw function for the program
def basic_draw(game_state: gamestate.GameState):
    global bullets

    # Fill the screen with black
    game_state.screen.fill((0, 0, 0))

    # Draw the physics objects
    for obj in entities.Physical.all_objects:
        obj.draw(game_state.screen)

    # Swap display buffers
    pygame.display.flip()