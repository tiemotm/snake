import random
import time
import pygame
from enum import Enum

# CONSTANTS

# SCREEN
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


SPEED = 10


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

        # pop last element if there are more elements than the length
        if len(self.positions) > self.length:
            self.positions.pop()

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


def check_play_again():
    valid_input = False
    play_again = False

    while not valid_input:
        input_play_again = input("Do you want to play again? y/n\n")

        if input_play_again in ("y", "Y"):
            valid_input = True
            play_again = True
        elif input_play_again in ("n", "N"):
            valid_input = True
            play_again = False
        else:
            print("Wrong input")

    return play_again


class Game:
    def __init__(
            self,
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
            speed=SPEED,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = speed

        pygame.init()

        self.clock = clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")

        # FONTS
        self.TEXT_FONT = pygame.font.SysFont("monospace", 16)
        self.TITLE_FONT = pygame.font.SysFont("monospace", 28)

        self.snake = Snake()
        self.food = Food()
        self.score = 0

        self.game_over = False

    def update_score(self):
        if self.food.position == self.snake.get_head_position():
            self.score += 1
            self.snake.length += 1
            # set new location for food
            self.food.randomize()

    def update_screen(self):
        self.screen.fill(Color.BLACK.value)
        # Draw snake and food on top
        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        # Draw scoreboard
        score_text = self.TEXT_FONT.render("Score {0}".format(self.score), True, Color.WHITE.value)
        self.screen.blit(score_text, (10, 10))

        pygame.display.update()

    def handle_events(self):
        # Allow only one press per loop
        pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Snake controls
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w) and pressed is False:
                    self.snake.turn(Direction.UP)
                    pressed = True
                if event.key in (pygame.K_DOWN, pygame.K_s) and pressed is False:
                    self.snake.turn(Direction.DOWN)
                    pressed = True
                if event.key in (pygame.K_RIGHT, pygame.K_d) and pressed is False:
                    self.snake.turn(Direction.RIGHT)
                    pressed = True
                if event.key in (pygame.K_LEFT, pygame.K_a) and pressed is False:
                    self.snake.turn(Direction.LEFT)
                    pressed = True

    def reset(self):
        self.screen = 0
        self.snake = Snake()
        self.food.randomize()

    def game_end(self):
        print("Game over, you scored ", self.score)
        game_over_text = self.TITLE_FONT.render("Game over, you scored {0}".format(self.score), True, Color.RED.value)
        center_game_over_text = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(game_over_text, center_game_over_text)
        pygame.display.update()

    def game_step(self):
        # Handle user input
        self.handle_events()

        # Move snake and check if it was a valid move
        # If not, game is over
        self.game_over = not self.snake.move()

        # Update score if snake has eaten food
        self.update_score()

        # Fill screen and draw all objects on it
        self.update_screen()
        self.clock.tick(self.speed)

    def start_timer(self, length):
        for i in range(length, 0, -1):
            self.screen.fill(Color.BLACK.value)
            game_over_text = self.TITLE_FONT.render("{0}".format(i), True, Color.RED.value)
            center_game_over_text = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            self.screen.blit(game_over_text, center_game_over_text)
            pygame.display.update()
            time.sleep(1)

    def run(self):
        self.start_timer(3)
        # Game loop
        while True:
            self.game_step()

            if self.game_over:
                self.game_end()

                if check_play_again():
                    self.reset()
                    self.start_timer(3)
                else:
                    break

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
