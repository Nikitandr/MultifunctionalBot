import pygame
import sys
import os

pygame.init()
FPS = 60
pygame.key.set_repeat(10, 1)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
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
            elif level[y][x] == '*':
                Portal(x, y)
            elif level[y][x] == '%':
                Exit(x, y)
            elif level[y][x] == '@':
                player = Player(x, y)
    return player


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


class Flags(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = flag_image
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        if not pygame.sprite.spritecollideany(self, flags_group):
            self.add(flags_group)


class Portal(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(portal_group, all_sprites)
        self.image = portal_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Exit(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(exit_group, all_sprites)
        self.image = exit_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def start_screen():
    intro_text = ["Подсказки:",
                  "E - поставить метку,",
                  "Будь осторожен с использованием порталов"]

    fon = pygame.transform.scale(load_image('start.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
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


def finish_screen():
    intro_text = ["Спасибо за игру"]

    fon = pygame.transform.scale(load_image('start.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 380
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                terminate()

        pygame.display.flip()


sizes = width, height = 900, 700
tile_width, tile_height = 50, 50
screen, running = pygame.display.set_mode(sizes), True
camera = Camera()

flag_image = pygame.transform.scale(load_image('flag.png'), (25, 25))
portal_image = pygame.transform.scale(load_image('portal.png'), (50, 50))
tile_image = pygame.transform.scale(load_image('wall.png'), (50, 50))
player_image = pygame.transform.scale(load_image('hero.png', -1), (24, 40))
exit_image = pygame.transform.scale(load_image('exit.png'), (50, 50))
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
flags_group = pygame.sprite.Group()
fon_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

player = generate_level(load_level('map1.txt'))
start_screen()

while running:
    screen.fill((255, 255, 255))
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
            elif key == 101:    # E
                Flags()

        if pygame.sprite.spritecollideany(player, portal_group):
            player.rect.x += 200
        if pygame.sprite.spritecollideany(player, exit_group):
            finish_screen()

    for sprite in all_sprites:
        camera.apply(sprite)
    camera.update(player)
    exit_group.draw(screen)
    portal_group.draw(screen)
    flags_group.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()

pygame.quit()
