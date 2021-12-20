from init_screen import *
import image_initializer as im


def static_background(screen_id):
    """
    it draws a background that does not change during processes on the screen with a constant screen_id
    """
    _x = pygame.image.load(im.background_image[screen_id])
    x_rect = _x.get_rect(bottomleft=(0, 900))
    screen.blit(_x, x_rect)
