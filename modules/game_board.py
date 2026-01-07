import random
import pygame

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
                # Если ячейка содержит мину, пропускает ее.
                if self.board[r][c].is_mine:
                    continue
                mine_count = 0
                # Перебирает соседние ячейки.
                for dr in [-1, 0, 1]: # Смещение по строке
                    for dc in [-1, 0, 1]: # Смещение по столбцу
                       # Пропускает текущую ячейку.
                        if dr == 0 and dc == 0:
                            continue
                        # Вычисляет координаты соседних ячеек.
                        nr, nc = r + dr, c + dc

                        # Проверяет, что не вышли за границы поля.
                        if 0 <= nr < self.height and 0 <= nc < self.width:
                            # Если соседняя ячейка содержит мину, увеличивает счетчик.
                            if self.board[nr][nc].is_mine:
                                mine_count += 1
                # Записывает количество мин в ячейке.
                self.board[r][c].adjacent_mines = mine_count

    def open_cell(self, r, c):
        # Получает ячейку, по которой кликнули
        cell = self.board[r][c]

        # Нельзя открыть уже открытую ячейку или ячейку с флагом
        if cell.is_open or cell.is_flagged:
            return

        cell.is_open = True
        # Если это была мина - игра окончена
        if cell.is_mine:
            self.game_over = True
            return # Сразу выходим

        # Если ячейка пустая, открывает соседей
        if cell.adjacent_mines == 0 and not cell.is_mine:
            # Проходит по всем 8 соседям
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue

                    nr, nc = r + dr, c + dc

                    # Проверяет, что сосед в пределах поля
                    if 0 <= nr < self.height and 0 <= nc < self.width:
                        # И рекурсивно вызывает эту же функцию для соседа!
                        self.open_cell(nr, nc)

    def toggle_flag(self, r, c):
        cell = self.board[r][c]
        # Флаг можно ставить только на закрытые ячейки
        if not cell.is_open:
            cell.is_flagged = not cell.is_flagged

def draw_board(board_obj, screen, font, CELL_SIZE, BG_COLOR, LINE_COLOR):
    # Заливает весь экран фоновым цветом
    screen.fill(BG_COLOR)
    for r in range(board_obj.height):
        for c in range(board_obj.width):
            cell = board_obj.board[r][c]
            x = c * CELL_SIZE
            y = r * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            # Рисует контур ячейки
            pygame.draw.rect(screen, LINE_COLOR, rect, 1)

            # Если ячейка открыта
            if cell.is_open:
                if cell.is_mine:
                    # Рисует мину (красный круг)
                    pygame.draw.circle(screen, (255, 0, 0), rect.center, CELL_SIZE // 3)
                elif cell.adjacent_mines > 0:
                    # Рисует цифру
                    text = font.render(str(cell.adjacent_mines), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
            # Если стоит флаг
            elif cell.is_flagged:
                # Рисует флаг (желтый треугольник)
                pygame.draw.polygon(screen, (255, 255, 0),
                                    [(rect.left + 5, rect.top + 5),
                                     (rect.right - 5, rect.centery),
                                     (rect.left + 5, rect.bottom - 5)])
