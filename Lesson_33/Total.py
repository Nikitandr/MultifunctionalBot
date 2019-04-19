import os
import sys
import pygame
import requests

running = True
map_api_server = "http://static-maps.yandex.ru/1.x/"
spn_x, spn_y = "1.1", "1.1"
ll_x, ll_y = "37.617635", "55.755814"
spn = [spn_x, spn_y]
map_params = {
             "ll": (ll_x + "," + ll_y),
             "spn": ','.join(spn),
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

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if float(spn_x) < 10:
                    if float(spn_x) < 3:
                        spn_x = str(float(spn_x) + 0.5)
                        spn_y = str(float(spn_y) + 0.5)
                    elif float(spn_x) >= 3:
                        spn_x = str(float(spn_x) + 1)
                        spn_y = str(float(spn_y) + 1)
            elif event.key == pygame.K_PAGEDOWN:
                if float(spn_x) > 0.2:
                    if float(spn_x) < 3:
                        spn_x = str(float(spn_x) - 0.5)
                        spn_y = str(float(spn_y) - 0.5)
                    if float(spn_x) >= 3:
                        spn_x = str(float(spn_x) - 1)
                        spn_y = str(float(spn_y) - 1)
            elif event.key == pygame.K_UP:
                        ll_y = str(float(ll_y) + 0.100000)
            elif event.key == pygame.K_DOWN:
                        ll_y = str(float(ll_y) - 0.100000)
            elif event.key == pygame.K_LEFT:
                        ll_x = str(float(ll_x) - 0.100000)
            elif event.key == pygame.K_RIGHT:
                        ll_x = str(float(ll_x) + 0.100000)

            spn = [spn_x, spn_y]
            ll = ll_x + "," + ll_y
            map_params = {
                          "ll": ll,
                          "spn": ','.join(spn),
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

            try:
                with open(map_file, "wb") as file:
                    file.write(response.content)
            except IOError as ex:
                print("Ошибка записи временного файла:", ex)
                sys.exit(2)

            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()

pygame.quit()
os.remove(map_file)
