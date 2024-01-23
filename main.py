import pygame
import sys
import os
import math

cur_level = 0
levels = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt', 'level5.txt']

FPS = 70
STEP = 3
VOLUME = 0.15
BULLET_DAMAGE = 3
GUN_STORE = 19
BULLET_SPEED = 3
DEATH = False
reload = 0
player_hp = 20
HEAL_VISIBLE = False
heal_x = None
heal_y = None
pygame.init()
all_sprites = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
heal_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
hitbar_rect = (10, 30)
is_reload = False
run = True
move_ym = False
move_xm = False
move_xp = False
move_yp = False
font = pygame.font.SysFont('Courier New CYR', 40)
paused_text = font.render('Нажмите SPACE для продолжения игры\n\n   Нажмите CAPS для выхода'
                          ' из игры', True, (255, 255, 255))
death_text = font.render('Нажмите 1 для перезапуска игры\n\n   Нажмите 2 для выхода'
                         ' из игры', True, (255, 255, 255))
size = width, height = 1940, 1100
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load('fonovaya_musick .wav')
pygame.mixer.music.play(-1)
recharge = pygame.mixer.Sound('recharge.wav')
shoot_sound = pygame.mixer.Sound('shoot_sound.wav')
damage_sound = pygame.mixer.Sound('damage_sound.wav')
pygame.mixer.music.set_volume(VOLUME)
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


tile_images = {'wall': load_image('wall_2.png'),
                                   'empty': load_image('floor_1.png'),
                                   'street': load_image('street.png'),
                                   'enemy': load_image('enemy_1.png'),
                                   'HEAL': load_image('HEAL.png')
               }
player_image = load_image('main_hero_1.png')
tile_width, tile_height = 50, 50
cur = load_image('cur.png')
gun_image = load_image('gun_image.png')
hitbar_image = load_image('hitbar.png')


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


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(66, 1308) and event.pos[1] in range(241, 449):
                    choose_style()
                    return
                if event.pos[0] in range(66, 1308) and event.pos[1] in range(505, 711):
                    settings()
                    return
                if event.pos[0] in range(60, 1308) and event.pos[1] in range(761, 969):
                    terminate()
        cur_rect = cur.get_rect()
        cur_rect.center = pygame.mouse.get_pos()
        screen.blit(fon, (0, 0))
        screen.blit(cur, cur_rect)
        clock.tick(FPS)
        pygame.display.flip()

def choose_style():
    global tile_images, player_image
    fon = pygame.transform.scale(load_image('choose_style.png'), (width, height))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(130, 1670) and event.pos[1] in range(250, 400):
                    tile_images = {'wall': load_image('wall_1.png'),
                                   'empty': load_image('floor_1.png'),
                                   'street': load_image('street.png'),
                                   'enemy': load_image('enemy_1.png'),
                                   'HEAL': load_image('HEAL.png')}
                    player_image = load_image('main_hero_1.png')
                    return
                if event.pos[0] in range(130, 1670) and event.pos[1] in range(480, 630):
                    tile_images = {'wall': load_image('wall_2.png'),
                                   'empty': load_image('floor_2.png'),
                                   'street': load_image('street.png'),
                                   'enemy': load_image('enemy_2.png'),
                                   'HEAL': load_image('HEAL.png')}
                    player_image = load_image('main_hero_2.png')
                    return
                if event.pos[0] in range(130, 1670) and event.pos[1] in range(730, 870):
                    tile_images = {'wall': load_image('wall_3.png'),
                                   'empty': load_image('floor_3.png'),
                                   'street': load_image('street.png'),
                                   'enemy': load_image('enemy_3.png'),
                                   'HEAL': load_image('HEAL.png')}
                    player_image = load_image('main_hero_3.png')
                    return
        cur_rect = cur.get_rect()
        cur_rect.center = pygame.mouse.get_pos()
        screen.blit(fon, (0, 0))
        screen.blit(cur, cur_rect)
        clock.tick(FPS)
        pygame.display.flip()


