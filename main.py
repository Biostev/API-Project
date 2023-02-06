import pygame
import requests

from settings import *
from drawer import Drawer
from button import Button
from input_box import InputBox
from map import Map

pygame.init()


def make_request(mode: str, scale: str, ll: str, size: str, z: str):
    request = requests.get('https://static-maps.yandex.ru/1.x/',
                           params={
                               'l': mode,
                               'scale': scale,
                               'll': ll,
                               'size': size,
                               'z': z,
                           })
    return request.content


def main() -> None:
    def get_drawn() -> None:
        drawer.draw_button(search_button)
        drawer.draw_button(change_layer_button)
        drawer.draw_input_box(scale_input_box)
        drawer.draw_input_box(cords_input_box)

    def get_buttons_motions() -> dict:
        flag_search = search_button.motion()
        flag_layer = change_layer_button.motion()
        return {
            "search": flag_search,
            "layer": flag_layer
        }

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Map manager")
    drawer = Drawer(screen)

    search_button = Button(True, (260, 530), (75, 35), GREY, BLUE, "Search", 15)
    change_layer_button = Button(True, (60, 530), (150, 35), GREY, BLUE, "Change Layer", 15)

    scale_input_box = InputBox(True, (350, 475), (140, 27), GREY, BLUE, "", "Масштаб", 15)
    cords_input_box = InputBox(True, (45, 475), (140, 27), GREY, BLUE, "", "Координаты", 15)

    response_content = make_request("map", "1.0", "37.530887,55.703118", "350,350", "13")
    with open("map.png", 'wb') as map_file:
        map_file.write(response_content)
    print(response_content)

    mapa = Map(map_sprite, (125, 75))

    while 1:
        screen.fill(LIGHT_LIGHT_GREY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            scale_input_box.motion(event)
            cords_input_box.motion(event)

        drawer.draw_map(mapa)

        get_drawn()
        dict_motions = get_buttons_motions()
        if dict_motions["search"]:
            response_content = make_request("map", "1.0", cords_input_box.text, "350,350", scale_input_box.text)
            print(cords_input_box.text)
            with open("map.png", 'wb') as map_file:
                map_file.write(response_content)
            print(response_content)
            mapa.make_map()
        if dict_motions["layer"]:
            pass

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
