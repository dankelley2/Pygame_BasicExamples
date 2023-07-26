import pygame
import pygame.math as pgm
from itertools import combinations
import math

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
        self.mass = width * height
        self.imass = 1 / self.mass
        self.restitution = 0.25
        self.velocity = pgm.Vector2(vx, vy)
        self.locked = False
        Physical.all_objects.append(self)
            
    # move the object based on it's velocity
    # collision_handler is a function that takes in a collision object and handles the collision
    def step(self):
        self.move_by(self.velocity.x, self.velocity.y)
        self.velocity.x *= 0.8

    # add velocity
    def add_velocity(self, vx=None, vy=None):
        if vx is not None:
            self.velocity.x += vx
        if vy is not None:   
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


# player class that represents the player in the game
# This class inherits from Drawable, which is an example of polymorphism
class Player(Physical):
    
    def __init__(self, x, y, width, height, color, vx=0, vy=0):
        super().__init__(x, y, width, height, color, vx, vy)
        self.standing = False
        self.mass = math.pi * (width / 2) ** 2
        self.imass = 1 / self.mass

    def hit_by(self, other, collision_vector: pgm.Vector2):
        # if the other object is a wall
        if isinstance(other, Wall):
            # if the collision vector is pointing up, set the y velocity to 0, and standing to true
            if collision_vector.y == 1.0 and not self.standing:
                self.vy = 0
                self.standing = True
        
    # draw the object
    def draw(self, screen):
        # draw an ellipse with pygame
        pygame.draw.ellipse(screen, self.color, self.rect)


# wall class that represents a wall in the game
class Wall(Physical):
    list_of_walls = []

    def try_merge_walls():
        removed_walls = []
        # Use combinations to get all possible pairs from all_objects
        for obj1, obj2 in combinations(Wall.list_of_walls, 2):
            # if removed_walls does not contian obj1 and obj2
            if obj2 in removed_walls:
                continue
            if obj1.x == obj2.x and (abs(obj1.y - obj2.y) == 20 or abs(obj1.bottom - obj2.bottom) == 20):
                if obj1.merge(obj2):
                    removed_walls.append(obj2)
                    # change to brown
                    obj1.color = (139, 69, 19)
        if len(removed_walls) > 0:
            Wall.try_merge_walls()

    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color, 0, 0)
        self.locked = True
        self.mass = 1000000
        Wall.list_of_walls.append(self)

    # function that merges two walls together
    def merge(self, other):
        # if this wall is above the other wall
        if self.bottom == other.top and self.rect.width == other.rect.width and self.rect.x == other.rect.x:
            self.rect.height += other.rect.height
            self.mass += other.mass
            other.destroy()
            return True
        # if this wall is below the other wall
        elif self.top == other.bottom and self.rect.width == other.rect.width and self.rect.x == other.rect.x:
            self.rect.height += other.rect.height
            self.rect.y = other.rect.y
            self.mass += other.mass
            other.destroy()
            return True
        return False
    
    def destroy(self):
        Wall.list_of_walls.remove(self)
        Physical.all_objects.remove(self)
