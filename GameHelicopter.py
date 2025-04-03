import pygame
import random

# --- Инициализация Pygame ---
pygame.init()
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
COLS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)  # Деревья
RED = (255, 0, 0)  # Огонь
GRAY = (169, 169, 169)  # Пустые клетки
BLUE = (0, 0, 255)  # Вода (реки)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пожарный вертолет")
clock = pygame.time.Clock()

class Cell:
    def __init__(self, x, y, cell_type="empty"):
        self.x, self.y = x, y
        self.cell_type = cell_type
        self.burning = False

        # Деревья могут загореться с вероятностью 2% 
        if self.cell_type == "tree" and random.random() < 0.02:
            self.burning = True

    def draw(self):
        """Рисуем клетку"""
        if not pygame.get_init():
            return
        
        if self.cell_type == "tree":
            color = RED if self.burning else GREEN
        elif self.cell_type == "water":
            color = BLUE
        else:
            color = GRAY
        
        pygame.draw.rect(screen, color, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def spread_fire(self, grid):
        """Распространение огня"""
        if self.burning:
            for dx, dy in [(-1, 0), (1, 0), (0, -1),]:  # Проверяем соседей
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS:
                    neighbor = grid[ny][nx]
                    if neighbor.cell_type == "tree" and not neighbor.burning and random.random() < 0.01:
                        neighbor.burning = True  # 1% шанс загореться 

class Helicopter:
    def __init__(self):
        self.x, self.y = COLS // 2, ROWS // 2
        self.water = 0  # Запас воды
        self.max_water = 5  # Максимальный запас воды
        self.lives = 5  # Жизни вертолета
        self.trees_saved = 0  # Счетчик потушенных деревьев
        self.trees_burned = 0  # Счетчик сгоревших деревьев

    def move(self, dx, dy, grid):
        """Перемещение вертолета и пополнение воды"""
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < COLS and 0 <= new_y < ROWS:
            self.x, self.y = new_x, new_y
            if grid[new_y][new_x].cell_type == "water":
                self.water = self.max_water  # Заполняем бак водой
            elif grid[new_y][new_x].burning:
                self.lives -= 1  # Если вертолет попал в огонь - теряет жизнь
                print(f"Вертолет получил урон! Жизней осталось: {self.lives}")
                if self.lives <= 0:
                    print("Игра окончена! Вертолет сгорел.")
                    pygame.quit()

    def drop_water(self, grid):
        """Тушение огня """
        if self.water > 0:
            for dx in range(-1, 8):  
                for dy in range(-1, 8):  
                    nx, ny = self.x + dx, self.y + dy
                    if 0 <= nx < COLS and 0 <= ny < ROWS:
                        if grid[ny][nx].burning:
                            grid[ny][nx].burning = False  # Огонь потушен
                            self.water -= 1
                            self.trees_saved += 1  # Увеличиваем счётчик потушенных деревьев

    def draw(self):
        """Рисуем вертолет"""
        if pygame.get_init():
            pygame.draw.rect(screen, (255, 255, 0), (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def generate_grid():
    """Создание игрового поля с реками"""
    grid = [[Cell(x, y, "tree" if random.random() < 0.2 else "empty") for x in range(COLS)] for y in range(ROWS)]
    
    # Добавляем реки (вода)
    for _ in range(3):  # Генерируем 3 реки
        start_x = random.randint(0, COLS - 1)
        for y in range(ROWS):
            grid[y][start_x].cell_type = "water"
            if random.random() < 0.5:  # Река может слегка изгибаться
                start_x = max(0, min(COLS - 1, start_x + random.choice([-1, 1])))

    return grid

grid = generate_grid()
heli = Helicopter()
running = True

try:
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Выход из игры")
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: heli.move(-1, 0, grid)
                elif event.key == pygame.K_RIGHT: heli.move(1, 0, grid)
                elif event.key == pygame.K_UP: heli.move(0, -1, grid)
                elif event.key == pygame.K_DOWN: heli.move(0, 1, grid)
                elif event.key == pygame.K_SPACE: heli.drop_water(grid)

        # Обновление пожаров
        for row in grid:
            for cell in row:
                cell.spread_fire(grid)
                if cell.cell_type == "tree" and cell.burning:
                    heli.trees_burned += 1  # Считаем сгоревшие деревья

        if pygame.get_init():
            for row in grid:
                for cell in row:
                    cell.draw()
            heli.draw()

            # Отображаем уровень воды и жизней
            font = pygame.font.Font(None, 36)
            water_text = font.render(f"Вода: {heli.water}/{heli.max_water}", True, (0, 0, 0))
            lives_text = font.render(f"Жизни: {heli.lives}", True, (255, 0, 0))
            saved_text = font.render(f"Потушено: {heli.trees_saved}", True, (0, 0, 0))
            

            screen.blit(water_text, (10, 10))
            screen.blit(lives_text, (10, 40))
            screen.blit(saved_text, (10, 70))
            

            pygame.display.flip()

        clock.tick(10)

except Exception as e:
    print(f"Ошибка: {e}")

finally:
    print("Выход из Pygame")
    pygame.quit()
