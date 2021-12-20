from Battlefield_Class import *
from Button_Class import *


def handler_for_screen_first_or_second_human_player(screen_id, game_mode, event):
    old_screen_id = screen_id
    flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id, game_mode,
                                                                                   event, old_screen_id)
    return flag_quit, screen_id, ship_choice, game_mode, True


def handler_for_attack_screen_in_multiplayer(flag_quit, screen_id, ship_choice, game_mode, player, flag_move, event,
                                             coord_of_map):
    old_screen_id = screen_id
    add.hiding_ships(player)
    add.draw_battleground(player, screen_id, coord_of_map)
    flag_hit = 3
    if flag_move:
        if human_player_attack_exam(event, coord_of_map):
            a, b = (event.pos[0] - coord_of_map[0]) // delta + \
                   1, (event.pos[1] - coord_of_map[1]) // delta + 1
            flag_hit = add.attack_on_ships(a, b, player, 'human')
        else:
            flag_hit = 3

    if flag_hit == 0:
        flag_move = False

    elif flag_hit == 2:
        screen_id = 8
        static_background(screen_id)

    if flag_hit != 2:
        flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id,
                                                                                       game_mode, event, old_screen_id)

    if screen_id == 3:
        static_background(screen_id)

    if screen_id != 6 and screen_id != 3 and flag_hit != 2:
        screen_id -= player
        static_background(screen_id)
    return flag_quit, screen_id, ship_choice, game_mode, player, flag_move, coord_of_map


def handler_for_defend_screen_in_multiplayer(screen_id, game_mode, event, player, coord_of_map):
    old_screen_id = screen_id
    add.de_hiding_ships(player)
    add.draw_battleground(player, screen_id, coord_of_map)

    flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id, game_mode,
                                                                                   event, old_screen_id)

    if ship_choice == 1:
        player = 1 - player

    return flag_quit, screen_id, ship_choice, game_mode, player, old_screen_id, True
