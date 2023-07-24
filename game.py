import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
SPEED = 5
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

# Main game loop
running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and square.bottom + SPEED >= HEIGHT:
                vy = -JUMP_SPEED  # Give it an upward speed for jumping
        # check for mouse left click
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # get the position of the mouse
            pos = pygame.mouse.get_pos()
            # check if the mouse is inside the square
            if square.collidepoint(pos):
                # change the color of the square
                break #square. = (0, 255, 0)


    # Get a list of all pressed keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and square.left - SPEED > 0:
        square.x -= SPEED
    if keys[pygame.K_d] and square.right + SPEED < WIDTH:
        square.x += SPEED

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

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the square
    pygame.draw.rect(screen, (255, 0, 0), square)

    # Swap buffers
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
