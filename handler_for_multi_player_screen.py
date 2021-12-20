from Battlefield_Class import *
from Button_Class import *


def handler_for_screen_first_or_second_human_player(screen_id, game_mode, event):
    """
        splash screen for AI and player moves
    """
    old_screen_id = screen_id
    flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id, game_mode,
                                                                                   event, old_screen_id)
    return flag_quit, screen_id, ship_choice, game_mode, True


def handler_for_attack_screen_in_multiplayer(flag_quit, screen_id, ship_choice, game_mode, player, flag_move, event,
                                             coord_of_map):
    """
    here is the player's attack
    """

    old_screen_id = screen_id
    """
    a field is drawn here
    """
    add.hiding_ships(player)
    add.draw_battleground(player, screen_id, coord_of_map)
    flag_hit = 3
    """
       flag_hit runs everything here
        * == 3 - do nothing
        * == 2 - all ships destroyed
        * == 1 - hitting the ship
        * == 0 - getting into milk
       """

    if flag_move:
        """
        if you can walk, then the player has the right to attack
        """
        if human_player_attack_exam(event, coord_of_map):
            a, b = (event.pos[0] - coord_of_map[0]) // delta + \
                   1, (event.pos[1] - coord_of_map[1]) // delta + 1
            flag_hit = add.attack_on_ships(a, b, player, 'human')
        else:
            flag_hit = 3

    if flag_hit == 0:
        """
        player did not hit the ship, so blocked from further attack
        """
        flag_move = False

    elif flag_hit == 2:
        """
        ships destroyed - victory screen
        """
        screen_id = 8
        static_background(screen_id)

    if flag_hit != 2:
        """
        access to handling standard buttons
        """
        flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id,
                                                                                       game_mode, event, old_screen_id)

    if screen_id == 3:
        """
        screen update for return screen
        """
        static_background(screen_id)

    if screen_id != 6 and screen_id != 3 and flag_hit != 2:
        """
        screen update for next player screen
        """
        screen_id -= player
        static_background(screen_id)
    return flag_quit, screen_id, ship_choice, game_mode, player, flag_move, coord_of_map


def handler_for_defend_screen_in_multiplayer(screen_id, game_mode, event, player, coord_of_map):

    """
    here is the player's attack
    """

    old_screen_id = screen_id
    """
    a field is drawn here
    """
    add.de_hiding_ships(player)
    add.draw_battleground(player, screen_id, coord_of_map)

    flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id, game_mode,
                                                                                   event, old_screen_id)
    """
    Players change here
    """
    if ship_choice == 1:
        player = 1 - player

    return flag_quit, screen_id, ship_choice, game_mode, player, old_screen_id, True
