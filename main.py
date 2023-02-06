import requests


cords = '37.620070,55.753630'
scale = '1'
z = '13'
size = '450,450'
ll = cords


def change_mode(mode):
    request = requests.get('https://static-maps.yandex.ru/1.x/',
                           params={
                               'l': mode,
                               'scale': scale,
                               'll': ll,
                               'size': size,
                               'z': z,
                           })
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(request.content)


change_mode('sat,skl')
