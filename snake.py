import random
from collections import namedtuple
from enum import Enum

import numpy as np
import pygame

pygame.init()
# retro pixel font — use bundled arial or fallback to system monospace
try:
    font = pygame.font.Font("arial.ttf", 20)
except FileNotFoundError:
    font = pygame.font.SysFont("couriernew", 20, bold=True)

# smaller font for HUD label
try:
    font_small = pygame.font.Font("arial.ttf", 14)
except FileNotFoundError:
    font_small = pygame.font.SysFont("couriernew", 14)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x, y")

# ── retro pixel art palette ──────────────────────────────────────────
BG_COLOR = (15, 15, 26)  # deep dark navy
GRID_COLOR = (30, 30, 48)  # subtle grid lines
SNAKE_HEAD = (80, 220, 100)  # bright green head
SNAKE_HEAD_INNER = (130, 255, 140)  # lighter green head accent
SNAKE_BODY = (34, 139, 34)  # forest green body
SNAKE_BODY_INNER = (50, 180, 50)  # lighter green body accent
SNAKE_TAIL_DIM = (20, 90, 20)  # dimmer tail end
SCORE_TEXT = (240, 200, 80)  # warm amber/gold text
HUD_BG = (10, 10, 20, 180)  # semi-transparent dark panel
BORDER_COLOR = (60, 60, 90)  # subtle border around play area

# food color cycling palette — vibrant retro colors
FOOD_COLORS = [
    (255, 60, 60),  # red
    (255, 140, 30),  # orange
    (255, 220, 50),  # yellow
    (255, 80, 180),  # magenta/pink
    (50, 220, 255),  # cyan
    (130, 80, 255),  # purple
    (80, 255, 120),  # lime green
]

BLOCK_SIZE = 20
SPEED = 40


class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("🐍 Wiener Snake AI")
        self.clock = pygame.time.Clock()
        # pre-render the static grid surface for performance
        self._grid_surface = self._create_grid_surface()
        # HUD surface (semi-transparent background bar)
        self._hud_surface = pygame.Surface((self.w, 32), pygame.SRCALPHA)
        self._hud_surface.fill(HUD_BG)
        self.reset()

    def _create_grid_surface(self):
        """Pre-render the background grid to avoid redrawing every frame."""
        surface = pygame.Surface((self.w, self.h))
        surface.fill(BG_COLOR)
        for x in range(0, self.w, BLOCK_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, self.h))
        for y in range(0, self.h, BLOCK_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (0, y), (self.w, y))
        # draw border around play area
        pygame.draw.rect(surface, BORDER_COLOR, (0, 0, self.w, self.h), 2)
        return surface

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y),
        ]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if (
            pt.x > self.w - BLOCK_SIZE
            or pt.x < 0
            or pt.y > self.h - BLOCK_SIZE
            or pt.y < 0
        ):
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        # ── background with pre-rendered grid ──
        self.display.blit(self._grid_surface, (0, 0))

        # ── draw snake body with gradient from head to tail ──
        snake_len = len(self.snake)
        for i, pt in enumerate(self.snake):
            if i == 0:
                # HEAD — distinct bright color
                outer_color = SNAKE_HEAD
                inner_color = SNAKE_HEAD_INNER
            else:
                # BODY — gradient fading toward tail
                t = i / max(snake_len - 1, 1)  # 0.0 at head, 1.0 at tail
                outer_color = (
                    int(SNAKE_BODY[0] + (SNAKE_TAIL_DIM[0] - SNAKE_BODY[0]) * t),
                    int(SNAKE_BODY[1] + (SNAKE_TAIL_DIM[1] - SNAKE_BODY[1]) * t),
                    int(SNAKE_BODY[2] + (SNAKE_TAIL_DIM[2] - SNAKE_BODY[2]) * t),
                )
                inner_color = (
                    int(
                        SNAKE_BODY_INNER[0]
                        + (SNAKE_TAIL_DIM[0] - SNAKE_BODY_INNER[0]) * t
                    ),
                    int(
                        SNAKE_BODY_INNER[1]
                        + (SNAKE_TAIL_DIM[1] - SNAKE_BODY_INNER[1]) * t
                    ),
                    int(
                        SNAKE_BODY_INNER[2]
                        + (SNAKE_TAIL_DIM[2] - SNAKE_BODY_INNER[2]) * t
                    ),
                )

            # outer block
            pygame.draw.rect(
                self.display,
                outer_color,
                pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE),
            )
            # inner accent block (pixel art highlight)
            pygame.draw.rect(
                self.display,
                inner_color,
                pygame.Rect(pt.x + 4, pt.y + 4, 12, 12),
            )

            # head gets a small "eye" dot to distinguish direction
            if i == 0:
                eye_color = (20, 20, 30)
                ex, ey = pt.x + 12, pt.y + 6  # default: facing right
                if self.direction == Direction.LEFT:
                    ex, ey = pt.x + 6, pt.y + 6
                elif self.direction == Direction.UP:
                    ex, ey = pt.x + 12, pt.y + 6
                elif self.direction == Direction.DOWN:
                    ex, ey = pt.x + 6, pt.y + 12
                pygame.draw.rect(self.display, eye_color, pygame.Rect(ex, ey, 4, 4))

        # ── draw food with cycling colors ──
        food_color_idx = (self.frame_iteration // 6) % len(FOOD_COLORS)
        food_color = FOOD_COLORS[food_color_idx]

        # outer food block
        pygame.draw.rect(
            self.display,
            food_color,
            pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE),
        )
        # inner food highlight (brighter center for pixel art pop)
        highlight = (
            min(food_color[0] + 60, 255),
            min(food_color[1] + 60, 255),
            min(food_color[2] + 60, 255),
        )
        pygame.draw.rect(
            self.display,
            highlight,
            pygame.Rect(self.food.x + 4, self.food.y + 4, 12, 12),
        )

        # small sparkle dot on food corner (pixel art detail)
        sparkle = (255, 255, 255)
        pygame.draw.rect(
            self.display, sparkle, pygame.Rect(self.food.x + 2, self.food.y + 2, 2, 2)
        )

        # ── styled HUD bar ──
        self.display.blit(self._hud_surface, (0, 0))
        # score label
        label = font_small.render("SCORE", True, (140, 140, 170))
        self.display.blit(label, (10, 2))
        # score value
        score_text = font.render(str(self.score), True, SCORE_TEXT)
        self.display.blit(score_text, (68, 4))

        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
