import pygame
import sys
from levels import *
pygame.init()

screen = pygame.display.set_mode((470, 610))
pygame.display.set_caption("Гра Перегони")



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

#відображення меню
def show_menu():
    screen.fill(BLACK)
    title_rect = draw_text("Меню Гри", font, WHITE, screen, 150, 100)
    play_1_rect = draw_text("Легкий рівень", small_font, WHITE, screen, 150, 200)
    play_2_rect = draw_text("Середній рівень", small_font, WHITE, screen, 150, 250)
    play_3_rect = draw_text("Важкий рівень", small_font, WHITE, screen, 150, 300)
    settings_rect = draw_text("Налаштування", small_font, WHITE, screen, 150, 400)
    exit_game_rect = draw_text("Вийти з гри", small_font, WHITE, screen, 150, 450)

    pygame.display.flip()
    return play_1_rect, play_2_rect, play_3_rect, settings_rect, exit_game_rect

def show_settings():
    screen.fill(BLACK)
    title_rect = draw_text("Налаштування", font, WHITE, screen, 300, 100)
    back_rect = draw_text("Натисніть 'B' для повернення", small_font, WHITE, screen, 300, 200)

    pygame.display.flip()
    return back_rect

# Основний цикл гри
def main():
    while True:
        play_1_rect, play_2_rect, play_3_rect, settings_rect, exit_game_rect = show_menu()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_1_rect.collidepoint(event.pos):
                        print("Запуск легкого рівня")
                        return a1
                    elif play_2_rect.collidepoint(event.pos):
                        print("Запуск середнього рівня")
                        return a2
                    elif play_3_rect.collidepoint(event.pos):
                        print("Запуск важкого рівня")
                        return a3
                    elif settings_rect.collidepoint(event.pos):
                        while True:
                            back_rect = show_settings()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.MOUSEBUTTONDOWN and back_rect.collidepoint(event.pos):
                                    break
                    elif exit_game_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()
