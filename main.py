import pygame.event
import requests

from settings import *
from drawer import Drawer
from button import Button
from input_box import InputBox
from map import Map

pygame.init()


def make_request(mode: int, scale: str, ll: str, size: str, z: str):
    modes = {0: 'map',
             1: 'sat',
             2: 'sat,skl'}

    request = requests.get('https://static-maps.yandex.ru/1.x/',
                           params={
                               'l': modes[mode],
                               'scale': scale,
                               'll': ','.join(ll),
                               'size': size,
                               'z': z,
                           })
    return request.content


def change_map(params, mapa: Map) -> None:
    response_content = make_request(**params)
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
    current_params = {'mode': 0,
                      'scale': '1.0',
                      'll': ['37.530887',
                             '55.703118'],  # longitude, latitude
                      'size': '350,350',
                      'z': '13'}

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
    scale_input_box.text = current_params['z']
    longitude_input_box = InputBox(True, (45, 480), (100, 27), GREY, BLUE, "", "Долгота", 15)
    longitude_input_box.text = current_params['ll'][0]
    latitude_input_box = InputBox(True, (45, 445), (100, 27), GREY, BLUE, "", "Широта", 15)
    latitude_input_box.text = current_params['ll'][1]

    def make_correct():
        z = current_params['z']
        ll = current_params['ll']
        if not z.isdigit():
            z = '13'
        elif int(z) < 0 or 17 < int(z):
            z = '13'

        if ll[0] == longitude_input_box.background_text or \
                ll[1] == latitude_input_box.background_text:
            ll = ['37.530887', '55.703118']
        else:
            check_ll = float(ll[0]), float(ll[1])
            if check_ll[0] < -180 or 180 < check_ll[0] or \
                    check_ll[1] < -86 or 86 < check_ll[1]:
                ll = ['37.530887', '55.703118']

        current_params['z'] = z
        current_params['ll'] = ll
        scale_input_box.text = current_params['z']
        longitude_input_box.text = current_params['ll'][0]
        latitude_input_box.text = current_params['ll'][1]

    response_content = make_request(**current_params)
    with open("map.png", 'wb') as map_file:
        map_file.write(response_content)

    mapa = Map(map_sprite, (125, 75))

    while 1:
        screen.fill(LIGHT_LIGHT_GREY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            scale_input_box.motion(event)
            current_params['z'] = scale_input_box.text
            longitude_input_box.motion(event)
            latitude_input_box.motion(event)
            current_params['ll'] = [longitude_input_box.text, latitude_input_box.text]

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_UP]:
                    if event.key == pygame.K_LEFT:
                        if longitude_input_box.text != longitude_input_box.background_text:
                            longitude_input_box.text = str(float(longitude_input_box.text) - 1)
                            cycle(longitude_input_box)
                    elif event.key == pygame.K_DOWN:
                        if latitude_input_box.text != latitude_input_box.background_text:
                            if float(latitude_input_box.text) - 1 > -86:
                                latitude_input_box.text = str(float(latitude_input_box.text) - 1)
                    elif event.key == pygame.K_RIGHT:
                        if longitude_input_box.text != longitude_input_box.background_text:
                            longitude_input_box.text = str(float(longitude_input_box.text) + 1)
                            cycle(longitude_input_box)
                    elif event.key == pygame.K_UP:
                        if latitude_input_box.text != latitude_input_box.background_text:
                            if float(latitude_input_box.text) + 1 < 86:
                                latitude_input_box.text = str(float(latitude_input_box.text) + 1)
                    current_params['ll'] = [longitude_input_box.text, latitude_input_box.text]
                    change_map(current_params, mapa)
                elif event.key in [pygame.K_PAGEUP, pygame.K_w, pygame.K_PAGEDOWN, pygame.K_s]:
                    if event.key == pygame.K_PAGEUP or event.key == pygame.K_w:
                        if scale_input_box.text != scale_input_box.background_text:
                            if float(scale_input_box.text) + 1 <= 17:
                                scale_input_box.text = str(int(scale_input_box.text) + 1)
                    elif event.key == pygame.K_PAGEDOWN or event.key == pygame.K_s:
                        if scale_input_box.text != scale_input_box.background_text:
                            if float(scale_input_box.text) - 1 >= 0:
                                scale_input_box.text = str(int(scale_input_box.text) - 1)
                    current_params['z'] = scale_input_box.text
                    change_map(current_params, mapa)

        drawer.draw_map(mapa)

        get_drawn()
        dict_motions = get_buttons_motions()
        if dict_motions["search"]:
            make_correct()
            change_map(current_params, mapa)
        if dict_motions["layer"]:
            current_params['mode'] += 1
            current_params['mode'] %= 3
            make_correct()
            change_map(current_params, mapa)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
