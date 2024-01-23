import pygame
import sys
import os
import math
import pygame_gui
import threading

new_level = 'level1.txt'
levels = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt']

FPS = 70
STEP = 3
VOLUME = 0.15
BULLET_DAMAGE = 3
GUN_STORE = 19
BULLET_SPEED = 3
DEATH = False
reload = 0
player_hp = 20
pygame.init()
all_sprites = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
animation_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
hitbar_rect = (10, 30)
is_reload = True
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


tile_images = {'wall': load_image('wall_1.png'), 'empty': load_image('floor_1.png'), 'street': load_image('street.png'),
               'left': load_image('left.png'), 'right': load_image('right.png'), 'down': load_image('down.png'),
               'enemy': load_image('enemy_2.png'), 'portal': load_image('портал.png')}
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
                    VOLUME += 0.05
                    pygame.mixer.music.set_volume(VOLUME)
                if event.pos[0] in range(529, 602) and event.pos[1] in range(347, 437) and VOLUME >= 0.01:
                    VOLUME -= 0.05
                    pygame.mixer.music.set_volume(VOLUME)
        cur_rect = cur.get_rect()
        cur_rect.center = pygame.mouse.get_pos()
        screen.blit(fon, (0, 0))
        screen.blit(cur, cur_rect)
        pygame.display.flip()


def terminate():
    sys.exit()


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
    global DEATH, new_level, player_hp, GUN_STORE
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
            new_level = 'level1.txt'
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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, animation_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_group, all_sprites)
        if tile_type == 'wall':
            self.add(wall_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y


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
        if player_group.sprites()[0].rect.x in range(self.rect.x - 300, self.rect.x + 300) and \
                player_group.sprites()[0].rect.y in range(self.rect.y - 300, self.rect.y + 300):
            x, y = player_group.sprites()[0].rect.center[0], player_group.sprites()[0].rect.center[1]
            x1, y1 = x - self.rect.x, y - self.rect.y
            angle = (180 / math.pi) * -math.atan2(y1, x1)
            self.image = pygame.transform.rotate(self.orig_image, int(angle))
            self.rect = self.image.get_rect(center=self.rect.center)
            self.reload += clock.get_time()
            if (pygame.sprite.spritecollideany(self, bullet_group) and
                    pygame.sprite.spritecollideany(self, bullet_group).player_bullet):
                pygame.sprite.spritecollideany(self, bullet_group).kill()
                self.hp -= BULLET_DAMAGE
                if self.hp <= 0:
                    self.kill()
                    AnimatedSprite(load_image("animation_enemy.jpg"), 8, 2, self.pos_x, self.pos_y)
                    print('enemy_killed')
                if self.reload >= 170:
                    Bullet(self.rect.center[0], self.rect.center[1], player_group.sprites()[0].rect.center[0],
                           player_group.sprites()[0].rect.center[1], False)
                    self.reload = 0
                    shoot_sound.play()

    def shoot(self):
        Bullet(self.rect.center[0], self.rect.center[1], player_group.sprites()[0].rect.center[0],
               player_group.sprites()[0].rect.center[1], False)
        shoot_sound.play()
        threading.Timer(1.0, self.shoot).start()


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
            elif level[y][x] == '+':
                Tile('empty', x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                Enemy('enemy', x, y)
            else:
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


if not DEATH:
    player, level_x, level_y = generate_level(load_level(new_level))
camera = Camera()


def run_game():
    global run, GUN_STORE, is_reload, reload, move_yp, move_xp, move_xm, move_ym, new_level, player
    start_screen()
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
                else:
                    if is_reload:
                        recharge.play()
                        is_reload = False
                    reload += clock.get_time()
                    if reload >= 60:
                        GUN_STORE = 19
                        reload = 0
                        is_reload = True
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
            new_level = 'level2.txt'
            player, level_x, level_y = generate_level(load_level(new_level))
            run = False
            run_game()
        bullet_group.update()
        tile_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        bullet_group.draw(screen)
        portal_group.draw(screen)
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
        animation_group.update()
        pygame.display.flip()


run_game()