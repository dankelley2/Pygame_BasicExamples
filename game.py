import pygame
import sys
from customStuff import gameClasses

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
DISTANCE_TO_MOVE = 5
JUMP_SPEED = 5
GRAVITY = 0.1
FPS = 60  # Frames per second

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a clock
clock = pygame.time.Clock()

# Create a square
square = pygame.Rect(WIDTH // 2, HEIGHT // 2, 20, 20)

# Velocity in y direction
vy = 0

# Game loop variable
running = True

#global list of bullets
bullets = [] 


# Main game loop
def game_loop():
    while running:
        # Process game events
        run_engine()

        # draw everything
        draw_game()

        # Limit the frame rate
        clock.tick(FPS)


# Process game events
def run_engine():
    global vy
    global square
    global running
    global bullets

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # quit the game when the user clicks the X
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and square.bottom >= HEIGHT:
                vy = -JUMP_SPEED  # Give it an upward speed for jumping
            if event.key == pygame.K_ESCAPE:
                running = False # can also quit using escape key

        # check for mouse left click
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # get the position of the mouse
            pos = pygame.mouse.get_pos()
            # create a bullet at the mouse position
            bullet = gameClasses.Bullet(pos[0], pos[1], 10, (255, 255, 255))

    # Get a list of all pressed keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and square.left - DISTANCE_TO_MOVE > 0:
        square.x -= DISTANCE_TO_MOVE
    if keys[pygame.K_d] and square.right + DISTANCE_TO_MOVE < WIDTH:
        square.x += DISTANCE_TO_MOVE

    # Add gravity to the y velocity
    vy += GRAVITY

    # Add velocity to y position (with bounds checking)
    square.y += vy
    if square.y < 0:  # Hitting the top of the screen
        square.y = 0
        vy = 0
    elif square.y > HEIGHT - square.height:  # Hitting the bottom of the screen
        square.y = HEIGHT - square.height
        vy = 0


# draw function for the program
def draw_game():
    global bullets

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the square (the player)
    pygame.draw.rect(screen, (255, 0, 0), square)

    for bullet in gameClasses.Bullet.all_bullets:
        bullet.draw(screen)

    # Swap display buffers
    pygame.display.flip()


# main function for the program
def main():

    # run game loop function
    game_loop()

    # Quit Pygame
    pygame.quit()
    sys.exit()


# create entry point for the program
if __name__ == "__main__":
    main()

