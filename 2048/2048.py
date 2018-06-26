import pygame, random, sys
from pygame.locals import *
from enum import Enum

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 450

GAP = 10

GAME_TOP = 0
GAME_BOTTOM = 450
GAME_LEFT = 0
GAME_RIGHT = 450

TILE_LENGTH = 100
TILE_HALF_LENGTH = 50

SCORE_PER_COLLISION = 20

COLUMN = 4
ROW = 4

BG_COLOR = {
    "Map":     (187, 173, 160),
    "N_BG":    (119, 110, 101),
    "0_BG":    (205, 193, 180),
    "2_BG":    (238, 228, 218),
    "4_BG":    (237, 224, 200),
    "8_BG":    (242, 177, 121),
    "16_BG":   (245, 149, 99),
    "32_BG":   (246, 124, 95),
    "64_BG":   (246, 94,  59),
    "128_BG":  (237, 207, 114),
    "256_BG":  (237, 204, 97),
    "512_BG":  (237, 200, 80),
    "1024_BG": (237, 197, 63),
    "2048_BG": (237, 197, 46)
}


class Direction(Enum):
    Up = 0,
    Down = 1,
    Left = 2,
    Right = 3


class Tile(object):
    def __init__(self, x, y, value):
        self.center_x = x
        self.center_y = y
        self.value = value

    def upgrade_value(self):
        self.value *= 2

    def draw_tile(self, surface, fonts):
        bg_color = BG_COLOR['%d_BG' % self.value]
        pygame.draw.rect(surface, bg_color, (self.center_x - TILE_HALF_LENGTH,
                                             self.center_y - TILE_HALF_LENGTH,
                                             TILE_LENGTH, TILE_LENGTH))

        if self.value >= 2 and self.value <= 8:
            value_text = fonts[0].render(str(self.value), True, BG_COLOR["N_BG"])
            surface.blit(value_text, (self.center_x - 15, self.center_y - 25))

        elif self.value >= 16 and self.value <= 64:
            value_text = fonts[1].render(str(self.value), True, BG_COLOR["N_BG"])
            surface.blit(value_text, (self.center_x - 25, self.center_y - 25))

        elif self.value >= 128 and self.value <= 512:
            value_text = fonts[2].render(str(self.value), True, BG_COLOR["N_BG"])
            surface.blit(value_text, (self.center_x - 35, self.center_y - 25))

        elif self.value >= 1024 and self.value <= 2048:
            value_text = fonts[3].render(str(self.value), True, BG_COLOR["N_BG"])
            surface.blit(value_text, (self.center_x - 45, self.center_y - 25))
        else:
            pass

