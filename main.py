import pygame
import sys
import os
import math

new_level = 'level2.txt'

FPS = 1000
STEP = 3
pygame.init()
size = width, height = 1700, 1000
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load('fonovaya_musick .wav')
pygame.mixer.music.play()
sound2 = pygame.mixer.Sound('shoot_sound.wav')
sound2.set_volume(0.1)
pygame.mixer.music.set_volume(0.05)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)


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


tile_images = {'wall': load_image('floor_1.png'), 'empty': load_image('wall_1.png'), 'street': load_image('street.png'),
               'left': load_image('left.png'), 'right': load_image('right.png'), 'down': load_image('down.png')}
player_image = load_image('main_hero_1.png')
tile_width, tile_height = 50, 50


def start_screen():
    text = ['МАРИО', '', 'Правила игры:', '1. ИГРАТЬ']
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    coord_y = 50
    for line in text:
        draw_line = font.render(line, 1, 'black', 'white')
        line_rect = draw_line.get_rect()
        coord_y += 10
        line_rect.top = coord_y
        line_rect.x = width // 2 - line_rect.width // 2
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
    try:
        file = f'data/{file}'
        with open(file, 'r') as f:
            map_level = list(map(str.strip, f.readlines()))
        max_width = max(map(len, map_level))
        pygame.mouse.set_visible(False)
        return list(map(lambda x: x.ljust(max_width, '.'), map_level))
    except FileNotFoundError:
        terminate()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '-':
                Tile('street', x, y)
            elif level[y][x] == '<':
                Tile('right', x, y)
            elif level[y][x] == '>':
                Tile('left', x, y)
            elif level[y][x] == '+':
                Tile('down', x, y)
            else:
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, object):
        object.rect = object.rect.move(self.dx, self.dy)

    def update(self, target):
        self.dx = width // 2 - target.rect.x - target.rect.w // 2
        self.dy = height // 2 - target.rect.y - target.rect.h // 2


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_group, all_sprites)
        if (tile_type == 'wall' or tile_type == 'street' or tile_type == 'left'
                or tile_type == 'right' or tile_type == 'down'):
            self.add(wall_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        self.image = player_image
        self.x, self.y = pos_x, pos_y
        self.orig_image = player_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = tile_width * pos_x + 13, tile_height * pos_y + 5


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, bullet_group)
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        self.bullet = load_image('bullet.png')
        self.rect = self.bullet.get_rect()
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = 4

    def update(self):
        self.pos = (self.pos[0] + self.dir[0] * self.speed,
                    self.pos[1] + self.dir[1] * self.speed)
        if pygame.sprite.spritecollideany(self, wall_group):
            self.kill()

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center=self.pos)
        surf.blit(self.bullet, bullet_rect)


def terminate():
    sys.exit()


all_sprites = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
bullets = []
cur = load_image('cur.png')
start_screen()
run = True
player, level_x, level_y = generate_level(load_level(new_level))
camera = Camera()
move_ym = False
move_xm = False
move_xp = False
move_yp = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bullets.append(Bullet(player.rect.x + 7, player.rect.y + 20))
            sound2.play()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                move_yp = True
            if event.key == pygame.K_a:
                move_xm = True
            if event.key == pygame.K_d:
                move_xp = True
            if event.key == pygame.K_w:
                move_ym = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                move_yp = False
            if event.key == pygame.K_a:
                move_xm = False
            if event.key == pygame.K_d:
                move_xp = False
            if event.key == pygame.K_w:
                move_ym = False
        if event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            x1, y1 = x - player.rect.x, y - player.rect.y
            angle = (180 / math.pi) * -math.atan2(y1, x1)
            player.image = pygame.transform.rotate(player.orig_image, int(angle))
            player.rect = player.image.get_rect(center=player.rect.center)
    if move_yp:
        player.rect.y += STEP
        if (pygame.sprite.spritecollideany(player, wall_group) or
                player.rect.y + player.rect.height > height):
            player.rect.y -= STEP
    if move_xp:
        player.rect.x += STEP
        if (pygame.sprite.spritecollideany(player, wall_group) or
                player.rect.x + player.rect.width > width):
            player.rect.x -= STEP
    if move_ym:
        player.rect.y -= STEP
        if pygame.sprite.spritecollideany(player, wall_group) or player.rect.y < 0:
            player.rect.y += STEP
    if move_xm:
        player.rect.x -= STEP
        if pygame.sprite.spritecollideany(player, wall_group) or player.rect.x < 0:
            player.rect.x += STEP
    for bullet in bullets[:]:
        bullet.update()
        if not screen.get_rect().collidepoint(bullet.pos):
            bullets.remove(bullet)
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    all_sprites.draw(screen)
    wall_group.draw(screen)
    tile_group.draw(screen)
    wall_group.draw(screen)
    player_group.draw(screen)
    cur_rect = cur.get_rect()
    cur_rect.center = pygame.mouse.get_pos()
    for bullet in bullets:
        bullet.draw(screen)
    screen.blit(cur, cur_rect)
    pygame.time.delay(7)
    all_sprites.update()
    pygame.display.flip()
