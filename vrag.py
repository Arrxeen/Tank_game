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