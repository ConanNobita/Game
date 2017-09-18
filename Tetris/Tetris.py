import sys, math, random, pygame
from enum import Enum
from pygame.locals import *

WINDOW_WIDTH = 560
WINDOW_HEIGHT = 480

GAME_MAP_TOP = 40
GAME_MAP_BOTTOM = 440
GAME_MAP_LEFT = 20
GAME_MAP_RIGHT = 320

GAME_MAP_WIDTH = 300
GAME_MAP_HEIGHT = 400

TOP_LINE = 50
BOTTOM_LINE = 430
LEFT_LINE = 30
RIGHT_LINE = 310

ROWS = 20
COLUMNS = 15

SQUARE_HALF_LENGTH = 10
SQUARE_LENGTH = 20

CURR_BLOCK_START_X = 150
CURR_BLOCK_START_Y = 70

NEXT_BLOCK_X = 450
NEXT_BLOCK_Y = 300

SCORE_PER_ROW = 10
SCORE_NEXT_LEVEL = 150

SLIDE_TIME = 5


def print_text(surface, font, text, x, y, color=(0, 191, 255)):
    image_text = font.render(text, True, color)
    surface.blit(image_text, (x, y))


class RotateAngle(Enum):
    R_90 = 0
    R_180 = 1
    R_270 = 2
    R_360 = 3


class Shape(Enum):
    I_Block = 0
    J_Block = 1
    L_Block = 2
    O_Block = 3
    S_Block = 4
    T_Block = 5
    Z_Block = 6


class State(Enum):
    Accelerate = 0,
    Down = 1
    Left = 2
    Right = 3
    Rotate = 4


class Square():
    def __init__(self, color, x, y):
        self.color = color
        self.center_x = x
        self.center_y = y

    def move(self, state, level, rate):
        if state == State.Accelerate:
            self.center_y += level * rate * SQUARE_LENGTH
        elif state == State.Down:
            self.center_y += rate * SQUARE_LENGTH
        elif state == State.Left:
            self.center_x -= SQUARE_LENGTH
        elif state == State.Right:
            self.center_x += SQUARE_LENGTH
        elif state == State.Rotate:
            pass

    def draw_square(self, surface):
        _x = self.center_x - SQUARE_HALF_LENGTH
        _y = self.center_y - SQUARE_HALF_LENGTH
        pygame.draw.rect(surface, self.color, [_x, _y, SQUARE_LENGTH, SQUARE_LENGTH])


