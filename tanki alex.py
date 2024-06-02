import pygame
import random
from levels import *
from menu import *


# висота і ширина підрахована по розміру блоків. її не міняти
WIDTH = 720
HEIGHT = 540
FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)
TILE = (35)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game!")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
objects = []
bullets = []
enemy = []
tenk = []
tile_size = 36  # Rozmir
game_map = main()

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
        self.shot_counter = 0  # Counter for shooting
        self.shot_interval = 20  # Shooting interval in frames

    def move_towards_player(self):
        player_x, player_y = player.rect.topleft
        enemy_x, enemy_y = self.rect.topleft
        if player_x > enemy_x:
            self.direction = 2  # Right
        else:
            self.direction = 1  # Left

        if player_y > enemy_y:
            self.direction = 4  # Down
        else:
            self.direction = 3  # Up
    def should_shoot(self):
        player_x, player_y = player.rect.topleft
        enemy_x, enemy_y = self.rect.topleft
        return player_x == enemy_x or player_y == enemy_y

    def update(self):
        tank_image = pygame.image.load("images/tank5.png")  # Загрузить изображение танка
        player_x, player_y = player.rect.topleft
        enemy_x, enemy_y = self.rect.topleft
        oldX, oldY = self.rect.topleft

        if self.direction == 1:  # left
            self.rect.x -= 2
        if self.direction == 2:  # right
            self.rect.x += 2
        if self.direction == 3:  # up
            self.rect.y -= 2
        if self.direction == 4:  # down
            self.rect.y += 2

        if self.direction == 1:
            self.image = pygame.transform.rotate(tank_image, 90)  # Поворот на 90 градусов по часовой стрелке
        elif self.direction == 2:
            self.image = pygame.transform.rotate(tank_image, -90)  # Поворот на 90 градусов против часовой стрелки
        elif self.direction == 3:
            self.image = tank_image  # Не поворачивать
        elif self.direction == 4:
            self.image = pygame.transform.rotate(tank_image, 180)  # Поворот на 180 градусов


        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY
                self.move_towards_player()  

        # collision detection
        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.rect.topleft = oldX, oldY
            self.move_towards_player()

        # Shoot
        self.shot_counter += 1
        if self.shot_counter >= self.shot_interval:
            if player_x == enemy_x or player_y == enemy_y:
                self.shoot()
            self.shot_counter = 0

        screen.blit(self.image, self.rect)
    

    def shoot(self):
        if self.should_shoot():
            player_dx = player.rect.centerx - self.rect.centerx
            player_dy = player.rect.centery - self.rect.centery
            if abs(player_dx) > abs(player_dy):
                if player_dx > 0:
                    direction = 2  # Right
                else:
                    direction = 1  # Left
            else:
                if player_dy > 0:
                    direction = 4  # Down
                else:
                    direction = 3  # Up

            BulletEnemy(self, self.rect.centerx, self.rect.centery, self.damage, direction)

    def boom(self, value):
        self.hp -= value
        if self.hp <= 0:
            enemy.remove(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, row_index, col_index):
        pygame.sprite.Sprite.__init__(self)
        tenk.append(self)
        self.image = pygame.image.load('images/tank4.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (col_index * tile_size, row_index * tile_size)
        self.speedx = 0
        self.speedy = 0
        self.direction = ""
        self.i = 1
        self.bulletDamage = 1
        self.hp = 3

    def update(self):
        oldX, oldY = self.rect.topleft
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.direction = 'left'
            self.speedx = -2
        if keystate[pygame.K_RIGHT]:
            self.direction = 'right'
            self.speedx = 2
        self.rect.x += self.speedx
        if keystate[pygame.K_DOWN]:
            self.direction = 'down'
            self.speedy = 2
        if keystate[pygame.K_UP]:
            self.direction = 'up'
            self.speedy = -2
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
        screen.blit(self.image, self.rect)

    def shot_left(self):
        Bullet(self, self.rect.centerx, self.rect.centery, self.bulletDamage, self.direction)
    
    def kill(self, value):
        self.hp -= value
        if self.hp <= 0:
            tenk.remove(self)

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


class BulletEnemy:
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

        if self.direction == 0:
            bullets.remove(self)

        if self.direction == 1:
            self.speedx = -8

        if self.direction == 2:
            self.speedx = 8

        self.px += self.speedx
        if self.direction == 3:
            self.speedy1 = -8

        if self.direction == 4:
            self.speedy1 = 8

        self.py += self.speedy1

        for obj in objects:
            if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                obj.damage(self.damage)
                bullets.remove(self)
                break
        
        for tan in tenk:
            if tan.rect.collidepoint(self.px, self.py):
                tan.kill(self.damage)
                bullets.remove(self)

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

running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shot_left()

    for tank in tenk:
        tank.update()

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
