import random as rd

class AI_Sam():
    def __init__(self):
        self.not_detroyed_cells_in_battlefield = []
        self.old_number_not_destroyed_cells = 100
        self.flag_angle = 0
        self.x = 0
        self.y = 0

        for i in range(10):
            for j in range(10):
                self.not_detroyed_cells_in_battlefield.append((i+1,j+1))

        self.coordinates_in_process = [0] * 2
    
    def first_type_of_attack(self):

        x,y = rd.choice(self.not_detroyed_cells_in_battlefield)
        self.not_detroyed_cells_in_battlefield.pop(self.not_detroyed_cells_in_battlefield.index((x,y)))
        self.old_number_not_destroyed_cells -= 1

        self.coordinates_in_process[0],self.coordinates_in_process[1] = x,y
        return x,y

    def second_type_of_attack(self):

        direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        candidate_for_destruction = []
        print('-----------')
        print(self.coordinates_in_process)
        for i in range(len(direction)):
            x,y = self.coordinates_in_process[0] + direction[i][0], self.coordinates_in_process[1] + direction[i][1]
            if (x > 0 and x < 11 and y > 0 and y < 11 ):
                if (self.not_detroyed_cells_in_battlefield.count((x,y))):
                    candidate_for_destruction.append((x,y))
        x,y = rd.choice(candidate_for_destruction)
        self.not_detroyed_cells_in_battlefield.pop(self.not_detroyed_cells_in_battlefield.index((x,y)))
        self.x,self.y = x,y
        print(x,y)
        self.old_number_not_destroyed_cells -= 1
        return x,y

    def third_type_of_attack(self):
        direction = [(-3,0),(-2,0),(-1,0),(1,0),(2,0),(3,0)]
        candidate_for_destruction = []
        print('+++++++++++++')
        for i in range(len(direction)):
            x,y = self.coordinates_in_process[0] + direction[i][self.flag_angle], self.coordinates_in_process[1] + direction[i][1 - self.flag_angle]
            print('*',x,y)
            if (x > 0 and x < 11 and y > 0 and y < 11 ):
                if (self.not_detroyed_cells_in_battlefield.count((x,y))):
                    candidate_for_destruction.append((x,y))
        x,y = rd.choice(candidate_for_destruction)
        self.not_detroyed_cells_in_battlefield.pop(self.not_detroyed_cells_in_battlefield.index((x,y)))
        self.x,self.y = x,y
        print(x,y)
        self.old_number_not_destroyed_cells -= 1
        return x,y

    def diagonal_death_zone(self):
        direction = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        for i in range(len(direction)):
            x,y = self.coordinates_in_process[0] + direction[i][0], self.coordinates_in_process[1] + direction[i][1]
            if (x > 0 and x < 11 and y > 0 and y < 11 ):
                if (self.not_detroyed_cells_in_battlefield.count((x,y))):
                    self.old_number_not_destroyed_cells -= 1
                    print(x,y)
                    self.not_detroyed_cells_in_battlefield.pop(self.not_detroyed_cells_in_battlefield.index((x,y)))
    
    def angle_determinant(self):
        if (abs(self.x - self.coordinates_in_process[0]) == 1):
            self.flag_angle = 0
        else:
            self.flag_angle = 1
        print(self.flag_angle)

    def question_about_destroyed_ship(self):
        if (len(self.not_detroyed_cells_in_battlefield) != self.old_number_not_destroyed_cells):
            self.old_number_not_destroyed_cells = len(self.not_detroyed_cells_in_battlefield)
            return True
        return False
    def information_from_server_about_bad_cells(self,x,y):

        if (self.not_detroyed_cells_in_battlefield.count((x,y))):
            self.not_detroyed_cells_in_battlefield.pop(self.not_detroyed_cells_in_battlefield.index((x,y)))

AI = AI_Sam()
