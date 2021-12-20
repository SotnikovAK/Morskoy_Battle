from Battlefield_Class import *
from Button_Class import *

"""
processes the initial screen (menu)
"""


def handler_for_menu_screen(screen_id, game_mode, event):
    """
    to start a new game, game need to reset the settings for the battle
    clear - clears the field from all objects
    hiding_ships - hides the new arrangement from prying eyes
    """
    for n in range(2):
        add.clear_battlefield(n)
        add.hiding_ships(n)
    """
    This is where the coordinates of the upper left margin of the field are set.
    """
    coord_of_map = [100, 100]

    old_screen_id = screen_id
    """
    with the next command, the game checks all the buttons on the field, checks if they are pressed
    """
    flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(
        screen_id, game_mode, event, old_screen_id)
    """
    returns what was or could have been changed at this stage
    """
    return coord_of_map, flag_quit, screen_id, ship_choice, game_mode, old_screen_id


def handler_for_selection_ships(flag_quit, screen_id, player, game_mode, event, ship_choice, flag_move, flag_init_ships,
                                coord_of_map):
    """
    here the ship placement screen is handled
    """
    old_screen_id = screen_id
    """
    since the ships are drawn behind the cursor, 
    subject to their choice, it is necessary to select the consequences of this creativity
    
    so every tick the background is updated
    """

    static_background(screen_id)

    """
    with the next command we draw a field and ships on it
    """

    add.draw_battleground(player, screen_id, coord_of_map)

    """
    here the ship_choice is fully exploited
    
    == 0 - no ship selected for deployment
    == 1 - destroyer selected for manual placement
    == 2 - cruiser selected for manual placement
    == 3 - aircraft carrier selected for manual placement
    == 4 - battleship selected for manual placement
    
    buttons with special properties are programmed for its negative values, 
    and not just switching the screen, for example, the clear button - clears the screen of all ships

    == -1 - the auto placement button is programmed to this value
    == -2 - the field clear button is programmed for this value
    == -3 -  the continue button is programmed as to activate it, you need to arrange all the ships
    """
    if ship_choice == 0:
        """
        handling standard buttons that switch the screen
            * exit button
            * ship buttons
        the latter call the same screen, but with ship_choice! = 0
        """

        flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(
            screen_id, game_mode, event, old_screen_id)
        """
        flag_init_ships variable means that the player has the right to take the ship
        """
        flag_init_ships = True
    else:
        if flag_init_ships and ship_choice > 0:
            """
            ship selected
            the corresponding class is activated
            """
            add.create_ship(ship_choice - 1, screen_id, event)
            """
            flag_init_ships is reset so the player cannot created another
            """
            flag_init_ships = False

        elif ship_choice > 0:
            """
            interaction with these selected ships takes place here
            """
            ship_choice = add.manual_placement(
                ship_choice - 1, event, player, coord_of_map)

        elif ship_choice == -2:
            """
            here the button to clear the screen is activated
            """
            """
            clearing the current player's field
            """
            add.clear_battlefield(player)
            """
            transition to the level of interaction with standard buttons
            """
            ship_choice = 0

        elif ship_choice == -1:
            """
            here the button for auto placement of ships is activated
            """
            """
            the player's field is initially cleared
            and then filled
            """
            add.clear_battlefield(player)
            add.auto_set_ship(player)
            """
            transition to the level of interaction with standard buttons
            """
            ship_choice = 0

        elif ship_choice == -3:
            """
            here the continue button is activated
            """
            if add.continue_button(player) and game_mode == 0:
                """
                if it's a single player...
                """
                player = 0
                screen_id = 9
                """
                create a sam field by auto generation
                """
                add.clear_battlefield(1)
                add.auto_set_ship(1)
                """
                update the screen
                """
                static_background(screen_id)
                coord_of_map = [250, 150]

            elif add.continue_button(player) and game_mode == 1 and player == 0:

                """
                if it's a multi player...
                """
                """
                we give the opportunity to place ships for the next player
                """
                player += 1
                add.clear_battlefield(player)

            elif add.continue_button(player) and game_mode == 1 and player == 1:

                """
                ... and at the end we update the screen
                """
                screen_id = 4
                flag_move = True
                coord_of_map = [250, 150]
                player = 1
                static_background(screen_id)
            """
            transition to the level of interaction with standard buttons
            """
            ship_choice = 0

    return flag_quit, screen_id, ship_choice, game_mode, flag_init_ships, flag_move, player, coord_of_map, old_screen_id


def handler_for_return_screen(screen_id, game_mode, event, old_screen_id):
    """
    this is the return to game screen
    """
    """
    with the next command, the game checks all the buttons on the field, checks if they are pressed
    """
    flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id, game_mode, event,
                                                                                   old_screen_id)
    return flag_quit, screen_id, ship_choice, game_mode


def handler_for_final_screen(game_mode, player, screen_id, event, old_screen_id):
    """
    this is the game ending screen
    """
    """
    with the next command, the game checks all the buttons on the field, checks if they are pressed
    """
    if game_mode:
        text(435, 275, "number  " + str(player + 1), BLACK, 48)
        flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id, game_mode,
                                                                                       event, old_screen_id)
        return flag_quit, screen_id, ship_choice, game_mode

    else:
        if not player:
            name_winner = 'Admiral_Oscar'
        else:
            name_winner = 'Player'
        text(435, 275, name_winner, BLACK, 48)
        flag_quit, screen_id, ship_choice, game_mode = dispatcher_on_buttons_in_screen(screen_id, game_mode,
                                                                                       event, old_screen_id)
        return flag_quit, screen_id, ship_choice, game_mode

