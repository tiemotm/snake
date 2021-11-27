import random
import time
import pygame
from enum import Enum

# CONSTANTS
# SCREEN
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 10

# GRID
GRID_SIZE = 20


# Color Enum holding rgb values
class Color(Enum):
    GREEN = (0, 128, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


# Direction Enum holding screen axis directions as values
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    # Return opposite direction
    def opposite(self):
        if self is Direction.UP:
            return Direction.DOWN
        elif self is Direction.DOWN:
            return Direction.UP
        elif self is Direction.LEFT:
            return Direction.RIGHT
        elif self is Direction.RIGHT:
            return Direction.LEFT


# If values empty initialize green snake in the middle of the screen
# with random initial direction
class Snake:
    def __init__(
            self,
            x=(SCREEN_WIDTH / 2),
            y=(SCREEN_HEIGHT / 2),
            length=1,
            color=Color.GREEN,
            direction=random.choice(list(Direction))
    ):
        self.positions = [(x, y)]
        self.length = length
        self.direction = direction
        self.color = color

    # Return position of head
    def get_head_position(self):
        return self.positions[0]

    # change to given direction if it isn't the opposite one
    def turn(self, direction):
        if direction is not self.direction.opposite():
            self.direction = direction

    # check for collisions (border or snake itself)
    def check_collision(self):
        x, y = self.get_head_position()

        if len(self.positions) > 2 and self.get_head_position() in self.positions[2:]:
            return True
        elif x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            return True

        return False

    def move(self):
        head_pos = self.get_head_position()
        x, y = self.direction.value

        # New head position depending on direction
        # add % SCREEN_WIDTH to enable moving trough border
        new_head_pos = (
            (head_pos[0] + (x * GRID_SIZE)),
            (head_pos[1] + (y * GRID_SIZE))
        )

        # insert new head
        self.positions.insert(0, new_head_pos)
        print(self.positions)

        # pop last element if there are more elements than the length
        if len(self.positions) > self.length:
            self.positions.pop()
            print(self.positions)

        # Check for collisions, return True for a valid move with no collisions
        return not self.check_collision()

    def draw(self, screen):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.color.value, r)
            pygame.draw.rect(screen, (93, 216, 228), r, 1)


# If values empty initialize red food randomly on the screen
class Food:
    def __init__(
            self,
            x=random.randrange(0, SCREEN_WIDTH, GRID_SIZE),
            y=random.randrange(0, SCREEN_HEIGHT, GRID_SIZE),
            color=Color.RED
    ):
        self.position = (x, y)
        self.color = color

    # Set new random direction
    def randomize(self):
        x = random.randrange(0, SCREEN_WIDTH, GRID_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT, GRID_SIZE)

        self.position = (x, y)

    def draw(self, screen):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color.value, r)


def handle_events(snake):
    # Allow only one press per loop
    pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        # Snake controls
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w) and pressed is False:
                snake.turn(Direction.UP)
                pressed = True
            if event.key in (pygame.K_DOWN, pygame.K_s) and pressed is False:
                snake.turn(Direction.DOWN)
                pressed = True
            if event.key in (pygame.K_RIGHT, pygame.K_d) and pressed is False:
                snake.turn(Direction.RIGHT)
                pressed = True
            if event.key in (pygame.K_LEFT, pygame.K_a) and pressed is False:
                snake.turn(Direction.LEFT)
                pressed = True


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    text_font = pygame.font.SysFont("monospace", 16)

    pygame.display.set_caption("Snake Game")

    snake = Snake()
    food = Food()
    score = 0

    game_over = False

    while not game_over:
        clock.tick(FPS)

        handle_events(snake)

        # Move snake and check if valid move, game over if not
        game_over = not snake.move()

        # Black screen
        screen.fill(Color.BLACK.value)

        # Draw snake and food on top
        snake.draw(screen)
        food.draw(screen)

        # Check if snake has eaten food
        if food.position == snake.get_head_position():
            score += 1
            snake.length += 1
            # set new location for food
            food.randomize()

        # Draw scoreboard
        score_text = text_font.render("Score {0}".format(score), 1, Color.WHITE.value)
        screen.blit(score_text, (10, 10))

        pygame.display.update()

    # Game Over Text in center of screen
    title_font = pygame.font.SysFont("monospace", 28)
    game_over_text = title_font.render("Game Over you scored {0}".format(score), 10, Color.RED.value)
    center_game_over_text = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(game_over_text, center_game_over_text)
    pygame.display.update()

    # Wait 5 seconds and quit
    time.sleep(5)
    pygame.quit()


main()
