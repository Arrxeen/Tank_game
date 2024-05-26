import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Установка размеров экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Танчики")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)

# Шрифты
font_large = pygame.font.Font(None, 64)
font_small = pygame.font.Font(None, 32)

# Функция отображения текста
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Класс танка
class Tank(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.direction = 'up'

    def update(self, keys, walls):
        old_rect = self.rect.copy()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = 'left'
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = 'right'
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = 'up'
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = 'down'

        # Ограничение перемещения танка границами экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Проверка столкновений со стенами
        if pygame.sprite.spritecollideany(self, walls):
            self.rect = old_rect

# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, color, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = direction

    def update(self, walls):
        if self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed

        # Удаляем пулю, если она выходит за пределы экрана
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # Удаляем пулю при столкновении со стеной
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def update(self, walls):
        old_rect = self.rect.copy()
        if self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed

        # Изменяем направление при столкновении с границами экрана
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = random.choice(['right', 'up', 'down'])
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction = random.choice(['left', 'up', 'down'])
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction = random.choice(['left', 'right', 'down'])
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.direction = random.choice(['left', 'right', 'up'])

        # Проверка столкновений со стенами
        if pygame.sprite.spritecollideany(self, walls):
            self.rect = old_rect
            self.direction = random.choice(['left', 'right', 'up', 'down'])

        # Случайное изменение направления
        if random.randint(0, 100) < 5:
            self.direction = random.choice(['left', 'right', 'up', 'down'])

# Класс стены
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Функция создания полосок стен
def create_wall_strips(num_strips):
    wall_group = pygame.sprite.Group()
    for _ in range(num_strips):
        if random.choice([True, False]):  # Определяем горизонтальная или вертикальная полоска
            # Горизонтальная полоска
            x = random.randint(0, SCREEN_WIDTH - 200)
            y = random.randint(0, SCREEN_HEIGHT - 50)
            for i in range(0, 200, 50):
                wall = Wall(x + i, y, 50, 50)
                wall_group.add(wall)
        else:
            # Вертикальная полоска
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(0, SCREEN_HEIGHT - 200)
            for i in range(0, 200, 50):
                wall = Wall(x, y + i, 50, 50)
                wall_group.add(wall)
    return wall_group

# Функция игры
def game():
    player = Tank(GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    wall_group = create_wall_strips(8)  # Создаем полоски стен

    # Создаем несколько врагов после создания стен
    for _ in range(5):
        enemy = Enemy(BLUE, random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50))
        while pygame.sprite.spritecollideany(enemy, wall_group):
            enemy.rect.topleft = (random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50))
        enemy_group.add(enemy)

    running = True
    while running:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(RED, player.rect.centerx, player.rect.centery, player.direction)
                    bullet_group.add(bullet)

        player.update(keys, wall_group)
        bullet_group.update(wall_group)
        enemy_group.update(wall_group)

        # Проверка попадания пуль во врагов
        for bullet in bullet_group:
            hits = pygame.sprite.spritecollide(bullet, enemy_group, True)
            if hits:
                bullet.kill()

        player_group.draw(screen)
        bullet_group.draw(screen)
        enemy_group.draw(screen)
        wall_group.draw(screen)

        pygame.display.update()

        pygame.time.Clock().tick(60)

# Функция главного меню
def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text("Главное меню", font_large, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text("Нажмите Enter, чтобы начать игру", font_small, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Нажмите Esc, чтобы выйти", font_small, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                   


if __name__ == "__main__":
    main_menu()
