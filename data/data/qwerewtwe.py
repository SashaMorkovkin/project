import pygame
import sys
import os

FPS = 60

pygame.init()
size = width, height = 550, 500
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Not found: {fullname}')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_it((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')
tile_width, tile_height = 50, 50


def start_screen():
    text = ['ЗАСТАВКА', '', 'ПРАВИЛА ИГРЫ', 'ЕСЛИ В ПРАВИЛАХ НЕСКОЛЬКО СТРОК, ТО ЭТО ПЕЧАЛЬНО']
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    coord_y = 50
    for line in text:
        draw_line = font.render(line, True, pygame.Color('red'))
        line_rect = draw_line.get_rect()
        coord_y += 20
        line_rect.top = coord_y
        line_rect.x = 20
        coord_y += line_rect.height
        screen.blit(draw_line, line_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(file):
    file = f'data/{file}'
    with open(file, 'r') as f:
        map_level = list(map(str.strip, f.readlines()))
    max_width = max(map(len, map_level))
    return list(map(lambda x: x.ljust(max_width, '.'), map_level))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            else:
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x + 13, tile_height * pos_y + 5


def terminate():
    sys.exit()


all_sprites = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
start_screen()
run = True
player, level_x, level_y = generate_level(load_level('level1.txt'))
step = 50
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.rect.y -= step
            if event.key == pygame.K_s:
                player.rect.y += step
            if event.key == pygame.K_a:
                player.rect.x -= step
            if event.key == pygame.K_d:
                player.rect.x += step
    screen.fill('black')
    tile_group.draw(screen)
    player_group.draw(screen)
    clock.tick(FPS)
    all_sprites.update()
    pygame.display.flip()
