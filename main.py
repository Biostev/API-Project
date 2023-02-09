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


def change_map(longitude_input_box: InputBox,
               latitude_input_box: InputBox,
               scale_input_box: InputBox,
               mapa: Map) -> None:
    response_content = make_request("map", "1.0", longitude_input_box.text + ',' + latitude_input_box.text,
                                    "350,350", scale_input_box.text)
    print(response_content)
    with open("map.png", 'wb') as map_file:
        map_file.write(response_content)
    mapa.make_map()


def cycle(input_box_object: InputBox) -> None:
    if float(input_box_object.text) >= 0:
        if float(input_box_object.text) > 180:
            input_box_object.text = str(float(input_box_object.text) % -180.0)
    else:
        if float(input_box_object.text) < -180:
            input_box_object.text = str(float(input_box_object.text) % 180.0)


def main() -> None:
    def get_drawn() -> None:
        drawer.draw_button(search_button)
        drawer.draw_button(change_layer_button)
        drawer.draw_input_box(scale_input_box)
        drawer.draw_input_box(longitude_input_box)
        drawer.draw_input_box(latitude_input_box)

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
    longitude_input_box = InputBox(True, (45, 480), (100, 27), GREY, BLUE, "", "Долгота", 15)
    latitude_input_box = InputBox(True, (45, 445), (100, 27), GREY, BLUE, "", "Широта", 15)

    response_content = make_request("map", "1.0", "37.530887,55.703118", "350,350", "13")
    with open("map.png", 'wb') as map_file:
        map_file.write(response_content)

    mapa = Map(map_sprite, (125, 75))

    while 1:
        screen.fill(LIGHT_LIGHT_GREY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if longitude_input_box.text != longitude_input_box.background_text:
                        longitude_input_box.text = str(float(longitude_input_box.text) - 1)
                        cycle(longitude_input_box)
                        change_map(longitude_input_box, latitude_input_box, scale_input_box, mapa)
                elif event.key == pygame.K_DOWN:
                    if latitude_input_box.text != latitude_input_box.background_text:
                        if float(latitude_input_box.text) - 1 > -90:
                            latitude_input_box.text = str(float(latitude_input_box.text) - 1)
                            change_map(longitude_input_box, latitude_input_box, scale_input_box, mapa)
                elif event.key == pygame.K_RIGHT:
                    if longitude_input_box.text != longitude_input_box.background_text:
                        longitude_input_box.text = str(float(longitude_input_box.text) + 1)
                        cycle(longitude_input_box)
                        change_map(longitude_input_box, latitude_input_box, scale_input_box, mapa)
                elif event.key == pygame.K_UP:
                    if latitude_input_box.text != latitude_input_box.background_text:
                        if float(latitude_input_box.text) + 1 < 90:
                            latitude_input_box.text = str(float(latitude_input_box.text) + 1)
                            change_map(longitude_input_box, latitude_input_box, scale_input_box, mapa)

            scale_input_box.motion(event)
            longitude_input_box.motion(event)
            latitude_input_box.motion(event)

        drawer.draw_map(mapa)

        get_drawn()
        dict_motions = get_buttons_motions()
        if dict_motions["search"]:
            change_map(longitude_input_box, latitude_input_box, scale_input_box, mapa)
        if dict_motions["layer"]:
            pass

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
