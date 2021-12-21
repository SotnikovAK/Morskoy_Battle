from handler_for_standard_screen import *
from handler_for_single_player_screen import *
from handler_for_multi_player_screen import *
from Battlefield_Class import *


class DispatcherGame:

    def __init__(self):
        """
        these are the parameters thanks to which the game functions
        """
        self.screen_id = 0
        """
        The screen id is responsible for changing the constant background, together with  game_mode,
         determine what the consequences of pressing any buttons by the player will lead to
        """
        self.coord_of_map = [100, 100]
        """
        these are the coordinates of the upper left corner of the field where the boats are located
        """
        self.player = 0
        """
        The number of the player who is currently making the move. There are two of them: 0 and 1
        """
        self.flag_quit = 0
        """
        this determines whether the program should be turned off. 
        if = 0 no otherwise yes
        """
        self.ship_choice = 0
        """
        is responsible for which ship the player chose when placing their ships
        from 0 to 3
        where 0 is the largest
        3 - the smallest
        
        can also take negative values
        this is necessary in order to program special effects from the buttons
        """
        self.game_mode = 0
        """
        == 0 - single player
        == 1 - multi player
        """
        self.FPS = 100
        """
        FPS of game
        """
        self.old_screen_id = 0
        """
        here is the old screen id that was before the current screen
        """
        self.stage_attack_sam = 1
        """
        this variable defines the type of attack of sam (admiral oscar)
        """
        self.flag_move = False
        """
        determines whether to walk or not, blocks the interaction area when = False
        used in attack
        """
        self.flag_init_ships = True
        """
        == true when the player took the ship when placing the ships
        """
    def handler(self, event_get):
        """
        heart all programs
        this is where the chain of events goes
        """
        for event in event_get:
            if self.flag_quit:
                """
                here the program turns off
                (the built-in button is specially disabled to show 
                that we are able to implement an exit from the program itself)
                """
                return True
            elif self.screen_id == 0 or self.screen_id == 1:
                """
                these ifs determine what screen is now
                """
                """
                here is the menu screen
                """
                self.player = 0
                self.coord_of_map, self.flag_quit, self.screen_id, self.ship_choice, self.game_mode, \
                    self.old_screen_id = handler_for_menu_screen(self.screen_id, self.game_mode, event)

            elif self.screen_id == 2:
                """
                here is the ship placement screen
                """
                self.flag_quit, self.screen_id, self.ship_choice, self.game_mode, self.flag_init_ships, \
                    self.flag_move, self.player, self.coord_of_map, self.old_screen_id = handler_for_selection_ships(
                        self.flag_quit, self.screen_id, self.player, self.game_mode, event, self.ship_choice,
                        self.flag_move, self.flag_init_ships, self.coord_of_map)

            elif self.screen_id == 3:
                """
                here is the return to game screen
                """
                self.flag_quit, self.screen_id, self.ship_choice, self.game_mode = handler_for_return_screen(
                    self.screen_id, self.game_mode, event, self.old_screen_id)

            elif (self.screen_id == 4 or self.screen_id == 5) and self.game_mode:
                """
                player split screens in multiplayer
                """
                self.flag_quit, self.screen_id, self.ship_choice, self.game_mode, self.flag_move =\
                    handler_for_screen_first_or_second_human_player(self.screen_id, self.game_mode, event)
                self.game_mode = 1

            elif self.screen_id == 6 and self.game_mode:
                """
                player attack screen in multiplayer mode
                """
                self.flag_quit, self.screen_id, self.ship_choice, self.game_mode, self.player, self.flag_move, \
                    self.coord_of_map =\
                    handler_for_attack_screen_in_multiplayer(self.flag_quit, self.screen_id, self.ship_choice,
                                                             self.game_mode, self.player, self.flag_move, event,
                                                             self.coord_of_map)
                self.game_mode = 1

            elif self.screen_id == 7 and self.game_mode:
                """
                the effect of the enemy attack is shown here
                """
                self.flag_quit, self.screen_id, self.ship_choice, self.game_mode, self.player, \
                    self.old_screen_id, self.flag_move =\
                    handler_for_defend_screen_in_multiplayer(self.screen_id, self.game_mode, event,
                                                             self.player, self.coord_of_map)
                self.game_mode = 1

            elif self.screen_id == 8:
                """
                victory screen
                """
                self.flag_quit, self.screen_id, self.ship_choice, self.game_mode = \
                    handler_for_final_screen(self.game_mode, self.player, self.screen_id, event, self.old_screen_id)
                self.game_mode = 0

            elif (self.screen_id == 9 or self.screen_id == 10) and not self.game_mode:
                """
                player split screens in single player
                """
                self.screen_id, self.player, self.game_mode, self.ship_choice, self.flag_move = \
                    handler_for_ai_human_screen(self.screen_id, self.player, self.game_mode, event)
                self.game_mode = 0

            elif self.screen_id == 11 and not self.game_mode:
                """
                player attack screen in single player mode
                """
                self.flag_quit, self.screen_id, self.ship_choice, self.game_mode, self.player, self.flag_move, \
                    event, self.coord_of_map =\
                    handler_for_attack_human_screen_in_single_player(self.flag_quit,
                                                                     self.screen_id, self.ship_choice, self.game_mode,
                                                                     self.player, self.flag_move, event,
                                                                     self.coord_of_map)
                self.game_mode = 0

            elif self.screen_id == 12 and not self.game_mode:
                """
                ai attack screen in single player mode
                """
                self.flag_quit, self.screen_id, self.ship_choice, self.game_mode, self.player, \
                    self.flag_move, event, self.coord_of_map, self.stage_attack_sam = \
                    handler_for_attack_ai_in_single_player(self.flag_quit,
                                                           self.screen_id, self.ship_choice, self.game_mode,
                                                           self.player, self.flag_move, event,
                                                           self.coord_of_map, self.stage_attack_sam)
                self.game_mode = 0

            return False

    def update_(self):
        """
        the screen is refreshed here
        """
        clock.tick(self.FPS)
        pygame.display.update()
