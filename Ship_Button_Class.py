from constans import *
from init_screen import *
import pygame as pg
import image_initializer as im
import Servise_Functions as Sf

class ShipButtons:
    def __init__(self):
        """
        Special buttons are generated here that are used to place ships. They can rotate depending on the player's
         actions, they follow the cursor when the player has selected them
        """
        self.image = pg.Surface((1500, 1500))
        self.image_rect = pg.Surface((1500, 1500))
        self.size = []
        self.angle_flag = 0
        self.angle = 0

    def creation_buttons(self, event, n, screen_id):
        """
        here these buttons are created by angle, coordinates and sizes
        """
        self.image = pg.image.load(im.button_unpushed_image[screen_id][n])
        self.image, self.image_rect = Sf.rot_center(self.image, 0, event.pos[0], event.pos[1])
        self.size = im.button_coord[screen_id][n][1]
        """
        self.angle_flag = 0 - the ship is horizontal
        self.angle_flag = 1 - the ship is vertical
        """
        self.angle_flag = 0
        self.angle = 0

    def examination_of_button(self, event, _ship, x0, y0):
        """
        The final stage in the life of this button is when it is put on the field.
        Here coordinates in the array are determined where the ship is installed (a, b), and its final angle
        (flag horizontal_vertical, flag rotation on 180 degrees (self.angle // 180 * 180)).
        """
        """
        _ship - which ship is it
        """
        a, b = (event.pos[0] - x0 + delta) // delta, (event.pos[1] - y0 + delta) // delta
        c = -1
        """
        if (flag_angle (c) == -1):
            the ship cannot be put here due to the fact that the coordinates are located where they always cannot be
        """
        if self.angle_flag == 0:
            a, b = a + delta_limits_placements_ships[_ship][0], b + delta_limits_placements_ships[_ship][1]
            """
            it is taken into account that the ships have a length
            """
            if 1 <= a <= 10 - im.size_ship[_ship] and 1 <= b <= 10:
                c = self.angle_flag
        else:
            a, b = a + delta_limits_placements_ships[_ship][1], b + delta_limits_placements_ships[_ship][0]
            """
            it is taken into account that the ships have a length
            """
            if 1 <= a <= 10 and 1 <= b <= 10 - im.size_ship[_ship]:
                c = self.angle_flag

        return a, b, c, self.angle // 180 * 180

    def rotation(self, event):
        """
        there is a 90 degrees turn
        """
        self.image, self.image_rect = Sf.rot_center(self.image, 90, event.pos[0], event.pos[1])
        self.angle_flag = 1 - self.angle_flag
        self.angle += 90
        screen.blit(self.image, self.image_rect)

    def draw(self, event):
        """
        This button is drawn here when it follows the cursor.
        """
        self.image_rect = self.image.get_rect(center=(event.pos[0], event.pos[1]))
        screen.blit(self.image, self.image_rect)


def check_can_we_locate_ship_here(x, y, ship_choice, player_battlefield, flag_angle):
    """
    here it is determined whether we can put the ship in this position on the field
    if flag_check == True then we can put a ship there
    otherwise no
    """
    """
    the first cycle determines whether there are other ships where our
    """
    flag_check = True
    for delta_coord in range(im.size_ship[ship_choice] + 1):
        if (not flag_angle and player_battlefield[y][x + delta_coord] != 0) or (
                flag_angle and player_battlefield[y + delta_coord][x] != 0):
            flag_check = False
            break
    """
    the second cycle for the sake of optimization is triggered when the first one is triggered
    it determines whether another ship can stand in the grinding in our ship
    
    that is, if the adjacent values around the ship are greater than 1
    """
    if flag_check:
        for delta_coord in range(len(im.Ships[ship_choice])):
            if (flag_angle == 0 and
                player_battlefield[y + im.Ships[ship_choice][delta_coord][1]]
                    [x + im.Ships[ship_choice][delta_coord][0]] > 1)\
                    or (flag_angle == 1 and
                        player_battlefield[y + im.Ships[ship_choice][delta_coord][0]]
                        [x + im.Ships[ship_choice][delta_coord][1]] > 1):
                flag_check = False
            break

    return flag_check


def locate_ship_in_battlefield(ship_choice, player_battlefield, flag_angle, y, x):
    """
    puts the ship on the board in the position chosen by the player
    """
    """
    the first cycle is responsible for the placement of the ship itself
    these cells are equal to its total length + 1
    """
    for i in range(im.size_ship[ship_choice] + 1):
        if not flag_angle:
            player_battlefield[y][x + i] = im.size_ship[ship_choice] + 2
        else:
            player_battlefield[y + i][x] = im.size_ship[ship_choice] + 2
    """
    the second cycle covers neighboring cells around the ship with ones
    """
    for i in range(len(im.Ships[ship_choice])):
        if not flag_angle:
            player_battlefield[y + im.Ships[ship_choice][i][1]][x + im.Ships[ship_choice][i][0]] = 1
        else:
            player_battlefield[y + im.Ships[ship_choice][i][0]][x + im.Ships[ship_choice][i][1]] = 1
    """
    example for an aircraft carrier
    0 0 0 0 0 0 0 0
    0 0 1 1 1 1 1 0
    0 0 1 4 4 4 1 0
    0 0 1 1 1 1 1 0
    0 0 0 0 0 0 0 0
    """
    return player_battlefield
