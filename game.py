import pygame
import sys
from customStuff import gameClasses, physics

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
        self.mvmt_delta = 3
        self.JUMP_SPEED = 3
        self.GRAVITY = 0.1
        self.player =  gameClasses.Player(self.WIDTH // 2, self.HEIGHT // 2, 20, 20, color=(255, 50, 50))
        self.vy = 0
        self.bullets = []

# Main game loop
def game_loop(game_state: GameState):
    while game_state.running:
        # Process game events
        run_engine(game_state)

        # draw everything
        draw_game(game_state)

        # Limit the frame rate
        game_state.clock.tick(game_state.FPS)


# Process game events
def run_engine(game_state: GameState):

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False # quit the game when the user clicks the X
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (game_state.player.standing or game_state.player.bottom >= game_state.HEIGHT):
                game_state.player.standing = False
                game_state.player.add_velocity(vx= 0, vy= -game_state.JUMP_SPEED)  # Give it an upward speed for jumping
            if event.key == pygame.K_ESCAPE:
                game_state.running = False # can also quit using escape key

        # check for mouse left click
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # get the position of the mouse
            pos = pygame.mouse.get_pos()
            # create a wall at the mouse position snapped to the nearest 20x20 grid
            gameClasses.Wall(pos[0] - pos[0] % 20, pos[1] - pos[1] % 20, 20, 20, color=(50, 50, 255))

    # Get a list of all pressed keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and game_state.player.left - game_state.mvmt_delta > 0:
        game_state.player.move_by(dx= -game_state.mvmt_delta, dy=0)
    if keys[pygame.K_d] and game_state.player.right + game_state.mvmt_delta < game_state.WIDTH:
        game_state.player.move_by(dx= game_state.mvmt_delta, dy=0)

    # Add gravity to the y velocity
    # but only if the player is not standing on a wall
    if not game_state.player.standing:
        game_state.player.vy += game_state.GRAVITY

    # step the physical objects
    for obj in gameClasses.Physical.all_objects:
        obj.step()
        collisions = physics.generate_collision_pairs(gameClasses.Physical.all_objects)
        if len(collisions) > 0:
            physics.resolve_collision_pairs(collisions)

    # generate collision pairs for the physical objects


    # Add velocity to y position (with bounds checking)
    if game_state.player.y < 0:  # Hitting the top of the screen
        game_state.player.y = 0
        game_state.player.vy = 0
    elif game_state.player.y > game_state.HEIGHT - game_state.player.height:  # Hitting the bottom of the screen
        game_state.player.y = game_state.HEIGHT - game_state.player.height
        game_state.player.vy = 0


# draw function for the program
def draw_game(game_state: GameState):
    global bullets

    # Fill the screen with black
    game_state.screen.fill((0, 0, 0))

    # Draw the physics objects
    for obj in gameClasses.Physical.all_objects:
        obj.draw(game_state.screen)

    # Draw the bullets
    for bullet in game_state.bullets:
        bullet.draw(game_state.screen)

    # Swap display buffers
    pygame.display.flip()


# main function for the program
def main():

    # create game state object at start of program
    game_state = GameState()

    # run game loop function, pass game state object as parameter/argument
    game_loop(game_state)

    # Quit Pygame
    pygame.quit()
    sys.exit()


# Entry Point of python file. This is where the program starts
if __name__ == "__main__":
    main()

