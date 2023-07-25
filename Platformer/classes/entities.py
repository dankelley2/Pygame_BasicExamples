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
        self.mass = self.width * self.height
        self.imass = 1 / self.mass
        self.restitution = 0.5
        self.velocity = pgm.Vector2(vx, vy)
        self.locked = False
        Physical.all_objects.append(self)
            
    # move the object based on it's velocity
    # collision_handler is a function that takes in a collision object and handles the collision
    def step(self):
        self.move_by(self.velocity.x, self.velocity.y)

    # add velocity
    def add_velocity(self, vx, vy):
        self.velocity.x += vx
        self.velocity.y += vy

    # add velocity
    def set_velocity(self, vx=None, vy=None):
        if vx is not None:
            self.velocity.x = vx
        if vy is not None:
            self.velocity.y = vy

    # destroy the object
    def destroy(self):
        Physical.all_objects.remove(self)

    # resolve the collision effects within the class
    def hit_by(self, other, collision_vector: pgm.Vector2):
        pass



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
            self.standing = False

        def hit_by(self, other, collision_vector: pgm.Vector2):
            # if the other object is a wall
            if isinstance(other, Wall):
                # if the collision vector is pointing up, set the y velocity to 0, and standing to true
                if collision_vector.y > 0 and not self.standing:
                    self.vy = 0
                    self.standing = True

# wall class that represents a wall in the game
class Wall(Physical):

    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color, 0, 0)
        self.locked = True
