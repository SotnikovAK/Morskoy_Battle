from Battlefield_Class import *
from Button_Class import *


def handler_for_menu_screen(screen_id, game_mode, event):
    add.clear_battlefield(0)
    add.clear_battlefield(1)
    add.hiding_ships(0)
    add.hiding_ships(1)
    coord_of_map = [100, 100]
    old_screen_id = screen_id

    flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(
        screen_id, game_mode, event, old_screen_id)

    return coord_of_map, flag_quit, screen_id, ship_choice, game_mode, old_screen_id


def handler_for_selection_ships(screen_id, player, game_mode, event, ship_choice, flag_move, flag_init_ships,
                                coord_of_map):
    old_screen_id = screen_id

    static_background(screen_id)
    add.draw_battleground(player, screen_id, coord_of_map)
    flag_quit = False

    if ship_choice == 0:
        flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(
            screen_id, game_mode, event, old_screen_id)
        flag_init_ships = True
    else:
        if flag_init_ships and ship_choice > 0:
            flag_init_ships = False
            add.create_ship(ship_choice - 1, screen_id, event)

        elif ship_choice > 0:
            ship_choice = add.manual_placement(
                ship_choice - 1, event, player, coord_of_map)

        elif ship_choice == -2:

            add.clear_battlefield(player)
            ship_choice = 0

        elif ship_choice == -1:

            add.clear_battlefield(player)
            add.auto_set_ship(player)
            ship_choice = 0

        elif ship_choice == -3:

            if add.continue_button(player) and game_mode == 0:
                player = 0
                screen_id = 9 + player
                add.clear_battlefield(1)
                add.auto_set_ship(1)
                static_background(screen_id)

                coord_of_map = [250, 150]

            elif add.continue_button(player) and game_mode == 1 and player == 0:

                player += 1
                add.clear_battlefield(player)

            elif add.continue_button(player) and game_mode == 1 and player == 1:

                screen_id = 4
                flag_move = True
                coord_of_map = [250, 150]
                player = 1
                static_background(screen_id)

            ship_choice = 0

    return flag_quit, screen_id, ship_choice, game_mode, flag_init_ships, flag_move, player, coord_of_map, old_screen_id


def handler_for_return_screen(screen_id, game_mode, event, old_screen_id):
    flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id, game_mode, event,
                                                                                   old_screen_id)
    return flag_quit, screen_id, ship_choice, game_mode


def handler_for_final_screen(game_mode, player, screen_id, event, old_screen_id):
    if game_mode:
        text(435, 275, "number  " + str(player + 1), BLACK, 48)
        flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id, game_mode,
                                                                                       event, old_screen_id)
        return flag_quit, screen_id, ship_choice, game_mode
