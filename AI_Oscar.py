import random as rd


def function_election_candidate_for_shot(not_destroyed_cells_in_battlefield, direction, coordinates_in_process,
                                         flag_angle):
    """
    this function determines the likely cells to hit depending on the direction
    """
    candidate_for_destruction = []
    for i in range(len(direction)):
        x, y = coordinates_in_process[0] + direction[i][flag_angle], coordinates_in_process[1] + direction[i][
            1 - flag_angle]
        if 0 < x < 11 and 0 < y < 11:
            if not_destroyed_cells_in_battlefield.count((x, y)):
                candidate_for_destruction.append((x, y))
    return candidate_for_destruction


def shot(not_destroyed_cells_in_battlefield, old_number_not_destroyed_cells, coord):
    """
    this function fires a shot at the cell with coordinates (x, y)
    """
    not_destroyed_cells_in_battlefield.pop(not_destroyed_cells_in_battlefield.index((coord[0], coord[1])))
    old_number_not_destroyed_cells -= 1
    return not_destroyed_cells_in_battlefield, old_number_not_destroyed_cells, coord[0], coord[1]


class AiSam:
    def __init__(self):
        """
        Initialization of Admiral Oscar
        more information on
        https://ru.wikipedia.org/wiki/%D0%9D%D0%B5%D0%BF%D0%BE%D1%82%D0
        %BE%D0%BF%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D0%B9_%D0%A1%D1%8D%D0%BC
        or
        https://lurkmore.to/%D0%A1%D0%BC%D0%B5%D1%85%D1%83%D0%B5%D1%87%D0%BA%D0%B8:%D0%9D%D0
        %B5%D0%BF%D0%BE%D1%82%D0%BE%D0%BF%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D0%B9_%D0%A1%D1%8D%D0%BC
        """
        self.not_destroyed_cells_in_battlefield = []
        self.old_number_not_destroyed_cells = 100
        self.flag_angle = 0
        self.x = 0
        self.y = 0

        for i in range(10):
            for j in range(10):
                self.not_destroyed_cells_in_battlefield.append((i + 1, j + 1))

        self.coordinates_in_process = [0] * 2

    def first_type_of_attack(self):
        """
        the first type of attack is an attack at a random point on the field,
        which is selected from an array of cells that have not been destroyed
        """
        x, y = rd.choice(self.not_destroyed_cells_in_battlefield)
        self.not_destroyed_cells_in_battlefield, self.old_number_not_destroyed_cells, self.coordinates_in_process[0], \
            self.coordinates_in_process[1] = shot(self.not_destroyed_cells_in_battlefield,
                                                  self.old_number_not_destroyed_cells, (x, y))
        print('1_type_attack', x, y)
        return x, y

    def second_type_of_attack(self):
        """
        the second type of attack - triggered when Oscar hits a ship of non-unit length

        it goes through all possible cells where the continuation of the ship can be

        + - the place of impact
        * - possible location for the continuation of the ship

        principle of operation
              *
            * + *
              *
        """
        direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        candidate_for_destruction = function_election_candidate_for_shot(self.not_destroyed_cells_in_battlefield,
                                                                         direction, self.coordinates_in_process, 0)
        x, y = rd.choice(candidate_for_destruction)
        self.not_destroyed_cells_in_battlefield, self.old_number_not_destroyed_cells, self.x, self.y = shot(
            self.not_destroyed_cells_in_battlefield, self.old_number_not_destroyed_cells, (x, y))
        print('2_type_attack', candidate_for_destruction)

        return x, y

    def third_type_of_attack(self):
        """
        finishing off ships
        """
        direction = [(-1, 0), (1, 0)]
        candidate_for_destruction = function_election_candidate_for_shot(self.not_destroyed_cells_in_battlefield,
                                                                         direction, self.coordinates_in_process,
                                                                         self.flag_angle)

        if len(candidate_for_destruction) != 0:
            x, y = rd.choice(candidate_for_destruction)
            self.not_destroyed_cells_in_battlefield, self.old_number_not_destroyed_cells, self.x, self.y = shot(
                self.not_destroyed_cells_in_battlefield, self.old_number_not_destroyed_cells, (x, y))
        else:
            direction = [(-2, 0), (2, 0)]
            candidate_for_destruction = function_election_candidate_for_shot(self.not_destroyed_cells_in_battlefield,
                                                                             direction, self.coordinates_in_process,
                                                                             self.flag_angle)
            if len(candidate_for_destruction) != 0:
                x, y = rd.choice(candidate_for_destruction)
                self.not_destroyed_cells_in_battlefield, self.old_number_not_destroyed_cells, self.x, self.y = shot(
                    self.not_destroyed_cells_in_battlefield, self.old_number_not_destroyed_cells, (x, y))
            else:
                direction = [(-3, 0), (3, 0)]
                candidate_for_destruction = function_election_candidate_for_shot(
                    self.not_destroyed_cells_in_battlefield,
                    direction, self.coordinates_in_process,
                    self.flag_angle)
                x, y = rd.choice(candidate_for_destruction)

                self.not_destroyed_cells_in_battlefield, self.old_number_not_destroyed_cells, self.x, self.y = shot(
                    self.not_destroyed_cells_in_battlefield, self.old_number_not_destroyed_cells, (x, y))
        print('3_type_attack', x, y)
        return x, y

    def diagonal_death_zone(self):
        """
        this function is triggered when attack type> = 2
        removes diagonal cells from possible attack cells

        there obviously cannot be a ship or other ships

        + - the place of impact
        - - deleted cells

        principle of operation

            -   -
              +
            -   -

        """
        direction = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        for i in range(len(direction)):
            x, y = self.coordinates_in_process[0] + direction[i][0], self.coordinates_in_process[1] + direction[i][1]
            if 0 < x < 11 and 0 < y < 11:
                if self.not_destroyed_cells_in_battlefield.count((x, y)):
                    self.old_number_not_destroyed_cells -= 1
                    print(x, y)
                    self.not_destroyed_cells_in_battlefield.pop(self.not_destroyed_cells_in_battlefield.index((x, y)))

    def angle_determinant(self):
        """
        triggers if during the second phase it turns out that the length of the ship is more than 2

        the found continuation of the ship finds the flag_angle
        flag_angle == 0 - ship horizontal
        flag_angle == 1 - ship vertical
        """
        if abs(self.x - self.coordinates_in_process[0]) == 1:
            self.flag_angle = 0
        else:
            self.flag_angle = 1

    def question_about_destroyed_ship(self):
        """
        checks if the ship is destroyed
        True = Yes
        False = No

        Does it thank to old_number_not_destroyed_cells.
        old_number_not_destroyed_cells - the length of the array with possible cells in the previous step

        At the time of the destruction of the ship, the array sharply reduces the length by several cells
        because of this, there is a discrepancy.
        """
        if len(self.not_destroyed_cells_in_battlefield) != self.old_number_not_destroyed_cells:
            self.old_number_not_destroyed_cells = len(self.not_destroyed_cells_in_battlefield)
            return True
        return False

    def information_from_server_about_bad_cells(self, x, y):
        """
        information about already destroyed cells as a result of the "explosion" of ships.
        """
        if self.not_destroyed_cells_in_battlefield.count((x, y)):
            self.not_destroyed_cells_in_battlefield.pop(self.not_destroyed_cells_in_battlefield.index((x, y)))


"""
Admiral entered the game
"""
AI = AiSam()

