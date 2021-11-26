import time

import pygame
import sys
from enum import Enum, auto

pygame.init()

# CONSTANTS
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT_STYLE = pygame.font.SysFont(None, 50)

pygame.display.set_caption("SnakeAI")


class Color(Enum):
    GREEN = (0, 128, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def opposite(self, opps={
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT
    }):
        return opps[self.value]


class Snake:

    def __init__(self, color=Color.GREEN, direction=Direction.RIGHT):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.direction = direction
        self.color = color
        self.score = 0

    def check_border(self):
        if (self.x >= SCREEN_WIDTH
                or self.x <= 0
                or self.y >= SCREEN_HEIGHT
                or self.y <= 0):
            return True

        return False

    def move(self):
        if self.direction == Direction.UP:
            self.y -= 10
            return
        elif self.direction == Direction.DOWN:
            self.y += 10
            return
        elif self.direction == Direction.RIGHT:
            self.x += 10
            return
        elif self.direction == Direction.LEFT:
            self.x -= 10
            return

    def change_direction(self, direction):
        if direction.value != self.direction.opposite():
            self.direction = direction

    def draw(self):
        pygame.draw.rect(SCREEN, self.color.value, [self.x, self.y, 15, 15])


# class Food():
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#

def message(msg, color):
    mesg = FONT_STYLE.render(msg, True, color)
    SCREEN.blit(mesg, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2])


def main():
    clock = pygame.time.Clock()

    snake = Snake()

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        user_input = pygame.key.get_pressed();

        if user_input[pygame.K_UP] or user_input[pygame.K_w]:
            snake.change_direction(Direction.UP)
        elif user_input[pygame.K_DOWN] or user_input[pygame.K_s]:
            snake.change_direction(Direction.DOWN)
        elif user_input[pygame.K_RIGHT] or user_input[pygame.K_d]:
            snake.change_direction(Direction.RIGHT)
        elif user_input[pygame.K_LEFT] or user_input[pygame.K_a]:
            snake.change_direction(Direction.LEFT)

        snake.move()

        SCREEN.fill(Color.WHITE.value)
        snake.draw()

        game_over = snake.check_border()

        clock.tick(30)
        pygame.display.update()

    message("Game Over", Color.RED.value)
    pygame.display.update()
    time.sleep(3)
    pygame.quit()
    quit()


main()
