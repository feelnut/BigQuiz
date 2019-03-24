import pygame
import requests
import sys
import os

# Изменение типов карты происходит через нажатие на правую кнопку мыши
def draw_screen():
    response = None
    map_params = {
        "ll": ','.join([str(sh), str(dol)]),
        "spn": ','.join([str(spn), str(spn)]),
        "l": maps[current_map]
    }
    try:
        map_request = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)
    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    screen.blit(pygame.image.load(map_file), (0, 0))
    os.remove(map_file)


# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))

sh, dol = 61.402554, 55.159897
spn = 0.005
maps = ['map', 'sat', 'skl']
current_map = 0
running = True
pygame.display.flip()
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                spn -= spn / 1.2 if spn >= 0.0001 else 0
            elif event.key == pygame.K_PAGEUP:
                spn += spn / 1.2 if spn <= 15 else 0
            elif event.key == pygame.K_DOWN:
                dol -= spn / 5
            elif event.key == pygame.K_UP:
                dol += spn / 5
            elif event.key == pygame.K_LEFT:
                sh -= spn / 3
            elif event.key == pygame.K_RIGHT:
                sh += spn / 3
            if dol >= 180:
                dol -= 360
            elif dol <= -180:
                dol += 360
            if sh >= 90:
                sh -= 180
            elif sh <= -90:
                sh += 180
        if event.type == pygame.MOUSEBUTTONDOWN\
            and event.button == 1:
            current_map += 1
    draw_screen()
    pygame.display.flip()

pygame.quit()