def settings():
    fon = pygame.transform.scale(load_image('settings.png'), (width, height))
    global VOLUME
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(73, 153) and event.pos[1] in range(36, 136):
                    return start_screen()
                if event.pos[0] in range(384, 461) and event.pos[1] in range(350, 441):
                    VOLUME += 0.15
                    pygame.mixer.music.set_volume(VOLUME)
                if (event.pos[0] in range(529, 602) and event.pos[1]
                        in range(347, 437) and VOLUME >= 0.01):
                    VOLUME -= 0.15
                    pygame.mixer.music.set_volume(VOLUME)
        cur_rect = cur.get_rect()
        cur_rect.center = pygame.mouse.get_pos()
        screen.blit(fon, (0, 0))
        screen.blit(cur, cur_rect)
        pygame.display.flip()


def terminate():
    sys.exit()

start_screen()

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            paused = False
        if keys[pygame.K_CAPSLOCK]:
            terminate()
        pygame.display.update()
        screen.blit(paused_text, (800, 200))
        clock.tick(FPS)


def death_menu():
    global DEATH, cur_level, player_hp, GUN_STORE, player, level_x, level_y, all_sprites, move_yp, move_xp, move_xm, \
        move_ym, HEAL_VISIBLE
    death = True
    while death:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        DEATH = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            death = False
            player_hp = 20
            GUN_STORE = 19
            cur_level = 0
            HEAL_VISIBLE = False
            all_sprites.empty()
            tile_group.empty()
            player_group.empty()
            bullet_group.empty()
            enemy_group.empty()
            wall_group.empty()
            portal_group.empty()
            move_yp, move_xp, move_xm, move_ym = False, False, False, False
            cur_level = 0
            player, level_x, level_y = generate_level(load_level(levels[cur_level]))
            DEATH = False
        if keys[pygame.K_2]:
            terminate()
        pygame.display.update()
        screen.blit(death_text, (800, 200))
        clock.tick(FPS)
    run_game()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, object):
        if object.__class__.__name__ == 'Bullet':
            object.pos = (object.pos[0] + self.dx, object.pos[1] + self.dy)
        else:
            object.rect = object.rect.move(self.dx, self.dy)

    def update(self, target):
        self.dx = width // 2 - target.rect.x - target.rect.w // 2
        self.dy = height // 2 - target.rect.y - target.rect.h // 2


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_group, all_sprites)
        if tile_type == 'wall':
            self.add(wall_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y


class HEAL(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(heal_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y

    def update(self):
        global player_hp
        if pygame.sprite.spritecollideany(self, player_group):
            player_hp += 3
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.image = tile_images[tile_type]
        self.hp = 21
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.orig_image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y
        self.reload = 0

    def update(self):
        global HEAL_VISIBLE, heal_x, heal_y
        if player_group.sprites()[0].rect.x in range(self.rect.x - 450, self.rect.x + 450) and \
                player_group.sprites()[0].rect.y in range(self.rect.y - 450, self.rect.y + 450):
            x, y = (player_group.sprites()[0].rect.center[0],
                    player_group.sprites()[0].rect.center[1])
            x1, y1 = x - self.rect.x, y - self.rect.y
            angle = (180 / math.pi) * -math.atan2(y1, x1)
            self.image = pygame.transform.rotate(self.orig_image, int(angle))
            self.rect = self.image.get_rect(center=self.rect.center)
            self.reload += clock.get_time()
            if self.reload >= 770:
                Bullet(self.rect.center[0], self.rect.center[1], player_group.sprites()[0].rect.center[0],
                       player_group.sprites()[0].rect.center[1], False)
                self.reload = 0
                shoot_sound.play()
        if (pygame.sprite.spritecollideany(self, bullet_group) and
                pygame.sprite.spritecollideany(self, bullet_group).player_bullet):
            pygame.sprite.spritecollideany(self, bullet_group).kill()
            self.hp -= BULLET_DAMAGE
            if self.hp <= 0:
                if self.pos_x == heal_x and heal_y == self.pos_y:
                    HEAL_VISIBLE = True
                self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        self.image = player_image
        self.x, self.y = pos_x, pos_y
        self.orig_image = player_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = tile_width * pos_x + 13, tile_height * pos_y + 5

    def update(self):
        global player_hp
        x, y = pygame.mouse.get_pos()
        x1, y1 = x - self.rect.x, y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(y1, x1)
        self.image = pygame.transform.rotate(self.orig_image, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        if (pygame.sprite.spritecollideany(self, bullet_group) and
                not pygame.sprite.spritecollideany(self, bullet_group).player_bullet):
            pygame.sprite.spritecollideany(self, bullet_group).kill()
            player_hp -= BULLET_DAMAGE
            damage_sound.play()
            if player_hp <= 0:
                death_menu()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mx, my, player_bullet):
        super().__init__(all_sprites, bullet_group)
        self.pos = (x, y)
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        self.image = load_image('bullet.png')
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.rotate(self.image, angle)
        self.player_bullet = player_bullet

    def update(self):
        if pygame.sprite.spritecollideany(self, wall_group):
            self.kill()
        self.pos = (self.pos[0] + self.dir[0] * BULLET_SPEED,
                    self.pos[1] + self.dir[1] * BULLET_SPEED)
        self.rect = self.image.get_rect(center=self.pos)

def generate_level(level):
    global heal_x, heal_y
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '-':
                Tile('street', x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                Enemy('enemy', x, y)
            elif level[y][x] == '+':
                Tile('empty', x, y)
                Enemy('enemy', x, y)
                HEAL('HEAL', x, y)
                heal_x = x
                heal_y = y
            else:
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


cur_level = 0
player, level_x, level_y = generate_level(load_level(levels[cur_level]))
camera = Camera()


def run_game():
    global run, GUN_STORE, is_reload, reload, move_yp, move_xp, \
        move_xm, move_ym, player, cur_level
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or DEATH:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if GUN_STORE > 0:
                    Bullet(player.rect.center[0] + 6, player.rect.center[1] + 6, pygame.mouse.get_pos()[0],
                           pygame.mouse.get_pos()[1], True)
                    shoot_sound.play()
                    GUN_STORE -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
                if event.key == pygame.K_s:
                    move_yp = True
                if event.key == pygame.K_a:
                    move_xm = True
                if event.key == pygame.K_d:
                    move_xp = True
                if event.key == pygame.K_w:
                    move_ym = True
                if event.key == pygame.K_r:
                    if reload == 0:
                        recharge.play()
                        is_reload = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    move_yp = False
                if event.key == pygame.K_a:
                    move_xm = False
                if event.key == pygame.K_d:
                    move_xp = False
                if event.key == pygame.K_w:
                    move_ym = False
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
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        patrons = font.render(f'{GUN_STORE}/{19}', True, (255, 255, 255))
        if len(enemy_group.sprites()) == 0:
            cur_level = (cur_level + 1) % len(levels)
            GUN_STORE = 19
            all_sprites.empty()
            tile_group.empty()
            player_group.empty()
            bullet_group.empty()
            enemy_group.empty()
            wall_group.empty()
            portal_group.empty()
            move_yp, move_xp, move_xm, move_ym = False, False, False, False
            player, level_x, level_y = generate_level(load_level(levels[cur_level]))
            run_game()
        if is_reload:
            reload += clock.get_time()
        if reload >= 700:
            GUN_STORE = 19
            reload = 0
            is_reload = False
        bullet_group.update()
        tile_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        if HEAL_VISIBLE:
            heal_group.draw(screen)
        bullet_group.draw(screen)
        cur_rect = cur.get_rect()
        cur_rect.center = pygame.mouse.get_pos()
        screen.blit(hitbar_image, hitbar_rect)
        screen.blit(gun_image, (30, 880))
        screen.blit(patrons, (60, 1000))
        pygame.draw.rect(screen, 'grey', (60, 34, 192, 23))
        pygame.draw.rect(screen, 'red', (60, 34, 192 * (player_hp / 20), 23))
        pygame.draw.rect(screen, 'black', (60, 34, 194, 25), 3)
        screen.blit(cur, cur_rect)
        clock.tick(FPS)
        portal_group.update()
        all_sprites.update()
        pygame.display.flip()


run_game()