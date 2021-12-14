import random as rd

class AI_Sam():
    def __init__(self):
        #0 - didn't shoot; 1 - missed; 2 - hit
        self.battlefield = [[0] * 12 for i in range(12)]
        #4 - index = lenght of the ship
        self.enemy_ships = [1,2,3,4]#{'Battleship':1, 'Carrier':2, 'Cruiser':3, 'Destroyer':4}
        #hit_flag = True if Sam hitted player's ship in previous move
        self.hit_flag = False
        #moves - array of [x, y, hit_ind], hit_ind = 0 - didn't shoot; 1 - missed; 2 - hit
        self.cur_ship = []
    def set_comp_ships(self):
        #here we call Auto(self.ships)
        pass
    def attack_player(self):
        progress = len(moves)
        if hit_flag:
            if len(cur_ship) == 1:
                #makes random stop from hit
                direction = [(1, 0), (-1, 0), (0, 1), (0, -1)][rd.randint(0, 4)]
                x, y = cur_ship[0] + direction[0], cur_ship[1] + direction[1]
            else:
                if cur_ship[0][0] - cur_ship[1][0] == 0:#ship is horizontal
                    direction = rd.randint(0, 1)
                    if direction:
                        #steps right
                        x = max(cur_ship[:][0]) + 1
                        y = cur_ship[0][1] #y of the cur_ship is constant
                    else:
                        #steps left
                        x = min(cur_ship[:][0]) - 1
                        y = cur_ship[0][1]
                else:
                    direction = rd.randint(0, 1)
                    if direction:
                        #steps down
                        x = cur_ship[0][0] #x of the cur_ship is constant
                        y = max(cur_ship[:][1]) + 1
                    else:
                        #steps upwards
                        x = cur_ship[0][0] 
                        y = min(cur_ship[:][1]) - 1
        else:
            x, y = rd.randint(0, 12), rd.randint(0, 12)
            
        if self.battlefield[x][y] != 0 or (x not in range(0,13)) or (y not in range(0, 13)):
            x,y = attack_player()
        else:
            return x, y
    def account_hit(self, x, y):
        #adjust point to current ship and raises hit_flag
        self.cur_ship.append([x,y])
        self.hit_flag = True
    def account_ship(self, x, y):
        #deleting destroyed ship from self.enemy_ships and clears cur_ship
        self.enemy_ships[4 - len(cur_ship)] -= 1
        self.cur_ship.clear()
    def account_miss(x,y):
        #lowers hit_flag
        self.hit_flag = False