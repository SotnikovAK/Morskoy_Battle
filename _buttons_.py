import json


Name_files_buttons = ['menu_buttons.json', 'question_about_gamemode_buttons.json', 'set_ships_buttons.json', 'question_quit_buttons.json',
                      'screen_of_first-second_player.json', 'screen_of_first-second_player.json', 'field_of_attack_player_buttons.json', 'field_of_defender_player_buttons.json','final_screen_buttons.json']

p = len(Name_files_buttons)
button_pushed_image = [0] * p
button_unpushed_image = [0] * p
button_coord = [0] * p
post_pressing_effect = [0] * p
Gamemode = [0] * p

k = 0

for name_file in Name_files_buttons:
    a, b, c, d, e = [], [], [], [], []
    with open(name_file) as buttons_json_file:
        buttons_list = json.load(buttons_json_file)

    for i in range(len(buttons_list)):
        a.append(buttons_list[i]["pushed"])
        b.append(buttons_list[i]["unpushed"])
        c.append(buttons_list[i]["coords"])
        d.append(buttons_list[i]["post_effect"])
        e.append(buttons_list[i]["gamemode"])

    button_pushed_image[k] = a
    button_unpushed_image[k] = b
    button_coord[k] = c
    post_pressing_effect[k] = d
    Gamemode[k] = e
    k += 1