class Game(object):
    def __init__(self):
        self.score = 0
        self.gameover = False

        self.grid = [[] for i in range(4)]
        self.init_game()

    def init_game(self):
        for c in range(0, COLUMN):
            self.grid[0].append(Tile(0, 0, 0))
            self.grid[1].append(Tile(0, 0, 0))
            self.grid[2].append(Tile(0, 0, 0))
            self.grid[3].append(Tile(0, 0, 0))

        for r in range(0, ROW):
            for c in range(0, COLUMN):
                self.grid[r][c].center_x = GAP * (c + 1) + TILE_HALF_LENGTH * (c * 2 + 1)
                self.grid[r][c].center_y = GAP * (r + 1) + TILE_HALF_LENGTH * (r * 2 + 1)

        self.grid[random.randint(0, COLUMN - 1)][random.randint(0, ROW - 1)].value = 2
        self.gen_next()

    def draw_map(self, surface, fonts):
        pygame.draw.rect(surface, (187, 173, 160), (GAME_LEFT, GAME_TOP, GAME_RIGHT, GAME_BOTTOM))
        for r in range(0, COLUMN):
            for c in range(0, ROW):
                self.grid[c][r].draw_tile(surface, fonts)

        score_text = fonts[1].render("Score: {0}".format(self.score), True, (0, 191, 255))
        surface.blit(score_text, (GAME_RIGHT + 10, GAME_TOP + 20))

    def gen_next(self):
        while True:
            r = random.randint(0, ROW - 1)
            c = random.randint(0, COLUMN - 1)
            if self.grid[r][c].value == 0:
                self.grid[r][c].value = 2
                return

    def handle_collision(self, r, c):
        self.grid[r][c].upgrade_value()
        self.score += SCORE_PER_COLLISION

    def handle_input(self, direction):
        if direction == Direction.Up:
            for r in range(0, ROW):
                for c in range(0, COLUMN):
                    self.move_up(r, c)

        elif direction == Direction.Down:
            for r in range(0, ROW):
                for c in range(0, COLUMN):
                    self.move_down(r, c)

        elif direction == Direction.Left:
            for r in range(0, ROW):
                for c in range(0, COLUMN):
                    self.move_left(r, c)

        elif direction == Direction.Right:
            for r in range(0, ROW):
                for c in range(0, COLUMN):
                    self.move_right(r, c)

        game.update_game()

    def is_full(self):
        for r in range(0, ROW):
            for c in range(0, COLUMN):
                if self.grid[r][c].value == 0:
                    return False

        return True

    def is_gameover(self):
        return self.gameover

    def move_up(self, r, c):
        if self.grid[r][c].value == 0 or r == 0:
            return

        row = r
        while row > 0 and self.grid[row - 1][c].value == 0:
            row -= 1

        if row == 0:
            self.grid[0][c].value = self.grid[r][c].value
            return

        if self.grid[row - 1][c].value == self.grid[row][c].value:
            self.grid[row - 1][c].upgrade_value()
            self.grid[r][c].value = 0
        else:
            temp = self.grid[r][c].value
            self.grid[r][c].value = 0
            self.grid[row][c].value = temp

    def move_down(self, r, c):
        if self.grid[r][c].value == 0 or r == ROW - 1:
            return
        row = r
        while row < ROW - 1 and self.grid[row + 1][c].value == 0:
            row += 1

        if row == ROW - 1:
            self.grid[ROW - 1][c].value = self.grid[r][c].value
            return

        if self.grid[row + 1][c].value == self.grid[row][c].value:
            self.grid[row + 1][c].upgrade_value()
            self.grid[r][c].value = 0
        else:
            temp = self.grid[r][c].value
            self.grid[r][c].value = 0
            self.grid[row][c].value = temp

    def move_left(self, r, c):
        if self.grid[r][c].value == 0 or c == 0:
            return

        column = c
        while column > 0 and self.grid[r][column - 1].value == 0:
            column -= 1

        if column == 0:
            self.grid[r][0].value = self.grid[r][c].value
            return

        if self.grid[r][column - 1].value == self.grid[r][column].value:
            self.grid[r][column - 1].upgrade_value()
            self.grid[r][c].value = 0
        else:
            temp = self.grid[r][c].value
            self.grid[r][c].value = 0
            self.grid[r][column].value = temp

    def move_right(self, r, c):
        if self.grid[r][c].value == 0 or c == COLUMN - 1:
            return

        column = c
        while column < COLUMN - 1 and self.grid[r][column + 1].value == 0:
            column += 1

        if column == COLUMN - 1:
            self.grid[r][COLUMN - 1].value = self.grid[r][c].value
            return

        if self.grid[r][column + 1].value == self.grid[r][column].value:
            self.grid[r][column + 1].upgrade_value()
            self.grid[r][c].value = 0
        else:
            temp = self.grid[r][c].value
            self.grid[r][c].value = 0
            self.grid[r][column].value = temp

    def update_game(self):
        if not self.is_full():
            self.gen_next()
        else:
            self.gameover = True

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2048")

fonts = (pygame.font.Font(None, 80),
         pygame.font.Font(None, 70),
         pygame.font.Font(None, 60),
         pygame.font.Font(None, 50))

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.handle_input(Direction.Up)
            elif event.key == pygame.K_DOWN:
                game.handle_input(Direction.Down)
            elif event.key == pygame.K_LEFT:
                game.handle_input(Direction.Left)
            elif event.key == pygame.K_RIGHT:
                game.handle_input(Direction.Right)

    screen.fill((0, 0, 0), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
    game.draw_map(screen, fonts)
    pygame.display.update()