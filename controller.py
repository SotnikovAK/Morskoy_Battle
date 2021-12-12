import pygame
from pygame.draw import *
from random import choice
from _constans import *
from _main_game_parmetres import *
from _buttons_ import *
from init_screen import *
from Servise_Functions import *
from _background import *
from Button_Class import *
from Ship_Button_Class import *
from Operators import *
from Battlefield_Class import *

class Controller_Game():

    def _init_(self):
        self.screen_id = 0
        self.coord_of_map = [100,100]
        self.player = 0
        self.flag_quit = 0
        self.ship_choice = 0
        self.gamemode = 0
    
    def controller(self,event_get):

        for event in event_get:
            print(self.screen_id , self.gamemode)
            if (self.flag_quit) :
                return True
            elif self.screen_id == 0 or self.screen_id == 1:

                add.clear_battlefield(0)
                add.clear_battlefield(1)
                self.coord_of_map = [100, 100]

                self.old_screen_id = self.screen_id
                self.flag_quit, self.screen_id, self.ship_choice, self.gamemode = operator_on_screen(self.screen_id,self.gamemode,event,self.old_screen_id)

            elif self.screen_id == 2:  # SET YOUR SHIPS

                self.old_screen_id = self.screen_id

                static_background(self.screen_id)
                add.draw_battleground(self.player,self.screen_id,self.coord_of_map)

                if (self.ship_choice == 0):
                    self.flag_quit, self.screen_id, self.ship_choice, self.gamemode = operator_on_screen(
                        self.screen_id,self.gamemode,event,self.old_screen_id)
                    self.flag_init_ships = True
                else:
                    if (self.flag_init_ships == True and self.ship_choice > 0 ):
                        self.flag_init_ships = False
                        add._init_ship(self.ship_choice - 1, self.screen_id ,event)

                    elif (self.ship_choice > 0 ):
                        self.ship_choice = add.operator_on_ships_button(
                            self.ship_choice - 1, event, self.player , self.coord_of_map)

                    elif (self.ship_choice == -2):

                        add.clear_battlefield(self.player)
                        self.ship_choice = 0

                    elif (self.ship_choice == -1):

                        add.clear_battlefield(self.player)
                        add.auto_set_ship(self.player)
                        self.ship_choice = 0

                    elif (self.ship_choice == -3):

                        if (add.continue_button(self.player) and self.gamemode == 0):
                            self.screen_id = 4 
                            add.clear_battlefield(1)
                            add.auto_set_ship(1)
                            static_background(self.screen_id)

                            self.coord_of_map = [250,150]

                        elif (add.continue_button(self.player) and self.gamemode == 1 and self.player == 0):

                            self.player += 1
                            add.clear_battlefield(self.player)

                        elif (add.continue_button(self.player) and self.gamemode == 1 and self.player == 1):

                            self.screen_id = 4
                            self.flag_move = True
                            self.coord_of_map = [250,150]
                            self.player = 1
                            static_background(self.screen_id)

                        self.ship_choice = 0

            elif (self.screen_id == 3):

                self.flag_quit, self.screen_id, self.ship_choice, self.gamemode = operator_on_screen(self.screen_id, self.gamemode,event,self.old_screen_id)

            if (self.gamemode == 1):
                if (self.screen_id == 4 or self.screen_id == 5): # Here should be myasso
                    
                    self.old_screen_id = self.screen_id
                    self.flag_quit, self.screen_id, self.ship_choice, self.gamemode = operator_on_screen(self.screen_id,self.gamemode,event,self.old_screen_id)
                    
                    self.flag_move = True

                elif (self.screen_id == 7): # defend ship!

                    self.old_screen_id = self.screen_id
                    add.dehiding_ships(self.player)
                    add.draw_battleground(self.player,self.screen_id,self.coord_of_map)
                    self.flag_move = True

                    self.flag_quit, self.screen_id, self.ship_choice, self.gamemode = operator_on_screen(self.screen_id, self.gamemode,event,self.old_screen_id)

                    if (self.ship_choice == 1):
                        self.player = 1 - self.player
                
                elif (self.screen_id == 6): #ATTACK SHIP!!!
                    
                    self.old_screen_id = self.screen_id
                    add.hiding_ships(self.player)
                    add.draw_battleground(self.player,self.screen_id,self.coord_of_map)
                    if (self.flag_move):
                        self.flag_hit = add.attack_on_ships(event,self.player,self.coord_of_map)

                    if (self.flag_hit == 0):
                        self.flag_move = False

                    elif (self.flag_hit == 2):
                        self.screen_id = 8
                        static_background(self.screen_id)
                        
                    if (self.flag_hit != 2):
                        self.flag_quit, self.screen_id, self.ship_choice, self.gamemode = operator_on_buttons(len(button_pushed_image[self.screen_id]), self.screen_id, event, self.old_screen_id)
                    
                    if (self.screen_id == 3):
                        static_background(self.screen_id)

                    if (self.screen_id != 6 and self.screen_id != 3 and self.flag_hit != 2):
                        self.screen_id -= self.player
                        static_background(self.screen_id)

                elif (self.screen_id == 8): #FINAL SCREEN!
                    text(435,275,"number  " + str(self.player + 1),BLACK, 48)
                    self.flag_quit, self.screen_id, self.ship_choice, self.gamemode = operator_on_screen(self.screen_id, self.gamemode,event,self.old_screen_id)
                    add.hiding_ships(self.player)

                self.gamemode = 1
            else:



                self.gamemode = 0
            return False

    def update_(self):
        clock.tick(FPS)
        pygame.display.update()
