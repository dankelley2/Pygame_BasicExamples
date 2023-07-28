import pygame
import sys
from classes import gamestate, scenes


# Main game loop
def game_loop(game_state: gamestate.GameState, current_scene: scenes.Scene):
    while game_state.running:
        # Setup current scene
        current_scene.setup()

        # Process game events
        current_scene.run_engine()

        # Determine the next scene
        current_scene = current_scene.next_scene()

        # Test Exit condition
        if current_scene is None:
            break


# main function for the program
def main():

    # create game state object at start of program
    game_state = gamestate.GameState()

    # Choose a scene to start on
    initial_scene = scenes.Level_1(game_state)

    # run game loop function, pass game state object as parameter/argument
    game_loop(game_state, initial_scene)

    # Quit Pygame
    pygame.quit()
    sys.exit()


# Entry Point of python file. This is where the program starts
if __name__ == "__main__":
    main()

