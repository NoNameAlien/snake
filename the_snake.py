from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        """Инициализирует базовые атрибуты объекта."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Абстрактный метод для отрисовки объекта на экране."""
        pass


class Apple(GameObject):
    """Класс для объекта 'яблоко'."""

    def __init__(self):
        """Инициализирует атрибуты яблока."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для объекта 'змейка'."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки, добавляя новую голову в начало
        списка positions и удаляя последний элемент.
        """
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        # Новая позиция головы с учетом "зацикленности" поля
        new_x = (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH
        new_y = (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        # Проверка на столкновение с самой собой
        if (new_x, new_y) in self.positions[1:]:
            self.reset()
        else:
            # Добавление новой головы
            self.positions.insert(0, (new_x, new_y))
            # Сохраняем последнюю позицию для затирания
            self.last = self.positions[-1]
            # Удаляем хвост, если длина змейки не увеличилась
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры."""
    # Инициализация PyGame:
    pygame.init()
    # Создание экземпляров классов
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        # Обработка нажатий клавиш
        handle_keys(snake)
        # Обновление направления движения змейки
        snake.update_direction()
        # Движение змейки
        snake.move()
        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
        # Очистка экрана
        screen.fill(BOARD_BACKGROUND_COLOR)
        # Отрисовка змейки и яблока
        snake.draw()
        apple.draw()
        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
