import pygame
from pygame.constants import MOUSEBUTTONDOWN
from pygame.draw import *
from random import choice
import json

pygame.init()

FPS = 100
screen = pygame.display.set_mode((1000, 900))

BLACK = (0, 0, 0)

button_pushed_image = [('images_buttons/exit_pushed_button.png', 'images_buttons/button_pushed_play.png',
                        'images_buttons/button_pushed_settings.png'), ('images_buttons/AI_gamemode_pushed.png', 'images_buttons/pushed_pass_next.png'), ('images_buttons/Tirpitz_pushed_button.png', 'images_buttons/essex_pushed_button.png', 'images_buttons/kirov_pushed_button.png', 'images_buttons/destroyer_pushed_button.png', 'images_buttons/exit_pushed_button.png', 'images_buttons/button_pushed_auto.png', 'images_buttons/button_pushed_clear.png', 'images_buttons/button_pushed_continue.png'),
                       ('images_buttons/return_in_game_pushed_button.png', 'images_buttons/return_in_the_menu_pushed_button.png', 'images_buttons/return_in_quit_pushed_button.png')]
button_unpushed_image = [('images_buttons/exit_unpushed_button.png', 'images_buttons/button_unpushed_play.png',
                          'images_buttons/button_unpushed_settings.png'), ('images_buttons/Al_gamemode_unpushed.png', 'images_buttons/unpushed_pass_next.png'), ('images_buttons/Tirpitz.png', 'images_buttons/essex.png', 'images_buttons/kirov.png', 'images_buttons/cringe_destroyer.png', 'images_buttons/exit_unpushed_button.png', 'images_buttons/button_unpushed_auto.png', 'images_buttons/button_unpushed_clear.png', 'images_buttons/button_unpushed_continue.png'),
                         ('images_buttons/return_in_game_unpushed_button.png', 'images_buttons/return_in_the_menu_unpushed_button.png', 'images_buttons/return_in_quit_unpushed_button.png')]
button_coord = [[[(902, 105), (100, -100)], [(432, 522), (137, -143)], [(902, 205), (100, -100)]],
                [[(321, 438), (362, -98)], [(321, 558), (362, -100)]],
                [[(720, 224), (200, -50)], [(720, 322), (150, -50)], [(720, 421), (100, -50)], [(721, 520), (50, -50)],
                 [(900, 105), (100, -100)], [(845, 740), (150, -50)], [(697, 740), (150, -50)], [(197, 803), (300, -50)]],
                [[(229, 477), (543, -63)], [(229, 544), (544, -62)], [(229, 610), (544, -62)]]]

attack_image = ['images_static_battleground/hit_on_sea.png','images_static_battleground/hit_on_ship.png']

background_image = ['images_static_battleground/menu_game.png',
                    'images_static_battleground/question_about_gamemode.png',
                    'images_static_battleground/selection_of_ships.png',
                    'images_static_battleground/question_quit.png',
                    'images_static_battleground/field_of_attack_player.png',
                    'images_static_battleground/field_of_defend_player.png']
post_pressing_effect = [[(1, 0, 0), (0, 1, 0), (0, 8, 0)], [
    (0, 2, 0), (0, 5, 0)], [(0, 2, 1), (0, 2, 2), (0, 2, 3), (0, 2, 4), (0, 3, 0), (0, 2, -1), (0, 2, -2), (0, 2, -3)], [(0, 2, 0), (0, 0, 0), (1, 0, 0)]]

ships_images = ['images_buttons/Tirpitz.png', 'images_buttons/essex.png',
                'images_buttons/kirov.png', 'images_buttons/cringe_destroyer.png']

Battleship = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (2, 1),
              (3, 1), (4, 1), (4, 0), (4, -1), (3, -1), (2, -1), (1, -1), (0, -1)]
Carrier = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (2, 1),
           (3, 1), (3, 0), (3, -1), (2, -1), (1, -1), (0, -1)]
Cruiser = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1),
           (2, 1), (2, 0), (2, -1), (1, -1), (0, -1)]
Destroyer = [(-1, -1), (-1, 0), (-1, 1), (0, 1),
             (1, 1), (1, 0), (1, -1), (0, -1)]
Ships = [Battleship, Carrier, Cruiser, Destroyer]


