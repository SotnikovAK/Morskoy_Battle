from random import choice
from Servise_Functions import *
from Ship_Button_Class import *
from AI_Oscar import *
import image_initializer as im


class Battlefield:

    def __init__(self):
        """
        Battlefield is arrays that reflect the battlefield as a two-dimensional array.
            * 0 - empty cell
            * 1 - cell near the ship
            * > 2 - ships themselves (ship length + 1)
        Used to place ships.
        (12 * 12 - made for simplicity)
        """
        self.battlefield = [[[0] * 12 for i in range(12)] for j in range(2)]
        """
        flag_angle reflects the angle of the ship
            * 0 - horizontal
            * 1 - vertical
        coordinates - coordinates of the topmost (if vertical) 
        (or leftmost (if horizontal)) part of the ship
        """
        self.coordinates, self.flag_angle = [[] * 2 for i in range(2)], [[] * 2 for i in range(2)]
        """
        id defines what kind of ship it is (battleship, carrier or other)
        angle - 180 degree turn rate
        """
        self.id, self.angle = [[], []], [[], []]
        """
        flag_hiding determines whether this ship location should be shown on the screen
        """
        self.flag_hiding = [0, 0]
        """
        catalog - the number of ships left for placement
        """
        self.catalog = [[1, 2, 3, 4], [1, 2, 3, 4]]
        """
        affected_cells_of_seas , affected_cells_of_ships - destroyed cells of the sea or ships, respectively
        """
        self.affected_cells_of_seas = [[], []]
        self.affected_cells_of_ships = [[], []]
        """
        remaining lives of certain ships
        """
        self.lives = [[], []]
        """
        initialization of ship_button
        """
        self.ship = ShipButtons()

    def clear_battlefield(self, n):
        """
        clears the field of ships at the time of deployment
        """
        self.battlefield[n] = [[0] * 12 for i in range(12)]
        self.coordinates[n], self.flag_angle[n] = [], []
        self.id[n], self.angle[n] = [], []
        self.lives[n] = []
        self.flag_hiding[n] = 0
        self.catalog[n] = [1, 2, 3, 4]
        self.affected_cells_of_seas[n] = []
        self.affected_cells_of_ships[n] = []

    def create_ship(self, _ship, screen_id, event):
        """
        will create the ship chosen by the player
        """
        self.ship.creation_buttons(event, _ship, screen_id)

    def manual_placement(self, ship_choice, event, player, coordinates):
        """
        this function is responsible for manually positioning the ship during the placement of ships
        """
        if not self.catalog[player][ship_choice]:
            """
            the ship can be delivered if it is in the ship catalog
            """
            return 0
        if event.type == pg.MOUSEMOTION:
            """
            the ship is drawn as the mouse moves across the screen near it
            """
            self.ship.draw(event)
        elif event.type == pg.MOUSEBUTTONDOWN:
            """
            there was a click
            """
            if event.button == 3:
                """
                the right mouse button is responsible for rotating the ship 90 degrees
                one click + 90 degrees
                """
                self.ship.rotation(event)
            elif event.button == 2:
                """
                if player click on the mouse wheel, the selection of this ship is removed
                """
                return 0

            elif event.button == 1:
                """
                left mouse button player put the ship
                """
                """
                minus one such ship
                """
                self.catalog[player][ship_choice] -= 1
                """
                the next line, the program determines where this boat is placed
                """
                x, y, flag_angle, angle = self.ship.examination_of_button(event, ship_choice, coordinates[0],
                                                                          coordinates[1])
                """
                if (flag_angle == -1 ) - he is put out of bounds
                """
                if flag_angle != -1:

                    if check_can_we_locate_ship_here(x, y, ship_choice, self.battlefield[player], flag_angle):
                        self.battlefield[player] = locate_ship_in_battlefield(ship_choice, self.battlefield[player],
                                                                              flag_angle,
                                                                              y, x)
                        """
                        check the file Ship_Button_Class
                        """
                        """
                        the necessary information is entered into the database
                        """
                        self.coordinates[player].append([y, x])
                        self.flag_angle[player].append(flag_angle)
                        self.id[player].append(ship_choice)
                        self.lives[player].append(im.size_ship[ship_choice] + 1)
                        self.angle[player].append(angle)
                        self.flag_hiding[player] = 1

                    else:
                        """
                        the ship cannot be located here therefore we return the ship to the catalog
                        """
                        self.catalog[player][ship_choice] += 1
                else:
                    """
                    the ship cannot be located here therefore we return the ship to the catalog
                    """
                    self.catalog[player][ship_choice] += 1

            self.ship.draw(event)

        return ship_choice + 1

    def auto_set_ship(self, player):
        """
        there is an automatic placement of ships
        """

        for n in self.catalog[player]:
            """
            for each ship from the catalog, we define a random place where it can stand
            """
            for m in range(n):
                """
                determine whether it will be horizontal or vertical
                """
                flag_angle = choice([0, 1])
                """
                candidates_for_ships is an array of cells in which the ship can stand
                """
                candidates_for_ships = []
                """
                m,k - possible boundaries for the ship
                (counting is carried out from the topmost or leftmost edge of the ship, 
                depending on the horizontal / vertical)
                """
                m, k = 11, 11 - im.size_ship[n - 1]

                if flag_angle:
                    m, k = k, m
                """
                in this cycle, coordinates suitable for all conditions are determined
                (within borders, there are no other ships nearby)
                """
                for i in range(1, m):
                    for j in range(1, k):
                        if ((flag_angle == 0 and self.battlefield[player][i][j] == 0 and self.battlefield[player][i][
                            j + im.size_ship[n - 1]] == 0) or (flag_angle == 1 and self.battlefield[player][i][j] == 0 and
                                                            self.battlefield[player][i + im.size_ship[n - 1]][j] == 0)):
                            candidates_for_ships.append((i, j))
                """
                the coordinate is randomly selected
                """
                coord = choice(candidates_for_ships)
                """
                the necessary information is entered into the database
                """
                self.coordinates[player].append([coord[0], coord[1]])
                self.flag_angle[player].append(int(flag_angle))
                self.id[player].append(n - 1)
                self.lives[player].append(im.size_ship[n - 1] + 1)
                self.angle[player].append(180 * choice([0, 1]))
                for i in range(0, im.size_ship[n - 1] + 1):
                    if flag_angle == 0:
                        self.battlefield[player][coord[0]][coord[1] + i] = im.size_ship[n - 1] + 2
                    else:
                        self.battlefield[player][coord[0] + i][coord[1]] = im.size_ship[n - 1] + 2

                B = im.Ships[n - 1]

                for i in range(len(B)):
                    if flag_angle == 0:
                        self.battlefield[player][int(
                            coord[0] + B[i][1])][int(coord[1] + B[i][0])] = 1
                    else:
                        self.battlefield[player][int(
                            coord[0] + B[i][0])][int(coord[1] + B[i][1])] = 1

        self.flag_hiding[player] = 1
        """
        the catalog is emptied so that the player cannot supply more ships
        """
        self.catalog[player] = [0, 0, 0, 0]

    def draw_battleground(self, player, screen_id, coordinates):
        """
        the field itself is drawn here
        x0,y0 - coordinates of the upper left corner
        """
        x0, y0 = coordinates[0], coordinates[1]
        if screen_id == 2:
            """
            if this is a deployment screen, then it is necessary to 
            show how many ships are still suitable for the deployment
            """
            for i in range(0, 400, 100):
                text(950, 170 + i, str(self.catalog[player][i // 100]), BLACK, 64)

        if len(self.affected_cells_of_seas[player]) > 0:
            """
            here are marked the cells of the sea destroyed by artillery fire
            """
            for i in range(len(self.affected_cells_of_seas[player])):
                _x = pygame.image.load(im.attack_image[1])
                center_ship = ((self.affected_cells_of_seas[player][i][1] - 1) * delta + y0 + delta // 2 + 2 * delta, (
                        self.affected_cells_of_seas[player][i][0] - 1) * delta + x0 + delta // 2 - 2 * delta)
                x_rect = _x.get_rect(center=center_ship)
                screen.blit(_x, x_rect)
        """
        the grid itself is drawn here
        """
        battleground(x0, y0, 10 * delta)

        if self.flag_hiding[player]:
            """
            if we are allowed we draw enemy ships
            """
            for i in range(len(self.id[player])):
                _x = pygame.image.load(im.ships_images[self.id[player][i]])
                x, y = self.coordinates[player][i][1] - 1, self.coordinates[player][i][0] - 1
                half_size_ship = (im.size_ship[self.id[player][i]] + 1) * delta / 2
                if self.flag_angle[player][i] == 0:
                    center_ship = (x * delta + x0 + half_size_ship,
                                   y * delta + delta / 2 + y0)
                    _x, x_rect = rot_center(
                        _x, self.angle[player][i], center_ship[0], center_ship[1])

                else:
                    center_ship = (x * delta + x0 + delta / 2,
                                   y * delta + half_size_ship + y0)
                    _x, x_rect = rot_center(
                        _x, 90 + self.angle[player][i], center_ship[0], center_ship[1])

                x_rect = _x.get_rect(center=center_ship)
                screen.blit(_x, x_rect)

        if len(self.affected_cells_of_ships[player]) > 0:
            """
            here are marked the cells of the ship destroyed by artillery fire
            """
            for i in range(len(self.affected_cells_of_ships[player])):
                _x = pygame.image.load(im.attack_image[0])
                center_ship = ((self.affected_cells_of_ships[player][i][1] - 1) * delta + y0 + delta // 2 + 2 * delta, (
                        self.affected_cells_of_ships[player][i][0] - 1) * delta + x0 + delta // 2 - 2 * delta)
                x_rect = _x.get_rect(center=center_ship)
                screen.blit(_x, x_rect)

    def hiding_ships(self, player):
        """
        hides enemy and allied ships
        """
        self.flag_hiding[player] = 0

    def de_hiding_ships(self, player):
        """
        shows enemy and allied ships
        """
        self.flag_hiding[player] = 1

    def attack_on_ships(self, a, b, player, type_player):
        """
        there is an attack on enemy ships

        a,b - coordinates of the attacked cell
        type_player determines who makes the move: computer or human
        """
        if self.battlefield[player][b][a] < 2:
            """
            shot in milk
            """
            self.affected_cells_of_seas[player].append([b, a])
            return 0

        if self.affected_cells_of_ships[player].count([b, a]) != 0:
            """
            if the cell has already been destroyed then there is no point in further analysis
            """
            return 0
        """
        there is a break
        """
        """
        in further arrays it is determined what kind of ship it was: his number, and type
        """
        list_coord = []
        for i in range(len(self.id[player])):
            x, y = self.coordinates[player][i][1], self.coordinates[player][i][0]

            if self.battlefield[player][b][a] == self.battlefield[player][y][x]:
                list_coord.append(i)

        size_ = self.battlefield[player][b][a] - 1

        for i in list_coord:

            flag = False
            for j in range(size_):

                if (a == self.coordinates[player][i][1] + j and b == self.coordinates[player][i][0] and
                    self.flag_angle[player][i] == 0) or (
                        a == self.coordinates[player][i][1] and b == self.coordinates[player][i][0] + j and
                        self.flag_angle[player][i] == 1):
                    flag = True
                    self.affected_cells_of_ships[player].append([b, a])
                    self.lives[player][i] -= 1
                    break

            if flag:
                break
        """
        if the ship was destroyed, then neighboring cells are also destroyed
        """
        for i in range(len(self.id[player])):
            if self.lives[player][i] == 0:
                for j in range(len(im.Ships[self.id[player][i]])):

                    if self.flag_angle[player][i] == 0:
                        x, y = self.coordinates[player][i][0] + im.Ships[self.id[player][i]][j][1], \
                               self.coordinates[player][i][1] + im.Ships[self.id[player][i]][j][0]
                    else:
                        x, y = self.coordinates[player][i][0] + im.Ships[self.id[player][i]][j][0], \
                               self.coordinates[player][i][1] + im.Ships[self.id[player][i]][j][1]

                    if 0 < x < 11 and 0 < y < 11:
                        self.affected_cells_of_seas[player].append([x, y])
                        if type_player == 'Sam':
                            AI.information_from_server_about_bad_cells(x, y)
        """
        here it is checked suddenly the player has destroyed all the ships
        """
        flag = 0
        for i in range(len(self.id[player])):
            if self.lives[player][i] < 1:
                flag += 1

        if flag == len(self.id[player]):
            return 2

        return 1

    def continue_button(self, player):
        """
        the continue button works only after all ships are placed
        """
        return int(self.catalog[player] == [0, 0, 0, 0])


def human_player_attack_exam(event, coordinates):
    """
    this function checks whether the person has pressed the LMB and whether he is in
    the field with the center of the ship
    """
    x0, y0 = coordinates[0], coordinates[1]
    if event.type != pygame.MOUSEBUTTONDOWN:
        return False
    if not (x0 <= event.pos[0] <= x0 + 10 * delta and y0 <= event.pos[1] <= y0 + 10 * delta):
        return False
    return True


add = Battlefield()
