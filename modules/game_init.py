import pygame

# --- Главный игровой цикл ---
running = True
while running:
    # 1. Обработка событий
    for event in pygame.event.get():
        # Если пользователь нажал на "крестик"
        if event.type == pygame.QUIT:
