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
    see the normal player attack documentation and the documentation in the ai file and player attack
    everything will be visible there
    general documentation for ai sam:
    
    * if we destroy the ship, we return to the first stage of shooting at random (stage_attack_sam = 1)
    * depending on the length of the ship, we change the stage of the attack
    
    so destroyers are destroyed at stage 1
    so cruisers are destroyed in stage 2
    so aircraft carriers are destroyed in stage 3
    to destroy battleships you need stages 4,5,6
    
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

            if not AI.question_about_destroyed_ship():
                AI.diagonal_death_zone()
                stage_attack_sam = 2

    if stage_attack_sam == 2:
        if flag_move:
            """
            if oscar can walk, then the player has the right to attack
            """
            x, y = AI.second_type_of_attack()
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
            AI.diagonal_death_zone()
            if not AI.question_about_destroyed_ship():
                AI.angle_determinant()
                stage_attack_sam = 3
            else:
                stage_attack_sam = 1

    if stage_attack_sam == 3:
        if flag_move:
            """
            if oscar can walk, then the player has the right to attack
            """
            x, y = AI.third_type_of_attack()
            if x != -1 and y != -1:
                flag_hit = add.attack_on_ships(x, y, player, 'Sam')
                if flag_hit == 0:
                    """
                    player did not hit the ship, so blocked from further attack
                    """
                    stage_attack_sam = 4
                    flag_move = False

                elif flag_hit == 1:
                    AI.angle_determinant()
                    fl = AI.question_about_destroyed_ship()
                    if not fl:

                        stage_attack_sam = 5

                    else:
                        stage_attack_sam = 1
            else:
                stage_attack_sam = 4

    if stage_attack_sam == 4:
        if flag_move:
            """
            if oscar can walk, then the player has the right to attack
            """
            x, y = AI.fourth_type_of_attack()
            if x != -1 and y != -1:
                flag_hit = add.attack_on_ships(x, y, player, 'Sam')
                if flag_hit == 1:
                    if not AI.question_about_destroyed_ship():

                        stage_attack_sam = 6

                    else:
                        stage_attack_sam = 1

    if stage_attack_sam == 5:

        if flag_move:
            x, y = AI.fifth_type_of_attack()
            if x != -1 and y != -1:
                flag_hit = add.attack_on_ships(x, y, player, 'Sam')
            else:
                stage_attack_sam = 1
        if flag_hit == 0:
            flag_move = False

        elif flag_hit == 1:
            AI.question_about_destroyed_ship()
            stage_attack_sam = 1

    if stage_attack_sam == 6:
        if flag_move:
            x, y = AI.six_type_attack()
            flag_hit = add.attack_on_ships(x, y, player, 'Sam')
        if flag_hit == 1:
            stage_attack_sam = 1

    if flag_hit == 2:
        """
        victory screen
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
