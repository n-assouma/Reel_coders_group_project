
# Andrei Sidorenko - 5750779

# =============================================================================
# Project Inventory — The Hollow Witness
# =============================================================================
# Libraries:
#   - pygame, json, os, sys, math, collections, typing, time
#
# Data Types:
#   - int, float, bool, str, None, tuple, list, dict, set, frozenset
#
# Data Structures:
#   - Graph (adjacency list), Tree (n-ary), Linked-list chain,
#     Capacity-bounded container, Counter, deque, JSON file
#
# Algorithms:
#   - Breadth-First Search, Path reconstruction, Merge sort, custom Bubble sort,
#     AABB collision detection, depth-sorting, Word-wrap layout,
#     Sprite animation, Linear search, JSON deserialisation, Route-with-blocker
#
# OOP Techniques:
#   - Inheritance, Polymorphism, Encapsulation, Abstraction, Composition,
#     Properties, Method overriding, Factory-style loading
#
# Programming Techniques:
#   - List comprehensions, filter/lambda, enumerate, zip,
#     Recursion, Ternary expressions, Short-circuit booleans,
#     Variadic *args, Type hints, f-strings, Context managers,
#     match/case, Tuple unpacking, Slicing, Augmented assignment
#
# Error Handling:
#   - Custom exceptions: RoomGraphError, EdgeNotExistError,
#     MaximumEvidenceReachedError, EvidenceNotFoundError, FurnitureCollisionError
#   - try/except: FileNotFoundError, JSONDecodeError, KeyError,
#     ValueError, pygame.error
# =============================================================================

from game import Game


# game run
print("starting game...")
g = Game()
g.run()
print("game closed")

# Andrei Sidorenko - 5750779