class Button:
    def _init(self, n):

        self.push_im = button_pushed_image[screen_id][n]
        self.unpush_im = button_unpushed_image[screen_id][n]

        self.coord_bottomleft = button_coord[screen_id][n][0]
        self.size_button = button_coord[screen_id][n][1]

    def pressure_test(self, event):
        return (int(event.pos[0] >= self.coord_bottomleft[0] and event.pos[0] <= self.coord_bottomleft[0] + self.size_button[0] and event.pos[1] <= self.coord_bottomleft[1] and event.pos[1] >= self.coord_bottomleft[1] + self.size_button[1]))

    def pushed_button_draw(self):
        _x = pygame.image.load(self.push_im)
        x_rect = _x.get_rect(bottomleft=self.coord_bottomleft)
        screen.blit(_x, x_rect)

    def unpushed_button_draw(self):
        _x = pygame.image.load(self.unpush_im)
        x_rect = _x.get_rect(bottomleft=self.coord_bottomleft)
        screen.blit(_x, x_rect)

class Ship_Buttons:

    def _init(self, event, n):
        self.image = pygame.image.load(button_unpushed_image[screen_id][n])
        self.image, self.image_rect = s_f.rot_center(
            self.image, 0, event.pos[0], event.pos[1])
        self.size = button_coord[screen_id][n][1]
        self.angle_flag = 0
        self.angle = 0

    def examination_of_button(self, event, _ship):
        A = [(-2, 0), (-1, 0), (-1, 0), (0, 0)]
        X, Y = event.pos[0]-x0 + delta, event.pos[1] - x0 + delta
        a, b = X//delta, Y//delta
        c = -1
        if self.angle_flag == 0:
            a, b = a + A[_ship][0], b + A[_ship][1]
            if (a >= 1 and a + size_ship[_ship] <= 10 and 1 <= b and b <= 10):
                c = self.angle_flag
        else:
            a, b = a + A[_ship][1], b + A[_ship][0]
            if (b >= 1 and b + size_ship[_ship] <= 10 and 1 <= a and a <= 10):
                c = self.angle_flag
        return a, b, c, _ship, self.angle//180 * 180

    def rotation(self, event):

        self.image, self.image_rect = s_f.rot_center(
            self.image, 90, event.pos[0], event.pos[1])
        if (self.angle_flag == 1):
            self.angle_flag = 0
        else:
            self.angle_flag = 1
        self.angle += 90
        screen.blit(self.image, self.image_rect)

    def _draw(self, event):
        self.image_rect = self.image.get_rect(
            center=(event.pos[0], event.pos[1]))
        screen.blit(self.image, self.image_rect)

def static_background(flag):

    _x = pygame.image.load(background_image[flag])
    x_rect = _x.get_rect(bottomleft=(0, 900))
    screen.blit(_x, x_rect)

def operator_on_buttons(number, screen_id, event):
    a, b, c = 0, screen_id, 0
    for i in range(number):

        b_n._init(i)
        if event.type == pygame.MOUSEMOTION:
            if (b_n.pressure_test(event)):
                b_n.pushed_button_draw()
            else:
                b_n.unpushed_button_draw()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (b_n.pressure_test(event)):
                a, b, c = post_pressing_effect[screen_id][i]
    return a, b, c

