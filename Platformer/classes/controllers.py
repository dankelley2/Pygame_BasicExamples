from . import entities

# input class that represents the input state of the game for a character controller
class Input:
    def __init__(self):
        self.left = False
        self.right = False
        self.jump = False
        self.down = False

# character controller class that handles player input and movement
class CharacterController:
    def __init__(self, player: entities.Player):
        self.player = player
        self.move_delta_velocity = 1.0
        self.jump_velocity = 4.0

    # handle input for the player
    def handle_input(self, input: Input):

        # Left and Right Movement
        if input.left and self.player.velocity.x > -2:
            self.player.add_velocity(vx= -self.move_delta_velocity, vy=0)
        if input.right and self.player.velocity.x < 2:
            self.player.add_velocity(vx= self.move_delta_velocity, vy=0)

        # Jump
        if input.jump and self.player.standing:
            self.player.standing = False
            self.player.set_velocity(vy= -self.jump_velocity)
        #End Controls

    # run the character controller
    def set_input(self, input: Input):
        self.handle_input(input)