class Block:
    def __init__(self, shape, center_x, center_y):
        self.shape = shape
        self.centerX = center_x
        self.centerY = center_y
        self.squares = [
            Square((0, 0, 0), 0, 0), Square((0, 0, 0), 0, 0),
            Square((0, 0, 0), 0, 0), Square((0, 0, 0), 0, 0)
        ]

        self.setup_block(self.centerX, self.centerY)

    def draw_block(self, surface):
        for i in range(0, 4):
            self.squares[i].draw_square(surface)

    def get_block_pos(self):
        pos = [0] * 8
        for i in range(0, 4):
            x = self.squares[i].center_x
            y = self.squares[i].center_y

            x -= self.centerX
            y -= self.centerY

            x, y = -y, x

            x += self.centerX
            y += self.centerY

            pos[i * 2] = x
            pos[i * 2 + 1] = y

        return pos

    def move_block(self, state, level, rate):
        if state == State.Accelerate:
            self.centerY += level * rate * SQUARE_LENGTH
        elif state == State.Down:
            self.centerY += level * SQUARE_LENGTH
        elif state == State.Left:
            self.centerX -= SQUARE_LENGTH
        elif state == State.Right:
            self.centerX += SQUARE_LENGTH
        elif state == State.Rotate:
            pass

        for i in range(0, 4):
            self.squares[i].move(state, level, rate)

    def rotate_block(self, rotate_angle):
        if rotate_angle == RotateAngle.R_90:
            for i in range(0, 4):
                pos_x = self.squares[i].center_x
                pos_y = self.squares[i].center_y

                pos_x -= self.centerX
                pos_y -= self.centerY

                pos_x, pos_y = -pos_y, pos_x

                pos_x += self.centerX
                pos_y += self.centerY

                self.squares[i].center_x = pos_x
                self.squares[i].center_y = pos_y

        elif rotate_angle == RotateAngle.R_180:
            for i in range(0, 4):
                pos_x = self.squares[i].center_x
                pos_y = self.squares[i].center_y

                pos_x -= self.centerX
                pos_y -= self.centerY

                pos_x, pos_y = -pos_x, -pos_y

                pos_x += self.centerX
                pos_y += self.centerY

                self.squares[i].center_x = pos_x
                self.squares[i].center_y = pos_y

        elif rotate_angle == RotateAngle.R_270:
            for i in range(0, 4):
                pos_x = self.squares[i].center_x
                pos_y = self.squares[i].center_y

                pos_x -= self.centerX
                pos_y -= self.centerY

                pos_x, pos_y = pos_y, -pos_x

                pos_x += self.centerX
                pos_y += self.centerY

                self.squares[i].center_x = pos_x
                self.squares[i].center_y = pos_y

        elif rotate_angle == RotateAngle.R_360:
            pass

    def setup_block(self, center_x, center_y):
        self.centerX = center_x
        self.centerY = center_y

        if self.shape == Shape.I_Block:
            self.centerX -= SQUARE_HALF_LENGTH
            self.centerY -= SQUARE_HALF_LENGTH
            self.squares[0].center_x = self.centerX + 1 * SQUARE_HALF_LENGTH
            self.squares[0].center_y = self.centerY - 3 * SQUARE_HALF_LENGTH
            self.squares[1].center_x = self.centerX + 1 * SQUARE_HALF_LENGTH
            self.squares[1].center_y = self.centerY - 1 * SQUARE_HALF_LENGTH
            self.squares[2].center_x = self.centerX + 1 * SQUARE_HALF_LENGTH
            self.squares[2].center_y = self.centerY + 1 * SQUARE_HALF_LENGTH
            self.squares[3].center_x = self.centerX + 1 * SQUARE_HALF_LENGTH
            self.squares[3].center_y = self.centerY + 3 * SQUARE_HALF_LENGTH
            for i in range(0, 4):
                self.squares[i].color = (0, 255, 255)

        elif self.shape == Shape.J_Block:
            self.squares[0].center_x = self.centerX + 0 * SQUARE_HALF_LENGTH
            self.squares[0].center_y = self.centerY - 2 * SQUARE_HALF_LENGTH
            self.squares[1].center_x = self.centerX + 0 * SQUARE_HALF_LENGTH
            self.squares[1].center_y = self.centerY + 0 * SQUARE_HALF_LENGTH
            self.squares[2].center_x = self.centerX + 0 * SQUARE_HALF_LENGTH
            self.squares[2].center_y = self.centerY + 2 * SQUARE_HALF_LENGTH
            self.squares[3].center_x = self.centerX - 2 * SQUARE_HALF_LENGTH
            self.squares[3].center_y = self.centerY + 2 * SQUARE_HALF_LENGTH
            for i in range(0, 4):
                self.squares[i].color = (0, 0, 255)

        elif self.shape == Shape.L_Block:
            self.squares[0].center_x = self.centerX + 0 * SQUARE_HALF_LENGTH
            self.squares[0].center_y = self.centerY - 2 * SQUARE_HALF_LENGTH
            self.squares[1].center_x = self.centerX + 0 * SQUARE_HALF_LENGTH
            self.squares[1].center_y = self.centerY + 0 * SQUARE_HALF_LENGTH
            self.squares[2].center_x = self.centerX + 0 * SQUARE_HALF_LENGTH
            self.squares[2].center_y = self.centerY + 2 * SQUARE_HALF_LENGTH
            self.squares[3].center_x = self.centerX + 2 * SQUARE_HALF_LENGTH
            self.squares[3].center_y = self.centerY + 2 * SQUARE_HALF_LENGTH
            for i in range(0, 4):
                self.squares[i].color = (255, 165, 0)

        elif self.shape == Shape.O_Block:
            self.centerX -= SQUARE_HALF_LENGTH
            self.centerY -= SQUARE_HALF_LENGTH
            self.squares[0].center_x = self.centerX - 1 * SQUARE_HALF_LENGTH
            self.squares[0].center_y = self.centerY - 1 * SQUARE_HALF_LENGTH
            self.squares[1].center_x = self.centerX + 1 * SQUARE_HALF_LENGTH
            self.squares[1].center_y = self.centerY - 1 * SQUARE_HALF_LENGTH
            self.squares[2].center_x = self.centerX - 1 * SQUARE_HALF_LENGTH
            self.squares[2].center_y = self.centerY + 1 * SQUARE_HALF_LENGTH
            self.squares[3].center_x = self.centerX + 1 * SQUARE_HALF_LENGTH
            self.squares[3].center_y = self.centerY + 1 * SQUARE_HALF_LENGTH
            for i in range(0, 4):
                self.squares[i].color = (255, 255, 0)

        elif self.shape == Shape.S_Block:
            self.squares[0].center_x = self.centerX + 2 * SQUARE_HALF_LENGTH
            self.squares[0].center_y = self.centerY - 2 * SQUARE_HALF_LENGTH
            self.squares[1].center_x = self.centerX + 0 * SQUARE_HALF_LENGTH
            self.squares[1].center_y = self.centerY - 2 * SQUARE_HALF_LENGTH
            self.squares[2].center_x = self.centerX + 0 * SQUARE_HALF_LENGTH
            self.squares[2].center_y = self.centerY + 0 * SQUARE_HALF_LENGTH
            self.squares[3].center_x = self.centerX - 2 * SQUARE_HALF_LENGTH
            self.squares[3].center_y = self.centerY + 0 * SQUARE_HALF_LENGTH
            for i in range(0, 4):
                self.squares[i].color = (0, 255, 0)

        elif self.shape == Shape.T_Block:
            self.squares[0].center_x = self.centerX - 0 * SQUARE_HALF_LENGTH
            self.squares[0].center_y = self.centerY - 2 * SQUARE_HALF_LENGTH
            self.squares[1].center_x = self.centerX - 2 * SQUARE_HALF_LENGTH
            self.squares[1].center_y = self.centerY + 0 * SQUARE_HALF_LENGTH
            self.squares[2].center_x = self.centerX + 0 * SQUARE_HALF_LENGTH
            self.squares[2].center_y = self.centerY + 0 * SQUARE_HALF_LENGTH
            self.squares[3].center_x = self.centerX + 2 * SQUARE_HALF_LENGTH
            self.squares[3].center_y = self.centerY + 0 * SQUARE_HALF_LENGTH
            for i in range(0, 4):
                self.squares[i].color = (128, 0, 128)

        elif self.shape == Shape.Z_Block:
            self.squares[0].center_x = self.centerX - 2 * SQUARE_HALF_LENGTH
            self.squares[0].center_y = self.centerY - 2 * SQUARE_HALF_LENGTH
            self.squares[1].center_x = self.centerX + 0 * SQUARE_HALF_LENGTH
            self.squares[1].center_y = self.centerY - 2 * SQUARE_HALF_LENGTH
            self.squares[2].center_x = self.centerX + 0 * SQUARE_HALF_LENGTH
            self.squares[2].center_y = self.centerY + 0 * SQUARE_HALF_LENGTH
            self.squares[3].center_x = self.centerX + 2 * SQUARE_HALF_LENGTH
            self.squares[3].center_y = self.centerY + 0 * SQUARE_HALF_LENGTH
            for i in range(0, 4):
                self.squares[i].color = (255, 0, 0)


