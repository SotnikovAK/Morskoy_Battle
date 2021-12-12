import pygame
from pygame.draw import *
from _constans import *
from _buttons_ import *
from _main_game_parmetres import *
from Servise_Functions import *
from init_screen import *

class Ship_Buttons:

    def _init(self, event, n, screen_id):
        self.image = pygame.image.load(button_unpushed_image[screen_id][n])
        self.image, self.image_rect = rot_center(
            self.image, 0, event.pos[0], event.pos[1])
        self.size = button_coord[screen_id][n][1]
        self.angle_flag = 0
        self.angle = 0

    def examination_of_button(self, event, _ship,B):
        A = [(-2, 0), (-1, 0), (-1, 0), (0, 0)]
        x0,y0 = B[0],B[1]
        X, Y = event.pos[0]- x0 + delta, event.pos[1] - y0 + delta
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

        self.image, self.image_rect = rot_center(
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
