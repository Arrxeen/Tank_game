import pygame
import random
from levels import *

WIDTH = 470
HEIGHT = 610
FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)
TILE = (35)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
objects = []
bullets = []
enemy = []

game_map = a1

colors = {
    0: (0, 0, 0),       # Чорний колір для нічого
    1: (105, 105, 105), # Сірий колір для стіни
    2: (192, 192, 192), # Світло-сірий колір для хлипкої стіни
    3: (255, 0, 0),     # Червоний колір для ворога
    4: (0, 255, 0)      # Зелений колір для танка
}

tile_size = 36  # Rozmir

def main_menu():
    font = pygame.font.Font(None, 36)
    start_button = pygame.Rect(150, 200, 150, 50)
    quit_button = pygame.Rect(150, 300, 150, 50)

    while True:
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, start_button)
        pygame.draw.rect(screen, RED, quit_button)

        start_text = font.render("Начать", True, BLACK)
        quit_text = font.render("Выйти", True, BLACK)

        screen.blit(start_text, (start_button.x + 37, start_button.y + 15))
        screen.blit(quit_text, (quit_button.x + 37, quit_button.y + 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    return  # Выйти из функции main_menu()
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

        pygame.display.update()
        clock.tick(FPS)

# Вызываем главное меню перед основным циклом игры
main_menu()



class Brick(pygame.sprite.Sprite):
    def __init__(self, row_index, col_index, tile_size):
        objects.append(self)
        self.rect = pygame.Rect(row_index * tile_size, col_index * tile_size, tile_size, tile_size)
        self.hp = 2
        self.image = pygame.image.load('images/block_brick.png')
        self.original_image = self.image.copy()
        screen.blit(self.image, self.rect)
        self.oldx, self.oldy = self.rect.center

    def draw(self):
        if self.hp == 1:
            self.rect.center = (self.oldx, self.oldy)
        screen.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, col_index, row_index, tile_size):
        enemy.append(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/tank5.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (col_index * tile_size, row_index * tile_size)
        self.hp = 2
        self.damage = 1
        self.direction = random.randint(1, 4)
        self.change_direction_counter = 0

    def update(self):
        oldX, oldY = self.rect.topleft

        if self.direction == 1:  # left
            self.rect.x -= 8
        if self.direction == 2:  # right
            self.rect.x += 8
        if self.direction == 3:  # up
            self.rect.y -= 8
        if self.direction == 4:  # down
            self.rect.y += 8

        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY
                self.direction = random.randint(1, 4)  # change direction on collision

        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.rect.topleft = oldX, oldY
            self.direction = random.randint(1, 4)  # change direction on boundary collision

        self.change_direction_counter += 1
        if self.change_direction_counter > 30:  # change direction periodically
            self.direction = random.randint(1, 4)
            self.change_direction_counter = 0

        screen.blit(self.image, self.rect)

    def boom(self, value):
        self.hp -= value
        if self.hp <= 0:
            enemy.remove(self)

class Player(pygame.sprite.Sprite):
    def __init__(self, row_index, col_index):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/tank4.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (col_index * tile_size, row_index * tile_size)
        self.speedx = 0
        self.speedy = 0
        self.direction = ""
        self.i = 1
        self.bulletDamage = 1

    def update(self):
        oldX, oldY = self.rect.topleft
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.direction = 'left'
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.direction = 'right'
            self.speedx = 8
        self.rect.x += self.speedx

        if keystate[pygame.K_DOWN]:
            self.direction = 'down'
            self.speedy = 8
        if keystate[pygame.K_UP]:
            self.direction = 'up'
            self.speedy = -8
        self.rect.y += self.speedy

        if self.direction == 'left':
            self.image = pygame.image.load("images/tank4.2.png")

        elif self.direction == 'right':
            self.image = pygame.image.load("images/tank4.3.png")

        if self.direction == 'up':
            self.image = pygame.image.load("images/tank4.png")

        elif self.direction == 'down':
            self.image = pygame.image.load("images/tank4.1.png")

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

    def shot_left(self):
        Bullet(self, self.rect.centerx, self.rect.centery, self.bulletDamage, self.direction)

class Bullet:
    def __init__(self, parent, px, py, damage, direction):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.damage = damage
        self.direction = direction
        self.speedx = 0
        self.speedy1 = 0

    def update(self):
        self.speedx = 0
        self.speedy1 = 0

        if self.direction == "":
            bullets.remove(self)

        if self.direction == 'left':
            self.speedx = -8

        if self.direction == 'right':
            self.speedx = 8

        self.px += self.speedx
        if self.direction == 'up':
            self.speedy1 = -8

        if self.direction == 'down':
            self.speedy1 = 8

        self.py += self.speedy1

        for obj in objects:
            if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                obj.damage(self.damage)
                bullets.remove(self)
                break

        for en in enemy:
            if en.rect.collidepoint(self.px, self.py):
                en.boom(self.damage)
                bullets.remove(self)
                break

    def draw(self):
        pygame.draw.circle(screen, 'yellow', (self.px, self.py), 2)

for row_index, row in enumerate(game_map):
    for col_index, tile in enumerate(row):
        if tile == 1:
            Brick(col_index, row_index, tile_size)
        if tile == 2:
            pass

        if tile == 3:
            Enemy(col_index, row_index, tile_size)

        if tile == 4:
            player = Player(row_index, col_index)
            all_sprites.add(player)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shot_left()

    all_sprites.update()
    for bullet in bullets:
        bullet.update()

    for en in enemy:
        en.update()

    for bullet in bullets:
        bullet.draw()
    for obj in objects:
        obj.draw()
    all_sprites.draw(screen)
    pygame.display.flip()
    screen.fill('black')
pygame.quit()
