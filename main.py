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

pygame.init()

FPS = 100

BLACK = (0, 0, 0)

class Battlefield():

    def _init_battlefield(self):

        self.battlefield = [
            [[0] * 12 for i in range(12)], [[0] * 12 for i in range(12)]]
        self.coordinates , self.flag_angle = [[] * 2 for i in range(2)], [[] * 2 for i in range(2)]
        self.id, self.angle = [[] * 2 for i in range(2)], [[] * 2 for i in range(2)]
        self.flag = [0,0]
        self.catalog = [[1, 2, 3, 4], [1 , 2, 3, 4]]
        self.affected_cells_of_seas = [[],[]]
        self.affected_cells_of_ships = [[],[]]
        self.lives = [[],[]]

    def clear_battlefield(self, n):

        self.battlefield[n] = [[0] * 12 for i in range(12)]
        self.coordinates[n] , self.flag_angle[n] = [], []
        self.id[n], self.angle[n] = [], []
        self.lives[n] = []
        self.flag[n] = 0
        self.catalog[n] = [1, 2, 3, 4]

    def _init_ship(self, _ship):
        self.ship = Ship_Buttons()
        self.ship._init(event, _ship, screen_id)

    def operator_on_ships_button(self, _ship, event, N):
        _ship_ = _ship + 1
        if (self.catalog[N][_ship] > 0):
            if event.type == pygame.MOUSEMOTION:
                self.ship._draw(event)

            elif (event.type == pygame.MOUSEBUTTONDOWN):

                if (event.button == 3):
                    self.ship.rotation(event)

                elif (event.button == 2):
                    _ship_ = 0

                elif (event.button == 1):
                    self.catalog[N][_ship] -= 1
                    x, y, angle_flag, d, angle = self.ship.examination_of_button(
                        event, _ship)
                    if (angle_flag != -1):

                        flag = True
                        for i in range(size_ship[_ship] + 1):
                            if ((angle_flag == 0 and self.battlefield[N][y][x+i] != 0) or (angle_flag == 1 and self.battlefield[N][y+i][x] != 0)):
                                flag = False
                                break

                        if (flag):
                            for i in range(len(Ships[_ship])):
                                if ((angle_flag == 0 and self.battlefield[N][y + Ships[_ship][i][1]][x + Ships[_ship][i][0]] > 1) or (angle_flag == 1 and self.battlefield[N][y + Ships[_ship][i][0]][x + Ships[_ship][i][1]] > 1)):
                                    flag = False
                                    break

                        if (flag):

                            for i in range(size_ship[_ship] + 1):
                                if (angle_flag == 0):
                                    self.battlefield[N][y][x +
                                                           i] = size_ship[_ship] + 2
                                else:
                                    self.battlefield[N][y +
                                                        i][x] = size_ship[_ship] + 2

                            for i in range(len(Ships[_ship])):
                                if (angle_flag == 0):
                                    self.battlefield[N][y + Ships[_ship]
                                                        [i][1]][x + Ships[_ship][i][0]] = 1
                                else:
                                    self.battlefield[N][y + Ships[_ship]
                                                        [i][0]][x + Ships[_ship][i][1]] = 1

                            self.coordinates[N].append([y, x])
                            self.flag_angle[N].append(angle_flag)
                            self.id[N].append(d)
                            self.lives[N].append(size_ship[d] + 1)
                            self.angle[N].append(angle)
                            self.flag[N] = 1
                        else:
                            self.catalog[N][_ship] += 1
                    else:
                        self.catalog[N][_ship] += 1
                self.ship._draw(event)
        else:
            _ship_ = 0
        return _ship_

    def auto_set_ship(self, N):

        for n in self.catalog[N]:
            for m in range(n):
                flag_angle = choice([0, 1])
                A = []
                m, k = 11, 11 - size_ship[n-1]

                if (flag_angle == 1):
                    m, k = k, m

                for i in range(1, m):
                    for j in range(1, k):
                        if ((flag_angle == 0 and self.battlefield[N][i][j] == 0 and self.battlefield[N][i][j + size_ship[n-1]] == 0) or (flag_angle == 1 and self.battlefield[N][i][j] == 0 and self.battlefield[N][i + size_ship[n-1]][j] == 0)):
                            A.append((i, j))

                coord = choice(A)

                self.coordinates[N].append(coord)
                self.flag_angle[N].append(flag_angle)
                self.id[N].append(n-1)
                self.lives[N].append(size_ship[n-1] + 1)
                self.angle[N].append(180*choice([0, 1]))

                for i in range(0, size_ship[n-1] + 1):
                    if (flag_angle == 0):
                        self.battlefield[N][coord[0]
                                            ][coord[1] + i] = size_ship[n-1] + 2
                    else:
                        self.battlefield[N][coord[0] +
                                            i][coord[1]] = size_ship[n-1] + 2

                B = Ships[n-1]

                for i in range(len(B)):
                    if (flag_angle == 0):
                        self.battlefield[N][int(
                            coord[0] + B[i][1])][int(coord[1] + B[i][0])] = 1
                    else:
                        self.battlefield[N][int(
                            coord[0] + B[i][0])][int(coord[1] + B[i][1])] = 1

        self.flag[N] = 1
        self.catalog[N] = [0, 0, 0, 0]

    def draw_battleground(self,N):

        if (screen_id == 2):
            for i in range(0, 400, 100):
                text(950, 170 + i, str(self.catalog[N][i//100]), BLACK, 64)

        if (len(self.affected_cells_of_seas[N]) > 0):

            for i in range(len(self.affected_cells_of_seas[N])):
                _x = pygame.image.load(attack_image[0])
                center_ship = ((self.affected_cells_of_seas[N][i][1] - 1) * delta + y0 + delta//2 + 2 * delta  ,(self.affected_cells_of_seas[N][i][0] - 1)* delta + x0 + delta//2 -2 * delta)
                x_rect = _x.get_rect(center = center_ship)
                screen.blit(_x, x_rect)
        battleground(x0, y0, 10 * delta)
        if (self.flag[N] == 1):
            for i in range(len(self.id[N])):
                _x = pygame.image.load(ships_images[self.id[N][i]])
                x, y = self.coordinates[N][i][1] - 1, self.coordinates[N][i][0] - 1
                half_size_ship = (size_ship[self.id[N][i]] + 1) * delta / 2
                if (self.flag_angle[N][i] == 0):
                    center_ship = (x * delta + x0 + half_size_ship,
                                   y * delta + delta / 2 + y0)
                    _x, x_rect = rot_center(
                        _x, self.angle[N][i], center_ship[0], center_ship[1])

                else:
                    center_ship = (x * delta + x0 + delta / 2,
                                   y * delta + half_size_ship + y0)
                    _x, x_rect = rot_center(
                        _x, 90 + self.angle[N][i], center_ship[0], center_ship[1])

                x_rect = _x.get_rect(center=center_ship)
                screen.blit(_x, x_rect)

        if (len(self.affected_cells_of_ships[N]) > 0):
            for i in range(len(self.affected_cells_of_ships[N])):
                _x = pygame.image.load(attack_image[1])
                center_ship = ((self.affected_cells_of_ships[N][i][1] - 1) * delta + y0 + delta//2 + 2 * delta  ,(self.affected_cells_of_ships[N][i][0] - 1)* delta + x0 + delta//2 -2 * delta)
                x_rect = _x.get_rect(center = center_ship)
                screen.blit(_x, x_rect)

    def hiding_ships(self,N):
        self.flag[N] = 0

    def dehiding_ships(self,N):
        self.flag[N] = 1

    def attack_on_ships(self,event,N):

        if (event.type == pygame.MOUSEBUTTONDOWN ):

            if ( x0 <= event.pos[0] and event.pos[0] <= x0 + 10 * delta and y0 <= event.pos[1] and event.pos[1] <= y0 + 10 * delta ):
                a,b = (event.pos[0] - x0) // delta + 1, (event.pos[1]-y0) // delta + 1

                if (self.battlefield[N][b][a] > 1):
                    if (self.affected_cells_of_ships[N].count((b,a)) == 0):
                        A = []
                        for i in range(len(self.id[N])):
                            X,Y = self.coordinates[N][i][1],self.coordinates[N][i][0]

                            if (self.battlefield[N][b][a] == self.battlefield[N][Y][X]):
                                A.append(i)
                        
                        size_ = self.battlefield[N][b][a] - 1

                        for i in A:

                            flag = False
                            for j in range(size_):

                                if (a == self.coordinates[N][i][1] + j and b == self.coordinates[N][i][0] and self.flag_angle[N][i] == 0) or (a == self.coordinates[N][i][1] and b == self.coordinates[N][i][0] + j and self.flag_angle[N][i] == 1):
                                    flag = True
                                    self.affected_cells_of_ships[N].append((b,a))
                                    self.lives[N][i] -= 1
                                    break

                            if (flag):
                                break

                        for i in range(len(self.id[N])):
                            if (self.lives[N][i] == 0):
                                for j in range(len(Ships[self.id[N][i]])):

                                    if (self.flag_angle[N][i] == 0):
                                        x,y = self.coordinates[N][i][0] + Ships[self.id[N][i]][j][1],self.coordinates[N][i][1] + Ships[self.id[N][i]][j][0]
                                    else:
                                        x,y = self.coordinates[N][i][0] + Ships[self.id[N][i]][j][0],self.coordinates[N][i][1] + Ships[self.id[N][i]][j][1]

                                    if (0 < x and x < 11 and 0 < y  and y < 11):
                                        self.affected_cells_of_seas[N].append((x,y))

                        flag = 0
                        for i in range(len(self.id[N])):
                            if (self.lives[N][i] < 1):
                                flag += 1

                        if (flag == len(self.id[N])):
                            return 2

                        return 1         
                    else:
                        return 0
                else:
                    self.affected_cells_of_seas[N].append((b,a))
                    return 0
        return 3

    def continue_button(self,N):
        return (int(self.catalog[N] == [0, 0, 0, 0]))
    
    def print_battlefield(self): #these function for only view
        print('First Field')
        for row in self.battlefield[0]:
            print(' '.join([str(elem) for elem in row]))
        print('Second Field')
        for row in self.battlefield[1]:
            print(' '.join([str(elem) for elem in row]))
        print(self.id[0], self.id[1])
        print(self.lives[0],self.lives[1])


pygame.display.update()
clock = pygame.time.Clock()
finished = False

add = Battlefield()

gamemode = 0
player = 0
flag_hit = True

static_background(screen_id)

while not finished:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or flag_quit == 1:
            finished = True

        elif screen_id != 2 and screen_id != 4 and screen_id != 5 and screen_id != 7 and screen_id != 6 and screen_id != 8:

            if (screen_id != 3):
                add._init_battlefield()

            flag_quit, screen_id, ship_choice, gamemode = operator_on_screen(screen_id,gamemode,event)
            flag_fill = False

        elif screen_id == 2:  # SET YOUR SHIPS

            static_background(screen_id)
            add.draw_battleground(player)

            if (ship_choice == 0):
                flag_quit, screen_id, ship_choice, gamemode = operator_on_screen(
                    screen_id,gamemode,event)
                flag_init_ships = True
            else:
                if (flag_init_ships == True and ship_choice > 0 ):
                    flag_init_ships = False
                    add._init_ship(ship_choice - 1)

                elif (ship_choice > 0 ):
                    ship_choice = add.operator_on_ships_button(
                        ship_choice - 1, event, player)

                elif (ship_choice == -2):

                    add.clear_battlefield(player)
                    ship_choice = 0

                elif (ship_choice == -1):

                    add.clear_battlefield(player)
                    add.auto_set_ship(player)
                    ship_choice = 0

                elif (ship_choice == -3):

                    if (add.continue_button(player) and gamemode == 0):
                        screen_id = 4 
                        add.clear_battlefield(1)
                        add.auto_set_ship(1)
                        static_background(screen_id)

                        x0,y0 = 250,150

                    elif (add.continue_button(player) and gamemode == 1 and player == 0):

                        player += 1
                        add.clear_battlefield(player)

                    elif (add.continue_button(player) and gamemode == 1 and player == 1):

                        screen_id = 4
                        flag_move = True
                        x0,y0 = 250,150
                        player = 1
                        static_background(screen_id)

                    ship_choice = 0

        elif (screen_id == 4 or screen_id == 5): # Here should be myasso
            
            flag_quit, screen_id, ship_choice, gamemode = operator_on_screen(screen_id,gamemode,event)
            flag_move = True

        elif (screen_id == 7): # defend ship!

            add.dehiding_ships(player)
            add.draw_battleground(player)
            flag_move = True

            flag_quit, screen_id, ship_choice, gamemode = operator_on_screen(screen_id, gamemode,event)

            if (ship_choice == 1):
                player = 1 - player
        
        elif (screen_id == 6): #ATTACK SHIP!!!
            
            add.hiding_ships(player)
            add.draw_battleground(player)
            if (flag_move):
                flag_hit = add.attack_on_ships(event,player)

            if (flag_hit == 0):
                flag_move = False

            elif (flag_hit == 2):
                screen_id = 8
                static_background(screen_id)
                
            if (flag_hit != 2):
                flag_quit, screen_id, ship_choice, gamemode = operator_on_buttons(len(button_pushed_image[screen_id]), screen_id, event)

            if (screen_id != 6 and flag_hit != 2):
                screen_id -= player
                static_background(screen_id)

        elif (screen_id == 8): #FINAL SCREEN!
            text(435,275,"number  " + str(player + 1),BLACK, 48)
            x0,y0 = 100,100
            flag_quit, screen_id, ship_choice, gamemode = operator_on_screen(screen_id,gamemode,event)

    pygame.display.update()

pygame.quit()

