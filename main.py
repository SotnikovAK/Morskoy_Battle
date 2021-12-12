import pygame
from controller import *

game = Controller_Game()
game._init_()

static_background(0)

while True:

    finished = game.controller(pygame.event.get())
    if (finished): break

    game.update_()

pygame.quit()
