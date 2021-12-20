from draw_background import *


class Button:
    def __init__(self):
        """
        Here the button is initialized
        """
        self.push_im = []
        self.un_push_im = []
        self.coord_bottom_left = []
        self.size_button = []

    def creation_of_button(self, n, screen_id):
        """
        Here, by n in and screen id, the button coordinates, button images are called
        """
        self.push_im = im.button_pushed_image[screen_id][n]
        self.un_push_im = im.button_unpushed_image[screen_id][n]

        self.coord_bottom_left = im.button_coord[screen_id][n][0]
        self.size_button = im.button_coord[screen_id][n][1]

    def pressure_test(self, event):
        """
        here it is checked if the button is pressed
        """
        return int(self.coord_bottom_left[0] <= event.pos[0] <= self.coord_bottom_left[0] + self.size_button[
            0] and self.coord_bottom_left[1] >= event.pos[1] >= self.coord_bottom_left[1] +
                   self.size_button[1])

    def pushed_button_draw(self):
        """
        The pressed button is drawn here
        """
        _x = pygame.image.load(self.push_im)
        x_rect = _x.get_rect(bottomleft=self.coord_bottom_left)
        screen.blit(_x, x_rect)

    def unpushed_button_draw(self):
        """
        An unpressed button is drawn here
        """
        _x = pygame.image.load(self.un_push_im)
        x_rect = _x.get_rect(bottomleft=self.coord_bottom_left)
        screen.blit(_x, x_rect)


b_n = Button()
"""
Calling a button
"""


def handler_on_buttons(number, screen_id, event, _old):
    """
    here there is an interaction between what the player is doing and the buttons
    """
    new_flag_quit, new_screen_id, new_ship_choice = 0, screen_id, 0
    new_game_mode = -1
    for elem in range(number):
        """
        here the buttons on this particular screen go over
        """
        b_n.creation_of_button(elem, screen_id)

        if event.type == pygame.MOUSEMOTION:
            """
            here are the consequences of the player hovering over this button
            """
            if b_n.pressure_test(event):
                b_n.pushed_button_draw()
                """
                if the cursor is on a button it is colored
                """
            else:
                b_n.unpushed_button_draw()
                """
                if the cursor is not on it, then it is painted in its original color
                """

        elif event.type == pygame.MOUSEBUTTONDOWN:
            """
            there was a click here
            """
            if b_n.pressure_test(event):
                """
                if the click occurred on the territory of the button, then the consequences begin
                """
                new_flag_quit, new_screen_id, new_ship_choice = im.post_pressing_effect[screen_id][elem]
                new_game_mode = im.Game_mode[screen_id][elem]
                """
                if the new screen_id == -10 then leave the old one
                """
                if new_screen_id == -10:
                    new_screen_id = _old

    return new_flag_quit, new_screen_id, new_ship_choice, new_game_mode


def dispatcher_on_buttons_in_screen(screen_id, game_mode, event, _old):
    """
    here is the processing of buttons on the screen
    """
    old_screen_id = screen_id
    flag_quit, screen_id, ship_choice, new_game_mode = handler_on_buttons(len(im.button_pushed_image[screen_id]),
                                                                          screen_id, event, _old)
    """
    if the new game_mod == -1 then leave the old one
    """
    if new_game_mode != -1:
        game_mode = new_game_mode
    """
    If the screen appears and changes, then you need to refresh the screen
    """
    if screen_id != old_screen_id:
        static_background(screen_id)
    return flag_quit, screen_id, ship_choice, game_mode
