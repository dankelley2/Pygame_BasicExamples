import pygame
import pygame.math as pgm

# Drawable class that represents an instance of an object in the game
# It has an initial size, keeps track of it's rectangle object, and has a draw method
class Drawable:

    # getters for the x and y position of the object
    @property
    def x(self):
        return self.rect.x
    
    @x.setter
    def x(self, value):
        self.rect.x = value
    
    @property
    def y(self):
        return self.rect.y
    
    @y.setter
    def y(self, value):
        self.rect.y = value

    # getters for the left, right, top, and bottom of the object
    @property
    def left(self):
        return self.rect.left
    
    @property
    def right(self):
        return self.rect.right
    
    @property
    def top(self):
        return self.rect.top
    
    @property
    def bottom(self):
        return self.rect.bottom

    @property
    def center(self):
        return pgm.Vector2(self.rect.centerx, self.rect.centery)

    def __init__(self, x, y, width, height, color):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    
    # draw the object
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    # relative move function that moves the rect based on the x and y parameters
    def move_by(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    # absolute move function that moves the rect to the x and y parameters
    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y

    # destroy the object
    def destroy(self):
        pass

# Physical class that inherits from Drawable, and contains vx and vy variables to track velocity
# It contains additional methods to add velocity and move the object based on it's velocity
class Physical(Drawable):

    all_objects=[]

    def __init__(self, x, y, width, height, color, vx, vy):
        super().__init__(x, y, width, height, color)
        self.vx = vx
        self.vy = vy
        self.mass = 0
        Physical.all_objects.append(self)
            
    # move the object based on it's velocity
    # collision_handler is a function that takes in a collision object and handles the collision
    def step(self):
        self.move_by(self.vx, self.vy)

    # add velocity
    def add_velocity(self, vx, vy):
        self.vx += vx
        self.vy += vy

    # destroy the object
    def destroy(self):
        Physical.all_objects.remove(self)

    # resolve the collision effects within the class
    def resolve_collision_effects(self, other, collision_vector):
        pass

    # resolve a collision with another object
    def resolve_collision(self, other):

        # Padding amount for resolving collisions. This is to prevent objects from getting stuck inside each other
        PADDING = 0

        MULT = 1
        # Create vectors for the objects' positions
        obj1_pos = pgm.Vector2(self.x, self.y)
        obj2_pos = pgm.Vector2(other.x, other.y)

        # Calculate the collision vector (from self to other)
        collision_vector = obj2_pos - obj1_pos

        # test if the vector is length 0
        if collision_vector.length() == 0:
            return

        # Find the overlap between the two rectangles along the collision vector
        overlap = abs(collision_vector.length() - (self.width / 2) - (other.width / 2))

        # TODO: Need to fix rect rect collision, and find overlap based on the distance between the closest two walls, instead of distance from center to center

        # Snap the collision vector to the nearest 90 degrees
        if abs(collision_vector.x) > abs(collision_vector.y):
            collision_vector.y = 0
        else:
            collision_vector.x = 0

        # Normalize the collision vector (make it have length 1)
        collision_vector.normalize_ip()

        # Check the masses of the objects and move them accordingly
        if self.mass > 0 and other.mass > 0:
            # Move both objects backwards along the collision vector by 50% of the overlap amount
            self.move_by(-collision_vector.x * (overlap / 2 + PADDING) * MULT, -collision_vector.y * (overlap / 2 + PADDING) * MULT)
            other.move_by(collision_vector.x * (overlap / 2 + PADDING) * MULT, collision_vector.y * (overlap / 2 + PADDING) * MULT)
        elif self.mass > 0:
            # Move self backwards along the collision vector by the full overlap amount
            self.move_by(-collision_vector.x * (overlap + PADDING) * MULT, -collision_vector.y * (overlap + PADDING) * MULT)
        elif other.mass > 0:
            # Move other backwards along the collision vector by the full overlap amount
            other.move_by(collision_vector.x * (overlap + PADDING) * MULT, collision_vector.y * (overlap + PADDING) * MULT)
        
        # resolve the collision effects within the class
        self.resolve_collision_effects(other, collision_vector)
        other.resolve_collision_effects(self, -collision_vector)


# class that represents a bullet in pygame
# It has an initial size, keeps track of it's circle object, and has a draw method
# This class inherits from Drawable, which is an example of polymorphism
class Bullet(Drawable):

    def __init__(self, x, y, r, color):
        super().__init__(x, y, r, r, color)
    
    # draw the bullet, this overrides the draw method in Drawable
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

# player class that represents the player in the game
# This class inherits from Drawable, which is an example of polymorphism
class Player(Physical):
    
        def __init__(self, x, y, width, height, color, vx=0, vy=0):
            super().__init__(x, y, width, height, color, vx, vy)

            # Add mass so this object moves during a collision
            self.mass = 100
            self.standing = False

        def resolve_collision_effects(self, other, collision_vector):
            # If the other object is a bullet, destroy the bullet
            if isinstance(other, Bullet):
                other.destroy()
            # if the other object is a wall
            elif isinstance(other, Wall):
                # if the collision vector is pointing up, set the y velocity to 0, and standing to true
                if collision_vector.y > 0 and not self.standing:
                    self.vy = 0
                    self.standing = True

# wall class that represents a wall in the game
class Wall(Physical):

    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color, 0, 0)
