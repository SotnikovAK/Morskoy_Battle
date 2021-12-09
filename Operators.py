import pygame
from pygame.draw import *
from Button_Class import *
from _background import *


b_n = Button()

def operator_on_buttons(number, screen_id, event):
    a, b, c = 0, screen_id, 0
    gamemode = -1
    for i in range(number):
        b_n._init(i,screen_id)
        
        if event.type == pygame.MOUSEMOTION:
            if (b_n.pressure_test(event)):
                b_n.pushed_button_draw()
            else:
                b_n.unpushed_button_draw()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (b_n.pressure_test(event)):
                a, b, c = post_pressing_effect[screen_id][i]
                gamemode = Gamemode[screen_id][i] 
                if (b == -10):
                    b = screen_id

    return a, b, c, gamemode 

def operator_on_screen(screen_id,gamemode, event):
    old_screen_id = screen_id
    new_gamemode = 0

    flag_quit, screen_id, ship_choice, new_gamemode = operator_on_buttons(
        len(button_pushed_image[screen_id]), screen_id, event)

    if (new_gamemode != -1):
        gamemode = new_gamemode

    if screen_id != old_screen_id:
        static_background(screen_id)
    return flag_quit, screen_id, ship_choice, gamemode