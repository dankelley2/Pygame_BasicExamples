from itertools import combinations
import pygame.math as pgm
import pygame
import math
from . import entities



# Manifold class that contains the two objects that collided, the penetration depth, and the normal
class Manifold:
    def __init__(self, A, B):
        self.A : entities.Physical = A
        self.B : entities.Physical = B
        self.Penetration = 0
        self.Normal = None

# generate_collision_pairs takes in a list of objects and returns a list of collision Manifold objects
def generate_collision_pairs(list_of_objects):
    collision_pair_manifolds : list(Manifold) = []

    # Use combinations to get all possible pairs from all_objects
    for obj1, obj2 in combinations(list_of_objects, 2):
        if obj1.rect.colliderect(obj2.rect):  # Check if rectangles collide
            if obj1.locked and obj2.locked:  # If both objects are static, skip
                continue
            collision_pair_manifolds.append(Manifold(A=obj1, B=obj2))  # If they collide, add them as a pair

    return collision_pair_manifolds


# resolve_collision_pairs takes in a list of collision Manifold objects and runs aabb_vs_aabb on them
# if a collision is detected, it runs resolve_collision on the collision Manifold
def resolve_collision_pairs(collision_manifolds):
    for m in collision_manifolds:
        if (isinstance(m.A, entities.Player) and isinstance(m.B, entities.Player)):
            collision_handler = circle_vs_circle
        if (isinstance(m.A, entities.Player) or isinstance(m.B, entities.Player)) \
            and not (isinstance(m.A, entities.Player) and isinstance(m.B, entities.Player)):
            collision_handler = aabb_vs_circle
            if isinstance(m.A, entities.Player):
                m.A, m.B = m.B, m.A
        if (isinstance(m.A, entities.Wall) and isinstance(m.B, entities.Wall)):
            collision_handler = aabb_vs_aabb
        if collision_handler(m):
            resolve_collision(m)
            positional_correction(m)
            m.A.hit_by(m.B, m.Normal)
            m.B.hit_by(m.A, m.Normal * -1)


# resolve_collision takes in a collision Manifold and resolves the collision
def resolve_collision(m : Manifold):
    rv = m.B.velocity - m.A.velocity

    if math.isnan(m.Normal.x) or math.isnan(m.Normal.y):
        return

    velAlongNormal = rv.dot(m.Normal)

    if velAlongNormal > 0:
        return

    e = min(m.A.restitution, m.B.restitution)

    j = -(1 + e) * velAlongNormal
    j = j / (m.A.imass + m.B.imass)

    impulse = m.Normal * j

    m.A.velocity = m.A.velocity - impulse * m.A.imass if not m.A.locked else m.A.velocity
    m.B.velocity = m.B.velocity + impulse * m.B.imass if not m.B.locked else m.B.velocity

# positional_correction takes in a collision Manifold and corrects the position of the objects
def positional_correction(m: Manifold):
    percent = 0.6  # usually 20% to 80%
    correction = m.Normal * (percent * (m.Penetration / (m.A.imass + m.B.imass)))
    
    if not m.A.locked:
        vel = -correction * m.A.imass
        m.A.move_by(vel.x, vel.y)

    if not m.B.locked:
        vel = correction * m.B.imass
        m.B.move_by(vel.x, vel.y)


