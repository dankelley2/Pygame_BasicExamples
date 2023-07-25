from itertools import combinations
import pygame.math as pgm
import pygame


def generate_collision_pairs(list_of_objects):
    collision_pairs = []

    # Use combinations to get all possible pairs from all_objects
    for obj1, obj2 in combinations(list_of_objects, 2):
        if obj1.rect.colliderect(obj2.rect):  # Check if rectangles collide
            if obj1.mass == 0 and obj2.mass == 0:  # If both objects are static, skip
                continue
            collision_pairs.append((obj1, obj2))  # If they collide, add them as a pair

    return collision_pairs


def resolve_collision_pairs(pairs):
    for pair in pairs:
        obj1, obj2 = pair
        obj1.resolve_collision(obj2) # Apply the collision resolution method


class Manifold:
    def __init__(self):
        self.A = None
        self.B = None
        self.Penetration = 0
        self.Normal = None


def aabb_vs_aabb(m):
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
                    m.Normal = Vec2(-1, 0)
                else:
                    m.Normal = Vec2(1, 0)

                m.Penetration = x_overlap
                return True

            # Point toward B knowing that n points from A to B
            if vector.x < 0:
                m.Normal = Vec2(0, -1)
            else:
                m.Normal = Vec2(0, 1)

            m.Penetration = y_overlap
            return True

    return False


def resolve_collision(m):
    rv = m.B.Velocity - m.A.Velocity

    if math.isnan(m.Normal.x) or math.isnan(m.Normal.y):
        return

    velAlongNormal = rv.dot(m.Normal)

    if velAlongNormal > 0:
        return

    e = min(m.A.Restitution, m.B.Restitution)

    j = -(1 + e) * velAlongNormal
    j = j / (m.A.IMass + m.B.IMass)

    impulse = m.Normal * j

    m.A.Velocity = m.A.Velocity - impulse * m.A.IMass if not m.A.Locked else m.A.Velocity
    m.B.Velocity = m.B.Velocity + impulse * m.B.IMass if not m.B.Locked else m.B.Velocity


def positional_correction(m):
    percent = 0.6  # usually 20% to 80%
    correction = m.Normal * (percent * (m.Penetration / (m.A.IMass + m.B.IMass)))
    
    if not m.A.Locked:
        m.A.Move(-correction * m.A.IMass)

    if not m.B.Locked:
        m.B.Move(correction * m.B.IMass)

