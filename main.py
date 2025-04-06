import pygame
import random
import time


pygame.init()


WIDTH, HEIGHT = 600, 600
FPS = 30
CARD_SIZE = 100
GRID_SIZE = 4  # Сітка 4x4
MARGIN = 20  # Проміжок між картами


BACKGROUND_COLOR = (255, 255, 255)
CARD_COLOR = (70, 130, 180)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (95, 158, 160)


font = pygame.font.Font(None, 50)

# Створення екрану
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Казіно на дурака")
clock = pygame.time.Clock()


pygame.mixer.music.load("ref/background_music.mp3")
pygame.mixer.music.play(-1)
# Генерація карт
def generate_cards():
    num_pairs = (GRID_SIZE ** 2) // 2
    cards = list(range(1, num_pairs + 1)) * 2  # Створюємо пари карт
    random.shuffle(cards)  # Перемішуємо карти
    return cards


# Функція для малювання карт
def draw_cards(cards, revealed, matched):
    for i, card in enumerate(cards):
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        x = col * (CARD_SIZE + MARGIN) + MARGIN
        y = row * (CARD_SIZE + MARGIN) + MARGIN

        # Якщо карта відкрито або підібрано, малюємо її значення
        if revealed[i] or matched[i]:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (x, y, CARD_SIZE, CARD_SIZE))
            text = font.render(str(card), True, TEXT_COLOR)
            screen.blit(text, (x + CARD_SIZE // 3, y + CARD_SIZE // 3))
        else:
            pygame.draw.rect(screen, CARD_COLOR, (x, y, CARD_SIZE, CARD_SIZE))


# Основна функція гри
def main():
    # Створення карт та станів
    cards = generate_cards()
    revealed = [False] * len(cards)
    matched = [False] * len(cards)
    selected = []
    moves = 0
    game_over = False

    while not game_over:
        screen.fill(BACKGROUND_COLOR)

        # Малюємо всі карти
        draw_cards(cards, revealed, matched)

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    x, y = pygame.mouse.get_pos()
                    row = (y - MARGIN) // (CARD_SIZE + MARGIN)
                    col = (x - MARGIN) // (CARD_SIZE + MARGIN)
                    index = row * GRID_SIZE + col

                    # Якщо карта ще не відкрита і не підібрана, вибираємо її
                    if not revealed[index] and not matched[index]:
                        revealed[index] = True
                        selected.append(index)
                        moves += 1

                    # Якщо вибрано 2 карти
                    if len(selected) == 2:
                        # Перевірка на відповідність
                        i1, i2 = selected
                        if cards[i1] == cards[i2]:
                            matched[i1] = matched[i2] = True
                        else:
                            pygame.time.delay(500)  # Час на перегляд карт
                            revealed[i1] = revealed[i2] = False

                        selected = []

        # Перевірка завершення гри
        if all(matched):
            game_over = True
            print(f"Ви виграли за {moves} ходів!")

        # Оновлення екрану
        pygame.display.flip()

        # Обмежуємо FPS
        clock.tick(FPS)

    pygame.quit()


# Запуск гри
if __name__ == "__main__":
    main()

