import pygame
import random
import math
from pathlib import Path
from levels import *
from menu import *


# висота і ширина підрахована по розміру блоків. її не міняти
WIDTH = 720
HEIGHT = 540
FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)
TILE = (35)

BASE_DIR = Path(__file__).resolve().parent

def resource_path(relative_path):
    return str(BASE_DIR / relative_path)

pygame.init()
window_size = (WIDTH, HEIGHT)
display = pygame.display.set_mode(window_size, pygame.RESIZABLE)
screen = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Tanks")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
objects = []
bullets = []
enemy = []
tenk = []
tile_size = 36  # Rozmir
game_map = main()

def render_game():
    scale = min(window_size[0] / WIDTH, window_size[1] / HEIGHT)
    scaled_size = (
        max(1, int(WIDTH * scale)),
        max(1, int(HEIGHT * scale)),
    )
    scaled = pygame.transform.smoothscale(screen, scaled_size)
    display.fill(BLACK)
    display.blit(
        scaled,
        ((window_size[0] - scaled_size[0]) // 2,
         (window_size[1] - scaled_size[1]) // 2),
    )
    pygame.display.flip()

class Brick(pygame.sprite.Sprite):
    def __init__(self, row_index, col_index, tile_size):
        objects.append(self)
        self.rect = pygame.Rect(row_index * tile_size, col_index * tile_size, tile_size, tile_size)
        self.hp = 2
        self.image = pygame.image.load(resource_path('images/block_brick.png'))
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
            if self in objects:
                objects.remove(self)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, col_index, row_index, tile_size):
        enemy.append(self)
        pygame.sprite.Sprite.__init__(self)
        self.base_image = pygame.image.load(resource_path('images/tank5.png'))
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (col_index * tile_size, row_index * tile_size)
        self.hp = 2
        self.damage = 1
        self.direction = random.randint(1, 4)
        self.change_direction_counter = 0
        self.random_move_counter = random.randint(25, 70)
        self.pause_counter = random.randint(0, 20)
        self.speed = random.choice((1, 1, 1))
        self.shot_counter = 0  
        self.shot_interval = random.randint(24, 36)

    def cell_for_position(self, x, y):
        return (max(0, min(WIDTH // tile_size - 1, x // tile_size)),
                max(0, min(HEIGHT // tile_size - 1, y // tile_size)))

    def cell_is_blocked(self, col, row):
        cell_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
        for obj in objects:
            if hasattr(obj, "rect") and obj is not self and obj.rect.colliderect(cell_rect):
                return True
        return False

    def find_next_direction(self):
        start = self.cell_for_position(self.rect.centerx, self.rect.centery)
        target = self.cell_for_position(player.rect.centerx, player.rect.centery)

        if start == target:
            return self.direction

        queue = [start]
        visited = {start: None}
        found = False
        neighbors = ((0, -1), (1, 0), (0, 1), (-1, 0))

        while queue and not found:
            col, row = queue.pop(0)
            if (col, row) == target:
                found = True
                break
            for dc, dr in neighbors:
                next_cell = (col + dc, row + dr)
                next_col, next_row = next_cell
                if (next_col < 0 or next_col >= WIDTH // tile_size or
                        next_row < 0 or next_row >= HEIGHT // tile_size):
                    continue
                if next_cell in visited:
                    continue
                if self.cell_is_blocked(next_col, next_row):
                    continue
                visited[next_cell] = (col, row)
                queue.append(next_cell)

        if not found:
            return self.direction

        step = target
        while visited[step] != start:
            previous = visited.get(step)
            if previous is None:
                return self.direction
            step = previous

        dc = step[0] - start[0]
        dr = step[1] - start[1]
        if dc > 0:
            return 2
        if dc < 0:
            return 1
        if dr > 0:
            return 4
        if dr < 0:
            return 3
        return self.direction

    def move_towards_player(self):
        self.direction = self.find_next_direction()

    def visible_target_point(self):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 400:
            return None

        horizontal_visible = player.rect.top <= self.rect.centery <= player.rect.bottom
        vertical_visible = player.rect.left <= self.rect.centerx <= player.rect.right

        if horizontal_visible:
            if dx >= 0:
                direction = 2
            else:
                direction = 1
            target_x = player.rect.left if dx >= 0 else player.rect.right
            target_y = self.rect.centery
        elif vertical_visible:
            if dy >= 0:
                direction = 4
            else:
                direction = 3
            target_x = self.rect.centerx
            target_y = player.rect.top if dy >= 0 else player.rect.bottom
        else:
            return None

        sample_count = max(1, int(distance / 6))
        sight_x = self.rect.centerx
        sight_y = self.rect.centery
        for step in range(1, sample_count):
            ratio = step / sample_count
            if direction in (1, 2):
                sight_x = self.rect.centerx + dx * ratio
                sight_y = self.rect.centery
            else:
                sight_x = self.rect.centerx
                sight_y = self.rect.centery + dy * ratio

            for obj in objects:
                if hasattr(obj, "rect") and obj is not self and obj.rect.collidepoint(sight_x, sight_y):
                    return None

        return target_x, target_y, direction

    def should_shoot(self):
        return self.visible_target_point() is not None

    def update(self):
        oldX, oldY = self.rect.topleft

        if self.pause_counter > 0:
            self.pause_counter -= 1
            self.image = pygame.transform.rotate(self.base_image, {
                1: 90,
                2: -90,
                3: 0,
                4: 180,
            }[self.direction])
            screen.blit(self.image, self.rect)
            return

        self.change_direction_counter += 1
        self.random_move_counter -= 1

        if self.random_move_counter <= 0:
            if random.random() < 0.55:
                self.direction = random.randint(1, 4)
            else:
                self.move_towards_player()
            self.random_move_counter = random.randint(25, 75)
            self.pause_counter = random.randint(0, 12)

        elif self.change_direction_counter >= 12:
            self.move_towards_player()
            self.change_direction_counter = 0

        if self.direction == 1:  
            self.rect.x -= self.speed
        if self.direction == 2:  
            self.rect.x += self.speed
        if self.direction == 3:  
            self.rect.y -= self.speed
        if self.direction == 4:  
            self.rect.y += self.speed

        if self.direction == 1:
            self.image = pygame.transform.rotate(self.base_image, 90)
        elif self.direction == 2:
            self.image = pygame.transform.rotate(self.base_image, -90)
        elif self.direction == 3:
            self.image = self.base_image
        elif self.direction == 4:
            self.image = pygame.transform.rotate(self.base_image, 180)

        
        collision = False
        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                collision = True
                break

        if not collision:
            for other_enemy in enemy:
                if other_enemy is not self and self.rect.colliderect(other_enemy.rect):
                    collision = True
                    break

        if not collision and self.rect.colliderect(player.rect):
            collision = True

        
        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            collision = True

        if collision:
            self.rect.topleft = oldX, oldY
            self.direction = random.randint(1, 4)  

        
        self.shot_counter += 1
        if self.shot_counter >= self.shot_interval:
            self.shoot()
            self.shot_counter = 0
            self.shot_interval = random.randint(24, 36)

        screen.blit(self.image, self.rect)

    def shoot(self):
        target = self.visible_target_point()
        if target is not None:
            target_x, target_y, direction = target
            BulletEnemy(
                self,
                self.rect.centerx,
                self.rect.centery,
                self.damage,
                direction,
                target_x,
                target_y,
            )

    def boom(self, value):
        self.hp -= value
        if self.hp <= 0:
            if self in enemy:
                enemy.remove(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, row_index, col_index):
        pygame.sprite.Sprite.__init__(self)
        tenk.append(self)
        self.images = {
            "": pygame.image.load(resource_path("images/tank4.png")),
            "up": pygame.image.load(resource_path("images/tank4.png")),
            "down": pygame.image.load(resource_path("images/tank4.1.png")),
            "left": pygame.image.load(resource_path("images/tank4.2.png")),
            "right": pygame.image.load(resource_path("images/tank4.3.png")),
        }
        self.image = self.images[""]
        self.rect = self.image.get_rect()
        self.rect.topleft = (col_index * tile_size, row_index * tile_size)
        self.speedx = 0
        self.speedy = 0
        self.direction = ""
        self.i = 1
        self.bulletDamage = 1
        self.hp = 5

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
            self.image = self.images["left"]
        elif self.direction == 'right':
            self.image = self.images["right"]
        elif self.direction == 'down':
            self.image = self.images["down"]
        elif self.direction == 'up':
            self.image = self.images["up"]

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
        if self.direction:
            Bullet(self, self.rect.centerx, self.rect.centery, self.bulletDamage, self.direction)
    
    def kill(self, value):
        self.hp -= value
        if self.hp <= 0:
            if self in tenk:
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
        if self.direction == "":
            if self in bullets:
                bullets.remove(self)
            return

        if self.direction == 'left':
            self.px -= 8
        elif self.direction == 'right':
            self.px += 8
        elif self.direction == 'up':
            self.py -= 8
        elif self.direction == 'down':
            self.py += 8

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            if self in bullets:
                bullets.remove(self)
            return

        for obj in objects:
            if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                obj.damage(self.damage)
                if self in bullets:
                    bullets.remove(self)
                break

        for en in enemy:
            if en.rect.collidepoint(self.px, self.py):
                en.boom(self.damage)
                if self in bullets:
                    bullets.remove(self)
                break

    def draw(self):
        pygame.draw.circle(screen, 'yellow', (self.px, self.py), 2)


class BulletEnemy:
    def __init__(self, parent, px, py, damage, direction, target_x=None, target_y=None):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.damage = damage
        self.direction = direction
        self.speedx = 0
        self.speedy1 = 0
        self.target_x = target_x if target_x is not None else px
        self.target_y = target_y if target_y is not None else py
        
    def update(self):
        if self.direction == 1:
            self.px -= 6
        elif self.direction == 2:
            self.px += 6
        elif self.direction == 3:
            self.py -= 6
        elif self.direction == 4:
            self.py += 6

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            if self in bullets:
                bullets.remove(self)
            return

        for obj in objects:
            if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                obj.damage(self.damage)
                if self in bullets:
                    bullets.remove(self)
                break
        
        for tan in tenk:
            if tan.rect.collidepoint(self.px, self.py):
                tan.kill(self.damage)
                if self in bullets:
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

def show_game_over():
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    title = font.render("Game Over", True, (255, 255, 255))
    hint = small_font.render("Esc - exit game", True, (255, 255, 255))
    overlay.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
    overlay.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
    screen.blit(overlay, (0, 0))
    render_game()


def show_victory():
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 70, 0, 190))
    title = font.render("Victory!", True, (255, 255, 255))
    hint = small_font.render("All enemies destroyed. Esc - exit", True, (255, 255, 255))
    overlay.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
    overlay.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
    screen.blit(overlay, (0, 0))
    render_game()


def show_pause():
    global window_size, display
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    title = font.render("Pause", True, (255, 255, 255))
    hint = small_font.render("Esc - continue", True, (255, 255, 255))
    overlay.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
    overlay.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
    screen.blit(overlay, (0, 0))
    render_game()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.VIDEORESIZE:
                window_size = (event.w, event.h)
                pygame.display.set_mode(window_size, pygame.RESIZABLE)
                render_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return


running = True
paused = False

pygame.mixer.init()
try:
    pygame.mixer.music.load(resource_path("sounds/videoplayback.mp3"))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)
except pygame.error as error:
    print("Could not start music:", error)

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            window_size = (event.w, event.h)
            display = pygame.display.set_mode(window_size, pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            show_pause()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player in tenk:
                player.shot_left()

    if paused:
        continue

    for tank in list(tenk):
        tank.update()

    for bullet in list(bullets):
        bullet.update()

    for en in list(enemy):
        en.update()

    if not enemy and player.hp > 0:
        show_victory()
        victory = True
        while victory:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    victory = False
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    window_size = (event.w, event.h)
                    display = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                    show_victory()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    victory = False
                    running = False

    for bullet in list(bullets):
        bullet.draw()
    for obj in list(objects):
        obj.draw()

    if player.hp <= 0:
        show_game_over()
        game_over = True
        while game_over:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    window_size = (event.w, event.h)
                    display = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                    show_game_over()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_over = False
                    running = False

    all_sprites.draw(screen)
    render_game()
    screen.fill('black')

pygame.quit()