class Game:
    def __init__(self):
        self.level = 1
        self.rate = 1
        self.score = 0
        self.b_gameover = False
        self.down_count = 0
        self.slide_count = SLIDE_TIME

        self.current_block = Block(Shape(random.randint(0, 6)),
                                   CURR_BLOCK_START_X, CURR_BLOCK_START_Y)
        self.next_block = Block(Shape(random.randint(0, 6)),
                                NEXT_BLOCK_X, NEXT_BLOCK_Y)
        self.current_block.rotate_block(RotateAngle(random.randint(0, 3)))
        self.current_block.rotate_block(RotateAngle(random.randint(0, 3)))

        self.game_map = []
        self.rows = [0] * ROWS

    def change_current_block(self):
        for i in range(0, 4):
            self.game_map.append(self.current_block.squares[i])

        del self.current_block.squares
        del self.next_block.squares

        self.current_block.squares = [
            Square((0, 0, 0), 0, 0), Square((0, 0, 0), 0, 0),
            Square((0, 0, 0), 0, 0), Square((0, 0, 0), 0, 0)
        ]

        self.next_block.squares = [
            Square((0, 0, 0), 0, 0), Square((0, 0, 0), 0, 0),
            Square((0, 0, 0), 0, 0), Square((0, 0, 0), 0, 0)
        ]

        self.current_block.shape = self.next_block.shape
        self.next_block.shape = Shape(random.randint(0, 6))
        self.current_block.setup_block(CURR_BLOCK_START_X, CURR_BLOCK_START_Y)
        self.next_block.setup_block(NEXT_BLOCK_X, NEXT_BLOCK_Y)
        self.current_block.rotate_block(RotateAngle(random.randint(0, 3)))

    def check_collision_entity_single(self, square, state):
        x = square.center_x
        y = square.center_y

        if state == State.Accelerate:
            y += self.level * self.rate * SQUARE_LENGTH
        elif state == State.Down:
            y += self.level * SQUARE_LENGTH
        elif state == State.Left:
            x -= SQUARE_LENGTH
        elif state == State.Right:
            x += SQUARE_LENGTH
        elif state == State.Rotate:
            pass

        for i in range(0, len(self.game_map)):
            if self.game_map[i] is not None:
                if math.fabs(x - self.game_map[i].center_x) < SQUARE_LENGTH and \
                                math.fabs(y - self.game_map[i].center_y) < SQUARE_LENGTH:
                    return True
        return False

    def check_collision_entity(self, state):
        for i in range(0, 4):
            if self.check_collision_entity_single(self.current_block.squares[i], state):
                return True
        return False

    def check_collision_wall_single(self, square, state):
        x = square.center_x
        y = square.center_y

        if state == State.Accelerate:
            ret = y >= BOTTOM_LINE
        elif state == State.Down:
            ret = y >= BOTTOM_LINE
        elif state == State.Left:
            ret = x <= LEFT_LINE
        elif state == State.Right:
            ret = x >= RIGHT_LINE
        elif state == State.Rotate:
            ret = False

        return ret

    def check_collision_wall(self, state):
        for i in range(0, 4):
            if self.check_collision_wall_single(self.current_block.squares[i], state):
                return True

        return False

    def check_game_over(self):
        return self.b_gameover

    def check_rotated_collision(self):
        pos = self.current_block.get_block_pos()
        length = len(self.game_map)

        for i in range(0, 4):
            if pos[i * 2] < LEFT_LINE or pos[i * 2] > RIGHT_LINE:
                del pos
                return True

            if pos[i * 2 + 1] > BOTTOM_LINE:
                del pos
                return True

            for j in range(0, length):
                if self.game_map[i] is not None:
                    x = self.game_map[i].center_x
                    y = self.game_map[i].center_y
                    if math.fabs(pos[i * 2] - x) < SQUARE_LENGTH and \
                                    math.fabs(pos[i * 2 + 1] - y) < SQUARE_LENGTH:
                        del pos
                        return True

        del pos
        return False

    def clear_row(self):
        full_row = 0
        length = len(self.game_map)

        for i in range(0, ROWS):
            self.rows[i] = 0

        for i in range(0, length):
            if self.game_map[i] is not None:
                row = int((self.game_map[i].center_y - TOP_LINE) / SQUARE_LENGTH)
                self.rows[row] += 1

        if self.rows[0] >= 1:
            self.b_gameover = True

        for r in range(0, ROWS):
            if self.rows[r] == COLUMNS:
                full_row += 1
                for i in range(0, length):
                    if self.game_map[i] is not None:
                        if (self.game_map[i].center_y - TOP_LINE) / SQUARE_LENGTH == r:
                            self.game_map[i] = None

        for i in range(0, length):
            for r in range(0, ROWS):
                if self.rows[r] == COLUMNS:
                    if self.game_map[i] is not None:
                        row = int((self.game_map[i].center_y - TOP_LINE) / SQUARE_LENGTH)
                    if r > row:
                        if self.game_map[i] is not None:
                            self.game_map[i].move(State.Down, 1, 1)

        return full_row

    def draw_map(self, surface, font):
        self.current_block.draw_block(surface)
        self.next_block.draw_block(surface)

        length = len(self.game_map)
        for i in range(0, length):
            if self.game_map[i] is not None:
                self.game_map[i].draw_square(surface)

        pygame.draw.rect(surface, (173, 216, 230), (0, SQUARE_LENGTH, GAME_MAP_WIDTH + 2 * SQUARE_LENGTH,
                                                    SQUARE_LENGTH))
        pygame.draw.rect(surface, (173, 216, 230), (0, GAME_MAP_TOP, SQUARE_LENGTH, GAME_MAP_HEIGHT))
        pygame.draw.rect(surface, (173, 216, 230), (GAME_MAP_RIGHT, GAME_MAP_TOP, SQUARE_LENGTH, GAME_MAP_HEIGHT))
        pygame.draw.rect(surface, (173, 216, 230), (0, GAME_MAP_BOTTOM, GAME_MAP_WIDTH + 2 * SQUARE_LENGTH,
                                                    SQUARE_LENGTH))
        for i in range(0, ROWS + 1):
            pygame.draw.line(surface, (255, 255, 255), (GAME_MAP_LEFT, GAME_MAP_TOP + i * SQUARE_LENGTH),
                             (GAME_MAP_RIGHT, GAME_MAP_TOP + i * SQUARE_LENGTH))
        for j in range(0, COLUMNS + 1):
            pygame.draw.line(surface, (255, 255, 255), (GAME_MAP_LEFT + j * SQUARE_LENGTH, GAME_MAP_TOP),
                             (GAME_MAP_LEFT + j * SQUARE_LENGTH, GAME_MAP_BOTTOM))

        level_text = "Level: %s" % (self.level)
        score_text = "Score: %s" % (self.score)
        print_text(surface, font, level_text, 400, 70)
        print_text(surface, font, score_text, 400, 140)

    def handle_input(self, state, b_up):
        if b_up:
            if not self.check_rotated_collision():
                self.current_block.rotate_block(RotateAngle.R_90)
        else:
            if not self.check_collision_entity(state) and \
                    not self.check_collision_wall(state):
                self.current_block.move_block(state, self.level, self.rate)

    def handle_self_down(self):
        self.down_count = 0
        self.slide_count = SLIDE_TIME

        if not self.check_collision_entity(State.Down) and \
                not self.check_collision_wall(State.Down):
            self.slide_count -= 1
        else:
            self.slide_count = 0

        if self.slide_count == 0:
            self.slide_count = SLIDE_TIME
            self.handle_static_collision()

    def handle_static_collision(self):
        self.change_current_block()
        row = self.clear_row()
        if row > 0:
            self.score += row * SCORE_PER_ROW
        if self.score >= SCORE_NEXT_LEVEL:
            self.level += 1


pygame.init()
pygame.font.init()

font = pygame.font.Font(None, 40)

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption("俄罗斯方块")

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        screen.fill((0, 0, 0), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.handle_input(State.Rotate, True)
            elif event.key == pygame.K_LEFT:
                game.handle_input(State.Left, False)
            elif event.key == pygame.K_RIGHT:
                game.handle_input(State.Right, False)
            elif event.key == pygame.K_DOWN:
                game.handle_input(State.Accelerate, False)
            else:
                pass

    game.handle_self_down()

    game.draw_map(screen, font)

    if game.check_game_over():
        screen.fill((0, 0, 0), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        print_text(screen, font, "G  a  m  e   O  v  e  r", 160, 200, (255, 0, 0))

    pygame.display.update()

pygame.font.quit()
pygame.quit()