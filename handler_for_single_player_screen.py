from Battlefield_Class import *
from Button_Class import *


def handler_for_ai_human_screen(screen_id, player, game_mode, event):
    """
    splash screen for AI and player moves
    """
    old_screen_id = screen_id
    flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id, game_mode, event,
                                                                                   old_screen_id)
    """
    Players change here
    """
    if screen_id == 9 and player < 1:
        player += 1
    elif screen_id == 10 and player > 0:
        player -= 1
    return screen_id, player, game_mode, ship_choice, True


def handler_for_attack_human_screen_in_single_player(flag_quit, screen_id, ship_choice, game_mode, player, flag_move,
                                                     event, coord_of_map):
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
            a, b = (event.pos[0] - coord_of_map[0]) // delta + 1, (event.pos[1] - coord_of_map[1]) // delta + 1
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

    return flag_quit, screen_id, ship_choice, game_mode, player, flag_move, event, coord_of_map


def handler_for_attack_ai_in_single_player(flag_quit, screen_id, ship_choice, game_mode, player, flag_move, event,
                                           coord_of_map, stage_attack_sam):
    """
    this is where sam's attack takes place
    """
    flag_hit = 0
    old_screen_id = screen_id
    """
    his ships must be hidden
    """
    add.de_hiding_ships(player)
    add.draw_battleground(player, screen_id, coord_of_map)
    """
    this is the mechanism of his attack
    """
    """
    see the normal player attack documentation and the documentation in the ai file
    """
    if stage_attack_sam == 1:
        if flag_move:
            """
            if oscar can walk, then the player has the right to attack
            """
            x, y = AI.first_type_of_attack()
            flag_hit = add.attack_on_ships(x, y, player, 'Sam')

        if flag_hit == 0:
            """
            player did not hit the ship, so blocked from further attack
            """
            flag_move = False

        if flag_hit == 1:
            """
            there is a break
            """

            print(stage_attack_sam)

            if not AI.question_about_destroyed_ship():
                AI.diagonal_death_zone()
                stage_attack_sam = 2
                print('*')

    if stage_attack_sam == 2:
        if flag_move:
            """
            if oscar can walk, then the player has the right to attack
            """
            x, y = AI.second_type_of_attack()
            flag_hit = add.attack_on_ships(x, y, player, 'Sam')

        if flag_hit == 0:
            flag_move = False

        if flag_hit == 1:
            """
            there is a break
            """
            if not AI.question_about_destroyed_ship():
                AI.angle_determinant()
                AI.diagonal_death_zone()
                print('/')
                stage_attack_sam = 3
            else:
                stage_attack_sam = 1
    if stage_attack_sam == 3:
        if flag_move:
            """
            if oscar can walk, then the player has the right to attack
            """
            x, y = AI.third_type_of_attack()
            flag_hit = add.attack_on_ships(x, y, player, 'Sam')

        if flag_hit == 0:
            """
            player did not hit the ship, so blocked from further attack
            """
            flag_move = False

        if flag_hit == 1:
            """
            there is a break
            """
            if AI.question_about_destroyed_ship():
                print('*+*+*+*++**++**++*')
                stage_attack_sam = 1

    if flag_hit == 2:
        """
        access to handling standard buttons
        """
        screen_id = 8
        static_background(screen_id)

    if flag_hit != 2:
        """
        access to handling standard buttons
        """
        flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id, game_mode, event,
                                                                                       old_screen_id)

    if screen_id == 3:
        """
        screen update for return screen
        """
        static_background(screen_id)

    return flag_quit, screen_id, ship_choice, game_mode, player, flag_move, event, coord_of_map, stage_attack_sam
