from Battlefield_Class import *
from Button_Class import *


def handler_for_ai_human_screen(screen_id, player, game_mode, event):
    old_screen_id = screen_id
    flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id, game_mode, event,
                                                                                   old_screen_id)
    if screen_id == 9 and player < 1:
        player += 1
    elif screen_id == 10 and player > 0:
        player -= 1
    return screen_id, player, game_mode, ship_choice, True


def handler_for_attack_human_screen_in_single_player(flag_quit, screen_id, ship_choice, game_mode, player, flag_move,
                                                     event, coord_of_map):
    old_screen_id = screen_id
    add.hiding_ships(player)
    add.draw_battleground(player, screen_id, coord_of_map)
    flag_hit = 3
    if flag_move:
        if human_player_attack_exam(event, coord_of_map):
            a, b = (event.pos[0] - coord_of_map[0]) // delta + 1, (event.pos[1] - coord_of_map[1]) // delta + 1
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

    return flag_quit, screen_id, ship_choice, game_mode, player, flag_move, event, coord_of_map


def handler_for_attack_ai_in_single_player(flag_quit, screen_id, ship_choice, game_mode, player, flag_move, event,
                                           coord_of_map, stage_attack_sam):
    flag_hit = 0
    old_screen_id = screen_id
    add.de_hiding_ships(player)
    add.draw_battleground(player, screen_id, coord_of_map)

    if stage_attack_sam == 1:
        if flag_move:
            x, y = AI.first_type_of_attack()
            flag_hit = add.attack_on_ships(x, y, player, 'Sam')

        if flag_hit == 0:
            flag_move = False

        if flag_hit == 1:
            print(stage_attack_sam)

            if not AI.question_about_destroyed_ship():
                AI.diagonal_death_zone()
                stage_attack_sam = 2
                print('*')

    if stage_attack_sam == 2:
        if flag_move:
            x, y = AI.second_type_of_attack()
            flag_hit = add.attack_on_ships(x, y, player, 'Sam')

        if flag_hit == 0:
            flag_move = False

        if flag_hit == 1:

            if not AI.question_about_destroyed_ship():
                AI.angle_determinant()
                AI.diagonal_death_zone()
                print('/')
                stage_attack_sam = 3
            else:
                stage_attack_sam = 1
    if stage_attack_sam == 3:
        if flag_move:
            x, y = AI.third_type_of_attack()
            flag_hit = add.attack_on_ships(x, y, player, 'Sam')

        if flag_hit == 0:
            flag_move = False

        if flag_hit == 1:

            if AI.question_about_destroyed_ship():
                print('*+*+*+*++**++**++*')
                stage_attack_sam = 1

    if flag_hit == 2:
        screen_id = 8
        static_background(screen_id)

    if flag_hit != 2:
        flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id, game_mode, event,
                                                                                       old_screen_id)

    if screen_id == 3:
        static_background(screen_id)

    return flag_quit, screen_id, ship_choice, game_mode, player, flag_move, event, coord_of_map, stage_attack_sam