class Battlefield():

    def _init_battlefield(self):

        self.battlefield = [
            [[0] * 12 for i in range(12)], [[0] * 12 for i in range(12)]]
        self.coordinates , self.flag_angle = [[] * 2 for i in range(2)], [[] * 2 for i in range(2)]
        self.id, self.angle = [[] * 2 for i in range(2)], [[] * 2 for i in range(2)]
        self.flag = [0,0]
        self.catalog = [[1, 2, 3, 4], [1 , 2, 3, 4]]

    def clear_battlefield(self, n):

        self.battlefield[n] = [[0] * 12 for i in range(12)]
        self.coordinates[n] , self.flag_angle[n] = [], []
        self.id[n], self.angle[n] = [], []
        self.flag[n] = 0
        self.catalog[n] = [1, 2, 3, 4]

    def _init_ship(self, _ship):
        self.ship = Ship_Buttons()
        self.ship._init(event, _ship)

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
                s_f.text(950, 170 + i, str(self.catalog[N][i//100]), BLACK, 64)

        s_f.battleground(x0, y0, 10 * delta)

        if (self.flag[N] == 1):
            for i in range(len(self.id[N])):
                _x = pygame.image.load(ships_images[self.id[N][i]])
                x, y = self.coordinates[N][i][1] - 1, self.coordinates[N][i][0] - 1
                half_size_ship = (size_ship[self.id[N][i]] + 1) * delta / 2
                if (self.flag_angle[N][i] == 0):
                    center_ship = (x * delta + x0 + half_size_ship,
                                   y * delta + delta / 2 + y0)
                    _x, x_rect = s_f.rot_center(
                        _x, self.angle[N][i], center_ship[0], center_ship[1])

                else:
                    center_ship = (x * delta + x0 + delta / 2,
                                   y * delta + half_size_ship + y0)
                    _x, x_rect = s_f.rot_center(
                        _x, 90 + self.angle[N][i], center_ship[0], center_ship[1])

                x_rect = _x.get_rect(center=center_ship)
                screen.blit(_x, x_rect)

    def hiding_ships(self,N):
        self.flag[N] = 0

    def dehiding_ships(self,N):
        self.flag[N] = 1

    def attack_on_ships(self,event,N):
        if (event.type == pygame.MOUSEBUTTONDOWN ):
            if ( x0 <= event.pos[0] and event.pos[0] <= x0 + 10 * delta and y0 <= event.pos[1] and event.pos[1] <= y0 + 10 * delta ):
                a,b = (event.pos[0] - x0) // delta + 1, (event.pos[1]-y0) // delta + 1

                if (self.battlefield[N][b][a] > 1 ):
                    self.battlefield[N][b][a] = 999
                
    def continue_button(self,N):
        return (int(self.catalog[N] == [0, 0, 0, 0]))
    
    def print_battlefield(self): #these function for only view
        print('First Field')
        for row in self.battlefield[0]:
            print(' '.join([str(elem) for elem in row]))
        print('Second Field')
        for row in self.battlefield[1]:
            print(' '.join([str(elem) for elem in row]))

        print(self.coordinates[0])
        print(self.coordinates[1])

def operator_on_screen(screen_id):
    old_screen_id = screen_id
    flag_quit, screen_id, ship_choice = operator_on_buttons(
        len(button_pushed_image[screen_id]), screen_id, event)
    if screen_id != old_screen_id:
        static_background(screen_id)
    return flag_quit, screen_id, ship_choice

class Servise_Function:
    def battleground(self, x, y, n):

        for i in range(0, n + n//10, n//10):

            line(screen, BLACK, (x+i, y), (x+i, y+n), 5)
            line(screen, BLACK, (x, y+i), (x+n, y+i), 5)

    def rot_center(self, image, angle, x, y):

        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(
            center=image.get_rect(center=(x, y)).center)

        return rotated_image, new_rect

    def text(self, x, y, A, color, size):
        pygame.font.init()
        myfont = pygame.font.SysFont(' ', size)
        textsurface = myfont.render(A, False, color)
        screen.blit(textsurface, (x, y))

    def full_sum_ships(self, ship_catalog):
        S = 0
        for i in range(len(ship_catalog)):
            S += ship_catalog[i]
        return S


pygame.display.update()
clock = pygame.time.Clock()
finished = False


screen_id , flag_quit , gamemode , ship_choice = 0 , 0 , 0 , 0
_ship_catalog = [1, 2, 3, 4]
ship_catalog = _ship_catalog
size_ship = [3, 2, 1, 0]

s_f = Servise_Function()
b_n = Button()
add = Battlefield()

x0, y0 = 100, 100
delta = 50

static_background(screen_id)

while not finished:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or flag_quit == 1:
            finished = True
        elif screen_id != 2 and screen_id != 4 and screen_id != 5:

            if (screen_id != 3):
                add._init_battlefield()
            flag_quit, screen_id, ship_choice = operator_on_screen(screen_id)
            flag_fill = False

        elif screen_id == 2:  # SET YOUR SHIPS

            static_background(screen_id)
            add.draw_battleground(0)

            if (ship_choice == 0):
                flag_quit, screen_id, ship_choice = operator_on_screen(
                    screen_id)
                flag_init_ships = True
                if (flag_fill == True and ship_choice > 0):
                    ship_choice = 0

            else:
                if (flag_init_ships == True and ship_choice > 0 and flag_fill == False):
                    flag_init_ships = False
                    add._init_ship(ship_choice - 1)

                elif (ship_choice > 0 and flag_fill == False):

                    ship_choice = add.operator_on_ships_button(
                        ship_choice - 1, event, 0)

                elif (ship_choice == -2):

                    add.clear_battlefield(0)
                    ship_choice = 0
                    flag_fill = False

                elif (ship_choice == -1):

                    add.clear_battlefield(0)
                    add.auto_set_ship(0)
                    ship_choice = 0
                    flag_fill = True

                elif (ship_choice == -3):
                    if (add.continue_button(0)):
                        screen_id = 4 
                        add.clear_battlefield(1)
                        add.auto_set_ship(1)

                        flag_move = True

                        static_background(screen_id)
                        add.print_battlefield()
                        x0,y0 = 250,150
                    ship_choice = 0

        elif (screen_id == 4): # Here should be myasso
            
            add.hiding_ships(1)
            add.draw_battleground(1)

            add.attack_on_ships(event,1)

            pass
        elif (screen_id == 5):
            add.draw_battleground(0)

    pygame.display.update()
    pygame.display.set_caption("Sea Battle")
pygame.quit()
