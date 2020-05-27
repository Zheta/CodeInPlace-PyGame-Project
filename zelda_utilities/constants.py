# Import standard
import os
import random

# Import other modules
import pygame
from pygame.locals import *

# Set shorthand for vector
vec = pygame.math.Vector2

# Game constants
# All art produced at this screen scale and then *integer scaled* up on run
#  pygame.display.set_mode(, SCALED) flag * in PyGame 2.0!!!
ART_SCALE_X = 320
ART_SCALE_Y = 180
TILE_SIZE = 16

# Game update rate in frames/sec
FRAME_RATE = 60
# Animation frame-rate in frames/sec
ANIMATION_RATE = 12

# Rate at which to spawn beepers
BEEPER_RATE = 300

# Keyboard control constants
P1_KB_UP = pygame.K_e
P1_KB_DOWN = pygame.K_d
P1_KB_LEFT = pygame.K_s
P1_KB_RIGHT = pygame.K_f
P1_KB_BUTTON1 = pygame.K_j
P1_KB_BUTTON2 = pygame.K_k

# Player starting coordinates
# P1_START = ((ART_SCALE_X[0] // 2), (ART_SCALE_X[1] // 2))
P1_START = (10, 4)

# Health values
PLAYER_HEALTH = 20
KAREL_HEALTH = 3

# ~Speed/direction constants~
# Directional speed base
D_SPEED = 1

# Stop vector
D_STOP = (0, 0)

D_UP = (0, D_SPEED * -1)
D_DOWN = (0, D_SPEED)
D_LEFT = (D_SPEED * -1, 0)
D_RIGHT = (D_SPEED, 0)

D_UP_LEFT = (D_SPEED * -1, D_SPEED * -1)
D_UP_RIGHT = (D_SPEED, D_SPEED * -1)
D_DOWN_LEFT = (D_SPEED * -1, D_SPEED)
D_DOWN_RIGHT = (D_SPEED, D_SPEED)

# Testing
P1_SHOW_FPS = K_9
P1_SHOW_BOUNDING_BOXES = K_0

# Colors for testing, quick rectangle making
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DARK_GREY = (64, 64, 64)
GREY = (128, 128, 128)
LIGHT_GREY = (192, 192, 192)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

ORANGE = (255, 128, 0)
LIME = (128, 255, 0)
AQUA = (0, 255, 128)
CERULEAN = (0, 128, 255)
PURPLE = (128, 0, 255)
PINK = (255, 0, 128)

