import pygame
from modules import GameBoard, draw_board, BOARD_WIDTH, BOARD_HEIGHT, MINES_COUNT, CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, LINE_COLOR

#  Инициализация Pygame и создание окна
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Сапёр")

# Создание шрифта
font = pygame.font.SysFont("Arial", CELL_SIZE // 2)

# Создание игрового поля
game_board = GameBoard(BOARD_WIDTH, BOARD_HEIGHT, MINES_COUNT)

#  Главный игровой цикл
running = True
while running:
    # 1. Обработка событий
    for event in pygame.event.get():
        # Если пользователь нажал на "крестик"
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_board.game_over:

            # Получение координаты клика в пикселях
            mouse_x, mouse_y = pygame.mouse.get_pos()
            clicked_col = mouse_x // CELL_SIZE
            clicked_row = mouse_y // CELL_SIZE

            # Если левая кнопка мыши
            if event.button == 1:
                game_board.open_cell(clicked_row, clicked_col)

            # Если правая кнопка мыши
            elif event.button == 3:
                game_board.toggle_flag(clicked_row, clicked_col)

            # Изменение пикселей в координаты ячейки
            clicked_col = mouse_x // CELL_SIZE
            clicked_row = mouse_y // CELL_SIZE

            # Вывод результата в терминал для проверки
            print(f"Клик по ячейке: строка {clicked_row}, столбец {clicked_col}")

    # 2. Отрисовка
    draw_board(game_board, screen, font, CELL_SIZE, BG_COLOR, LINE_COLOR)

    # Если игра окончена, вывод сообщение
    if game_board.game_over:
        # Полупрозрачный черный фон
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        # Текст
        text = font.render("Вы проиграли!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

    # 3. Обновление экрана
    pygame.display.flip()

# Корректное завершение работы
pygame.quit()