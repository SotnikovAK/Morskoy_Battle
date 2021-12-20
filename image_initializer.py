import json

background_image = []
Name_files_buttons = []
attack_image = []
ships_images = []


"""
This file is where the json list is read and processed.
"""
with open("Json_files/background.json") as buttons_json_file:
    buttons_list = json.load(buttons_json_file)

for i in range(len(buttons_list)):
    """
    treatment of background.json
    """
    background_image.append(buttons_list[i]["image"])
    Name_files_buttons.append(buttons_list[i]["buttons"])

"""
this list is not in the class Dispatcher_Game
because they are constant arrays that don't change
"""
button_pushed_image = [[] for i in range(len(Name_files_buttons))]
button_unpushed_image = [[] for i in range(len(Name_files_buttons))]
button_coord = [[] for i in range(len(Name_files_buttons))]
post_pressing_effect = [[] for i in range(len(Name_files_buttons))]
Game_mode = [[] for i in range(len(Name_files_buttons))]

"""
treatment of buttons
"""
k = 0
for name_file in Name_files_buttons:
    button_pushed_image_in_screen = []
    button_unpushed_image_in_screen = []
    button_coord_in_screen = []
    post_pressing_effect_in_screen = []
    Game_mode_in_screen = []
    """
    k, button_pushed_image_in_screen, button_unpushed_image_in_screen, button_coord_in_screen, 
    post_pressing_effect_in_screen,Game mode_in_screen is local variables are used only here
    """
    with open(name_file) as buttons_json_file:
        buttons_list = json.load(buttons_json_file)

    for i in range(len(buttons_list)):
        button_pushed_image_in_screen.append(buttons_list[i]["pushed"])
        button_unpushed_image_in_screen.append(buttons_list[i]["unpushed"])
        button_coord_in_screen.append(buttons_list[i]["coordinates"])
        post_pressing_effect_in_screen.append(buttons_list[i]["post_effect"])
        Game_mode_in_screen.append(buttons_list[i]["game_mode"])

    button_pushed_image[k] = button_pushed_image_in_screen
    button_unpushed_image[k] = button_unpushed_image_in_screen
    button_coord[k] = button_coord_in_screen
    post_pressing_effect[k] = post_pressing_effect_in_screen
    Game_mode[k] = Game_mode_in_screen
    k += 1

"""
As a result, we get five arrays, by which, by requesting the screen_id and serial number of the button, we can 
completely restore it:
    - in button_pushed_image - the image of the filled button is stored
    - in button_unpushed_image - the button image is stored in
    - button_coord - stores the bottom left corner and the size of the button
    - in post_pressing_effect - three digits are stored:
            * the first is the exit flag, shows whether to exit the game
            * second - new screen id (== -10 returns old screen id)
            * the third is the parameter responsible for special conditions, for example, if 
              this is the ship placement screen, then it is responsible for activating special movable buttons,
              which We call Ship_buttons
    - in Game_mode - which game mode is stored, 
            * == 0 is a two-player war mode
            * == 1 is ai war mode
            * == -1 - retains the old game mode
"""
"""
Here images of impact_on_hit
"""
with open("Json_files/Json_files_battle_objects/impact_on_hit.json") as buttons_json_file:
    buttons_list = json.load(buttons_json_file)

for i in range(len(buttons_list)):
    attack_image.append(buttons_list[i]["image"])

"""
    Here images of ships
"""

with open("Json_files/Json_files_battle_objects/ships.json") as buttons_json_file:
    buttons_list = json.load(buttons_json_file)

Ships = []
ships_images = []
size_ship = []

for i in range(len(buttons_list)):
    ships_images.append(buttons_list[i]["image"])
    size_ship.append(buttons_list[i]["size_ship"] - 1)
    Ships.append(buttons_list[i]["after destruction"])
"""
this if size ship - 1 , this is used when placing ships
"""

"""
these are the cells adjacent to the ship, if we consider them horizontal and the leftmost cell is considered 
the reference cell, due to this specificity, it is difficult to do this cycle, it is used when placing ships
(auto and manual modes), their destruction.
"""
"""
    * - desired cells
    + - cell of reference
    - - the rest of the cells of the ships
"""
"""
    * - desired cells
    + - cell of reference
    - - the rest of the cells of the ships
"""
"""
Battleship
    * * * * * *
    * + - - - *
    * * * * * *
"""
"""
Carrier
    * * * * * *
    * + - - - *
    * * * * * *
"""
"""
etc
"""
