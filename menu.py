import pygame
import sys
from pathlib import Path
from levels import *
pygame.init()

BASE_SIZE = (470, 610)
screen = pygame.display.set_mode(BASE_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Tank Racing")
canvas = pygame.Surface(BASE_SIZE)
window_size = BASE_SIZE
pygame.mixer.init()

BASE_DIR = Path(__file__).resolve().parent

def resource_path(relative_path):
    return str(BASE_DIR / relative_path)



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

def render_text(text, font, color):
    return font.render(text, True, color)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect

def scaled_mouse_pos(pos):
    width, height = window_size
    scale = min(width / BASE_SIZE[0], height / BASE_SIZE[1])
    offset_x = (width - BASE_SIZE[0] * scale) / 2
    offset_y = (height - BASE_SIZE[1] * scale) / 2
    return (
        int((pos[0] - offset_x) / scale),
        int((pos[1] - offset_y) / scale),
    )

def render_canvas():
    width, height = window_size
    scale = min(width / BASE_SIZE[0], height / BASE_SIZE[1])
    scaled_size = (max(1, int(BASE_SIZE[0] * scale)), max(1, int(BASE_SIZE[1] * scale)))
    scaled = pygame.transform.smoothscale(canvas, scaled_size)
    screen.fill(BLACK)
    screen.blit(scaled, ((width - scaled_size[0]) // 2, (height - scaled_size[1]) // 2))
    pygame.display.flip()

#відображення меню
def show_menu():
    global window_size
    canvas.fill(BLACK)
    draw_text("Game Menu", font, WHITE, canvas, 150, 100)
    play_1_rect = draw_text("Easy Level", small_font, WHITE, canvas, 150, 200)
    play_2_rect = draw_text("Medium Level", small_font, WHITE, canvas, 150, 250)
    play_3_rect = draw_text("Hard Level", small_font, WHITE, canvas, 150, 300)
    settings_rect = draw_text("Settings", small_font, WHITE, canvas, 150, 400)
    exit_game_rect = draw_text("Exit Game", small_font, WHITE, canvas, 150, 450)
    render_canvas()
    return play_1_rect, play_2_rect, play_3_rect, settings_rect, exit_game_rect

volume = 0.5

def show_settings():
    global volume, window_size, screen
    running = True
    while running:
        canvas.fill(BLACK)

        draw_text("Settings", font, WHITE, canvas, 20, 20)

        draw_text("Volume", small_font, WHITE, canvas, 20, 100)
        pygame.draw.rect(canvas, GRAY, (150, 100, 200, 30))
        pygame.draw.rect(canvas, WHITE, (150 + int(volume * 200), 100, 10, 30))

        back_rect = draw_text("Back to Menu", font, WHITE, canvas, 20, 200)

        render_canvas()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                window_size = (event.w, event.h)
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = scaled_mouse_pos(event.pos)
                if back_rect.collidepoint(mouse_pos):
                    running = False
                if 150 <= mouse_pos[0] <= 350 and 100 <= mouse_pos[1] <= 130:
                    volume = max(0.0, min(1.0, (mouse_pos[0] - 150) / 200))
                    pygame.mixer.music.set_volume(volume)
    
    show_menu()



# Основний цикл гри
def main():
    global window_size, screen
    while True:
        play_1_rect, play_2_rect, play_3_rect, settings_rect, exit_game_rect = show_menu()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    window_size = (event.w, event.h)
                    pygame.display.set_mode(window_size, pygame.RESIZABLE)
                    show_menu()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = scaled_mouse_pos(event.pos)
                    if play_1_rect.collidepoint(mouse_pos):
                        print("Starting easy level")
                        return a1
                    elif play_2_rect.collidepoint(mouse_pos):
                        print("Starting medium level")
                        return a2
                    elif play_3_rect.collidepoint(mouse_pos):
                        print("Starting hard level")
                        return a3
                    elif settings_rect.collidepoint(mouse_pos):
                        show_settings()
                    elif exit_game_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()
