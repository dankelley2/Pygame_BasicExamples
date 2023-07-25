from itertools import combinations
import pygame.math as pgm
import pygame

def generate_collision_pairs(list_of_objects):
    collision_pairs = []

    # Use combinations to get all possible pairs from all_objects
    for obj1, obj2 in combinations(list_of_objects, 2):
        if obj1.rect.colliderect(obj2.rect):  # Check if rectangles collide
            collision_pairs.append((obj1, obj2))  # If they collide, add them as a pair

    return collision_pairs

def resolve_collision_pairs(pairs):
    for pair in pairs:
        obj1, obj2 = pair
        obj1.resolve_collision(obj2) # Apply the collision resolution method