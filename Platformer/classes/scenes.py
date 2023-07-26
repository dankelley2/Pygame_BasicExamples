from . import gamestate, entities, controllers

# basic scene class with: name variable, start function, next_scene variable
class Scene:
    def __init__(self, name):
        self.name = name
        self.game_state = gamestate.GameState()
        self.engine: function = None
        self.next_scene = None
        self.dynamic_objects = []
        self.walls = []

    # def run(self, game_state):
    #     if self.engine is not None:
    #         self.engine(game_state)
    #         if self.next_scene is not None:
    #             self.next_scene.run(game_state)
    
    def draw(self):
        pass

    def setup(self):
        pass
    
    # add a dynamic object to the scene
    def add_dynamic_object(self, obj):
        self.dynamic_objects.append(obj)
    
    # add a wall to the scene
    def add_wall(self, wall):
        self.walls.append(wall)

    def remove_dynamic_object(self, obj):
        self.dynamic_objects.remove(obj)
    
    def remove_wall(self, wall):
        self.walls.remove(wall)
    
    def clear_dynamic_objects(self):
        self.dynamic_objects.clear()

    def clear_walls(self):
        self.walls.clear()
    
    def clear_all_objects(self):
        self.clear_dynamic_objects()
        self.walls.clear()


# level 1 scene class
class level_1(Scene):
    def __init__(self):
        super().__init__("level_1")
        self.next_scene = None
        self.setup()

    # setup the scene
    def setup(self):
        # Character controller setup
        player =  entities.Player(self.game_state.WIDTH // 2, 50, 20, 20, color=(255, 50, 50))
        self.character_controller = controllers.CharacterController(player)

        # Add to scene
        self.add_dynamic_object(player)

        # add walls around the edges of the screen
        self.add_wall(entities.Wall(0, 0, self.game_state.WIDTH, 20, color=(50, 50, 200)))
        self.add_wall(entities.Wall(0, 0, 20, self.game_state.HEIGHT, color=(50, 50, 200)))
        self.add_wall(entities.Wall(self.game_state.WIDTH - 20, 0, 20, self.game_state.HEIGHT, color=(50, 50, 200)))
        self.add_wall(entities.Wall(0, self.game_state.HEIGHT - 20, self.game_state.WIDTH, 20, color=(50, 50, 200)))
        # make a wall that spans half the screen horizontally
        self.add_wall(entities.Wall(self.game_state.WIDTH // 4, self.game_state.HEIGHT // 2, self.game_state.WIDTH // 2, 20, color=(50, 50, 200)))
        # make 20x20 walls in a staircase pattern
        for i in range(10):
            self.add_wall(entities.Wall(20 + i * 20, 20 + i * 20, 20, 20, color=(50, 50, 200)))

    # Draw background with two layers of objects
    def draw(self):
        # Fill the screen with black
        self.game_state.screen.fill((0, 0, 0))

        # Draw the walls
        for obj in self.walls:
            obj.draw(self.game_state.screen)

        # Draw the dynamic objects
        for obj in self.dynamic_objects:
            obj.draw(self.game_state.screen)