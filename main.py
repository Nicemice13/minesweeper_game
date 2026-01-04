import pygame
import random

# Размеры поля в ячейках
BOARD_WIDTH = 20
BOARD_HEIGHT = 15
MINES_COUNT = 30

# Размер одной ячейки в пикселях
CELL_SIZE = 30

# Рассчитываем размер окна в пикселях
SCREEN_WIDTH = BOARD_WIDTH * CELL_SIZE
SCREEN_HEIGHT = BOARD_HEIGHT * CELL_SIZE

# Цвета (в формате RGB)
BG_COLOR = (192, 192, 192) # Серый
LINE_COLOR = (128, 128, 128) # Темно-серый

class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_open = False
        self.is_flagged = False
        self.adjacent_mines = 0

class GameBoard:
    def __init__(self, width, height, mines_count):
        self.width = width
        self.height = height
        self.mines_count = mines_count
        self.game_over = False

        # Создает поле (двумерная матрица), заполняет объектами Cell.
        self.board = [[Cell() for _ in range(width)] for _ in range(height)]

        self.place_mines()
        self.calculate_adjacent_mines()

    def place_mines(self):
        #Создает список всех возможных координат в формате (строка, столбец).
        all_coords = [(r, c) for r in range(self.height) for c in range(self.width)]

        # Выбирает случайные координаты для расположения мин.
        mine_coords = random.sample(all_coords, self.mines_count)

        # В ячейках по этим координатам расставляет мины.
        for r, c in mine_coords:
            self.board[r][c].is_mine = True

    def calculate_adjacent_mines(self):
        # Перебирает все ячейки на поле.
        for r in range(self.height):
            for c in range(self.width):
                # Если ячейка содержит мину, пропускаем ее.
                if self.board[r][c].is_mine:
                    continue
                mine_count = 0
                # Перебираем соседние ячейки.
                for dr in [-1, 0, 1]: # Смещение по строке
                    for dc in [-1, 0, 1]: # Смещение по столбцу
                       # Пропускаем текущую ячейку.
                        if dr == 0 and dc == 0:
                            continue
                        # Вычисляем координаты соседних ячеек.
                        nr, nc = r + dr, c + dc

                        # Проверяет, что не вышли за границы поля.
                        if 0 <= nr < self.height and 0 <= nc < self.width:
                            # Если соседняя ячейка содержит мину, увеличивает счетчик.
                            if self.board[nr][nc].is_mine:
                                mine_count += 1
                # Записывает количество мин в ячейке.
                self.board[r][c].adjacent_mines = mine_count

    def open_cell(self, r, c):
        # Получаем ячейку, по которой кликнули
        cell = self.board[r][c]

        # Нельзя открыть уже открытую ячейку или ячейку с флагом
        if cell.is_open or cell.is_flagged:
            return

        cell.is_open = True
        # Если это была мина - игра окончена
        if cell.is_mine:
            self.game_over = True
            return # Сразу выходим

        # Магия "Сапёра": если ячейка пустая, открываем соседей
        if cell.adjacent_mines == 0 and not cell.is_mine:
            # Проходим по всем 8 соседям
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue

                    nr, nc = r + dr, c + dc

                    # Убеждаемся, что сосед в пределах поля
                    if 0 <= nr < self.height and 0 <= nc < self.width:
                        # И рекурсивно вызываем эту же функцию для соседа!
                        self.open_cell(nr, nc)

    def toggle_flag(self, r, c):
        cell = self.board[r][c]
        # Флаг можно ставить только на закрытые ячейки
        if not cell.is_open:
            cell.is_flagged = not cell.is_flagged

def draw_board(board_obj):
    # Заливаем весь экран фоновым цветом
    screen.fill(BG_COLOR)
    for r in range(board_obj.height):
        for c in range(board_obj.width):
            cell = board_obj.board[r][c]
            x = c * CELL_SIZE
            y = r * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            # Рисуем контур ячейки
            pygame.draw.rect(screen, LINE_COLOR, rect, 1)

            # Если ячейка открыта
            if cell.is_open:
                if cell.is_mine:
                    # Рисуем мину (красный круг)
                    pygame.draw.circle(screen, (255, 0, 0), rect.center, CELL_SIZE // 3)
                elif cell.adjacent_mines > 0:
                    # Рисуем цифру
                    text = font.render(str(cell.adjacent_mines), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
            # Если стоит флаг
            elif cell.is_flagged:
                # Рисуем флаг (желтый треугольник)
                pygame.draw.polygon(screen, (255, 255, 0),
                                    [(rect.left + 5, rect.top + 5),
                                     (rect.right - 5, rect.centery),
                                     (rect.left + 5, rect.bottom - 5)])


# --- Инициализация Pygame и создание окна ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Сапёр")

# Добавляем создание шрифта
font = pygame.font.SysFont("Arial", CELL_SIZE // 2)

# --- Создание игрового поля ---
game_board = GameBoard(BOARD_WIDTH, BOARD_HEIGHT, MINES_COUNT)

# --- Главный игровой цикл ---
running = True
while running:
    # 1. Обработка событий
    for event in pygame.event.get():
        # Если пользователь нажал на "крестик"
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_board.game_over:

            # Получаем координаты клика в пикселях
            mouse_x, mouse_y = pygame.mouse.get_pos()
            clicked_col = mouse_x // CELL_SIZE
            clicked_row = mouse_y // CELL_SIZE

            # Если левая кнопка мыши
            if event.button == 1:
                game_board.open_cell(clicked_row, clicked_col)

            # Если правая кнопка мыши
            elif event.button == 3:
                game_board.toggle_flag(clicked_row, clicked_col)

            # Превращаем пиксели в координаты ячейки
            clicked_col = mouse_x // CELL_SIZE
            clicked_row = mouse_y // CELL_SIZE

            # Выводим результат в терминал для проверки
            print(f"Клик по ячейке: строка {clicked_row}, столбец {clicked_col}")

    # 2. Отрисовка
    draw_board(game_board)

    # Если игра окончена, показываем сообщение
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