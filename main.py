import pygame as pg
import dispatcher as disp
import draw_background as bg

game = disp.DispatcherGame()
game.__init__()
finished = False
"""
The main game parameters are created in the _init_
"""
bg.static_background(0)

"""
Start game screen
"""

while not finished:
    """
    Events are handled here
    """
    finished = game.handler(pg.event.get())
    """
    This is the way out of the game
    """
    game.update_()
    """
    screen refresh
    """

pg.quit()
