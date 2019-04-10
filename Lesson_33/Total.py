import os
import sys
import pygame
import requests

map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
             "ll": "37.617635,55.755814",
             "spn": "0.5,0.5",
             "l": "map"
             }

try:
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print("Ошибка выполнения запроса")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
except:
    print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
    sys.exit(1)


map_file = "map.png"
try:
    with open(map_file, "wb") as file:
        file.write(response.content)
except IOError as ex:
    print("Ошибка записи временного файла:", ex)
    sys.exit(2)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass

pygame.quit()
os.remove(map_file)
