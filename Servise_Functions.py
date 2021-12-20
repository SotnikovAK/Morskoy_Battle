from init_screen import *
import pygame
from pygame.draw import *
from constans import *

"""
functions are stored here that have no semantic meaning, but are actively used in the game
"""


def battleground(x, y, n):
    """
    draws a box with a grid with delta spacing and top-left x and y coordinates
    """
    for i in range(0, n + n // 10, n // 10):
        line(screen, BLACK, (x + i, y), (x + i, y + n), 5)
        line(screen, BLACK, (x, y + i), (x + n, y + i), 5)


def rot_center(image, angle, x, y):
    """
    rotates the image by some angle in coordinates x,y
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


def text(x, y, word, color, size):
    """
    prints lettering word size in coordinates x,y
    """
    pygame.font.init()
    my_font = pygame.font.SysFont(' ', size)
    text_surface = my_font.render(word, False, color)
    screen.blit(text_surface, (x, y))
