import pygame
import sys
import os

pygame.init()
FPS = 60
pygame.key.set_repeat(10, 5)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename

    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile(x, y)
            elif level[y][x] == '@':
                player = Player(x, y)
    return player


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


def start_screen():
    intro_text = ["Правила игры:",
                  "Выберись из лабиринта,"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру

        pygame.display.flip()


sizes = width, height = 1000, 1100
tile_width, tile_height = 50, 50
screen, running, player = pygame.display.set_mode(sizes), True, None
tile_images, player_image = pygame.transform.scale(load_image('wall.png'), (50, 50)), load_image('mario.png')
all_sprites, tiles_group, player_group = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()

player = generate_level(load_level('map.txt'))
start_screen()

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == 119:    # W
                player.rect.y -= 1
                if pygame.sprite.spritecollideany(player, tiles_group):
                    player.rect.y += 1
            elif key == 97:    # A
                player.rect.x -= 1
                if pygame.sprite.spritecollideany(player, tiles_group):
                    player.rect.x += 1
            elif key == 115:    # S
                player.rect.y += 1
                if pygame.sprite.spritecollideany(player, tiles_group):
                    player.rect.y -= 1
            elif key == 100:    # D
                player.rect.x += 1
                if pygame.sprite.spritecollideany(player, tiles_group):
                    player.rect.x -= 1

    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()

pygame.quit()
