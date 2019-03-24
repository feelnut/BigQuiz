import pygame
import requests
import sys
import os
from spn_tester import get_spn


# Изменение типов карты происходит через нажатие на правую кнопку мыши

# Для поиска: нажать по серому прямоугольнику(перекрасится в белый), после этого
# вводить РУССКИЕ буквы, цифры, запятую(для русской раскладки) без пробелов. Для поиска кнопка
# "Поиск", для отмены поиска "Отмена". Все функции во время поиска отключены.
def draw_screen():
    response = None
    map_params = {
        "ll": ','.join([str(sh), str(dol)]),
        "spn": ','.join([str(spn), str(spn)]),
        "l": maps[current_map],
        "pt": pts
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
    screen.blit(pygame.image.load(map_file), (0, 50))
    font = pygame.font.Font(None, 25)

    pygame.draw.rect(screen, pygame.Color('white'), (250, 2, 100, 44), 2)
    text1 = font.render('Поиск', True, pygame.Color('orange'))
    text1_rect = text1.get_rect()
    text1_rect.center = (300, 23)
    screen.blit(text1, text1_rect)

    pygame.draw.rect(screen, pygame.Color('white'), (355, 2, 100, 44), 2)
    text2 = font.render('Отмена', True, pygame.Color('orange'))
    text2_rect = text2.get_rect()
    text2_rect.center = (405, 23)
    screen.blit(text2, text2_rect)

    pygame.draw.rect(screen, pygame.Color(search_color), (2, 2, 244, 44))
    text = font.render(name, True, pygame.Color('orange'))
    text_rect = text.get_rect()
    text_rect.center = (122, 23)
    screen.blit(text, text_rect)

    os.remove(map_file)


# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 500))

api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
search_api_server = "https://search-maps.yandex.ru/v1/"
sh, dol = 61.402554, 55.159897
spn = 0.005
search_color = 'grey'
maps = ['map', 'sat', 'skl']
current_map = 0
pts = ''
name = '|'
running = True
pygame.display.flip()
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                spn -= spn / 2.2 if spn >= 0.0001 else 0
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
            if dol >= 80:
                dol -= 130
            elif dol <= -50:
                dol += 130
            if sh >= 180:
                sh -= 360
            elif sh <= -180:
                sh += 360
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                current_map += 1
                current_map %= 3
            if event.button == 1:
                x, y = event.pos
                if 2 <= x <= 246 and 2 <= y <= 46:
                    searching = 2
                    search_color = 'white'
                    draw_screen()
                    pygame.display.flip()
                    d = {102: 'А', 44: 'Б', 100: 'В', 117: 'Г', 108: 'Д', 116: 'Е', 96: 'Ё',
                         59: 'Ж', 112: 'З', 98: 'И', 113: 'Й', 114: 'К', 107: 'Л', 118: 'М',
                         121: 'Н', 106: 'О', 103: 'П', 104: 'Р', 99: 'С', 110: 'Т', 101: 'У',
                         97: 'Ф', 91: 'Х', 119: 'Ц', 120: 'Ч', 105: 'Ш', 111: 'Щ', 93: 'Ъ',
                         115: 'Ы', 109: 'Ь', 39: 'Э', 46: 'Ю', 122: 'Я'}
                    while searching == 2:
                        keys = pygame.key.get_pressed()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                searching = 0
                                running = False
                            if event.type == pygame.KEYDOWN:
                                if event.key in list(d.keys()):
                                    name = name[:-1] + d[event.key] + '|'
                                if 48 <= event.key <= 57:
                                    name = name[:-1] + str(event.key - 48) + '|'
                                if event.key == pygame.K_BACKSPACE:
                                    name = name[:-2] + '|'
                                draw_screen()
                                pygame.display.flip()
                            if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and keys[47]:
                                name = name[:-1] + ',|'
                                draw_screen()
                                pygame.display.flip()
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                x, y = event.pos
                                if 250 <= x <= 350 and 2 <= y <= 46:
                                    searching = 1
                                elif 355 <= x <= 455 and 2 <= y <= 46:
                                    searching = 0
                                    name = '|'
                    if searching == 1:
                        search_params = {
                            "apikey": api_key,
                            "text": name[:-1],
                            "lang": "ru_RU",
                            "ll": ','.join([str(sh), str(dol)]),
                            "type": "biz"
                        }
                        response = requests.get(search_api_server, params=search_params)
                        json_response = response.json()
                        organization = json_response["features"][0]
                        coords = organization['properties']['boundedBy']
                        point = organization["geometry"]["coordinates"]
                        sh, dol = point
                        spn = (get_spn(coords)[0] + get_spn(coords)[1]) / 2
                        pts = "{0},{1},pm2vvl".format(point[0], point[1])
                        name = '|'
                    search_color = 'grey'
                    draw_screen()
                    pygame.display.flip()
    draw_screen()
    pygame.display.flip()

pygame.quit()
