from itertools import combinations
import pygame.math as pgm
import pygame
import math
from . import entities

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
        if aabb_vs_aabb(m):
            resolve_collision(m)
            positional_correction(m)
            m.A.hit_by(m.B, m.Normal)
            m.B.hit_by(m.A, m.Normal * -1)

# Manifold class that contains the two objects that collided, the penetration depth, and the normal
class Manifold:
    def __init__(self, A, B):
        self.A : entities.Physical = A
        self.B : entities.Physical = B
        self.Penetration = 0
        self.Normal = None

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


def positional_correction(m: Manifold):
    percent = 0.6  # usually 20% to 80%
    correction = m.Normal * (percent * (m.Penetration / (m.A.imass + m.B.imass)))
    
    if not m.A.locked:
        vel = -correction * m.A.imass
        m.A.move_by(vel.x, vel.y)

    if not m.B.locked:
        vel = correction * m.B.imass
        m.B.move_by(vel.x, vel.y)