# Function that takes in a Manifold, modifies it and returns a boolean based on whether or not the objects collided
def aabb_vs_aabb(m: Manifold) -> bool:
    # Setup a couple pointers to each object
    A = m.A
    B = m.B

    abox = A.rect
    bbox = B.rect

    # Vector from A to B
    vector = B.center - A.center

    # Calculate half extents along x axis for each object
    a_extent = (abox.right - abox.left) / 2
    b_extent = (bbox.right - bbox.left) / 2

    # Calculate overlap on x axis
    x_overlap = a_extent + b_extent - abs(vector.x)

    # SAT test on x axis
    if x_overlap > 0:
        # Calculate half extents along y axis for each object
        a_extent = (abox.bottom - abox.top) / 2
        b_extent = (bbox.bottom - bbox.top) / 2

        # Calculate overlap on y axis
        y_overlap = a_extent + b_extent - abs(vector.y)

        # SAT test on y axis
        if y_overlap > 0:
            # Find out which axis is axis of least penetration
            if x_overlap < y_overlap:
                # Point towards B knowing that n points from A to B
                if vector.x < 0:
                    m.Normal = pgm.Vector2(-1, 0)
                else:
                    m.Normal = pgm.Vector2(1, 0)

                m.Penetration = x_overlap
                return True

            # Point toward B knowing that n points from A to B
            if vector.y < 0:
                m.Normal = pgm.Vector2(0, -1)
            else:
                m.Normal = pgm.Vector2(0, 1)

            m.Penetration = y_overlap
            return True

    return False


# Function that takes in a Manifold, modifies it and returns a boolean based on whether or not the objects collided
def circle_vs_circle(m: Manifold) -> bool:
    # Setup a couple pointers to each object
    A = m.A
    B = m.B

    # Vector from A to B
    vector = B.center - A.center

    # Combine the radii of both circles
    r = A.width/2 + B.width/2
    r *= r

    # If the squared distance between the circles' centers is greater than the squared combined radii, no collision
    if vector.length_squared() > r:
        return False

    # Circles have collided, now compute manifold
    d = vector.length() # perform actual sqrt

    # If distance between circles is not zero
    if d != 0:
        # Distance is difference between radius and distance
        m.Penetration = A.width/2 + B.width/2 - d

        # Utilize our d since we performed sqrt on it already within length()
        # Points from A to B, and is a unit vector
        m.Normal = vector / d
        return True

    # Circles are on same position
    # Choose random (but consistent) values
    m.Penetration = A.width/2
    m.Normal = pgm.Vector2(1, 0)
    return True
       

# Function that takes in a Manifold, modifies it and returns a boolean based on whether or not the objects collided
def aabb_vs_circle(m: Manifold) -> bool:
    # Setup a couple pointers to each object
    # Box Shape
    box = m.A

    # Circle Shape
    circle = m.B

    # Vector from box to circle
    vector = circle.center - box.center

    # Closest point on box to center of circle
    closest = vector.copy()

    # Calculate half extents along each axis
    x_extent = (box.rect.right - box.rect.left) / 2
    y_extent = (box.rect.bottom - box.rect.top) / 2

    # Clamp point to edges of the AABB
    closest.x = max(-x_extent, min(x_extent, closest.x))
    closest.y = max(-y_extent, min(y_extent, closest.y))

    inside = False

    # Circle is inside the AABB, so we need to clamp the circle's center
    # to the closest edge
    if vector == closest:
        inside = True

        # Find closest axis
        if abs(vector.x) < abs(vector.y):
            # Clamp to closest extent
            if closest.x > 0:
                closest.x = x_extent
            else:
                closest.x = -x_extent
        # y axis is shorter
        else:
            # Clamp to closest extent
            if closest.y > 0:
                closest.y = y_extent
            else:
                closest.y = -y_extent

    normal = vector - closest
    if normal.length_squared() == 0:
        normal = pgm.Vector2(0, 1)
    d = normal.length_squared()
    r = circle.rect.width / 2

    # Early out of the radius is shorter than distance to closest point and
    # Circle not inside the AABB
    if d > r * r and not inside:
        return False

    # Avoided sqrt until we needed
    d = d ** 0.5

    # Collision normal needs to be flipped to point outside if circle was
    # inside the AABB
    if inside:
        m.Normal = (-normal).normalize()
        m.Penetration = r - d
    else:
        # If pushing up at all, go straight up (gravity hack)
        m.Normal = normal.normalize()
        m.Penetration = r - d

    return True
