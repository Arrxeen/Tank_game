import pygame
from random import *

WIDTH = 480
HEIGHT = 600
FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)
TILE =(35)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()
objects = []
bullets = []


class Map(pygame.sprite.Sprite):
    def __init__(self,px,py,size):
        objects.append(self)
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 2

    def draw(self):
        pygame.draw.rect(screen, 'green', self.rect)
        pygame.draw.rect(screen, 'gray20', self.rect, 2)
        if self.hp == 1:
            pygame.draw.rect(screen, "red", self.rect)
            pygame.draw.rect(screen, 'gray20', self.rect, 5)
    
    def damage(self, value):
        self.hp -= value
        if self.hp <= 0: objects.remove(self)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('0.png')
        self.rect = self.image.get_rect()
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
            self.image = pygame.image.load(f"l{self.i}.png")
            self.i += 1
            if self.i == 6:
                self.i = 1
        elif self.direction == 'right':
            self.image = pygame.image.load(f"r{self.i}.png")
            self.i += 1
            if self.i == 6:
                self.i = 1
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
        Bullet(self, self.rect.centerx, self.rect.centery, self.bulletDamage , self.direction)


class Bullet:
    def __init__(self, parent, px, py,  damage, diraction):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.damage = damage
        self.direction = diraction
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

    def draw(self):
        pygame.draw.circle(screen, 'yellow', (self.px, self.py), 2)
        self.speedx = 0
        self.speedy1 = 0


for _ in range(50):
    while True:
        x = randint(0, WIDTH // TILE - 1) * TILE
        y = randint(0, HEIGHT // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect): fined = True
        if not fined: break
    Map(x, y, TILE) 


all_sprites = pygame.sprite.Group()
player = Player()
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
    for bullet in bullets: bullet.update()
    for obj in objects: obj.update()

    for bullet in bullets: bullet.draw()
    for obj in objects: obj.draw()
    all_sprites.draw(screen)
    pygame.display.flip()
    screen.fill('black')
pygame.quit()