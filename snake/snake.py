from pygame.locals import *
import pygame
import random
import sys

Direction = {
    "Up": 1,
    "Down": 2,
    "Left": 3,
    "Right": 6
}

def checkCollision(dir, src, dst, w1, h1, w2, h2):
    if dir == Direction["Up"]:
        if src.y <= dst.y + h2:
            return True

    elif dir == Direction["Down"]:
        if src.y + h1 >= dst.y:
            return True

    elif dir == Direction["Left"]:
        if src.x <= dst.x + w2:
            return True

    elif dir == Direction["Right"]:
        if src.x + w1 >= dst.x:
            return True

    return False

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Food(object):
    def __init__(self):
        self.pos = Point(100, 100)
        self.visible = True 

    def generate(self):
        if self.visible == False:
            self.pos.x = random.randint(40, 600)
            self.pos.y = random.randint(30, 450)
            self.visible = True 

    def setEated(self, flag):
        self.visible = not flag

    def draw(self, surface):
        if self.visible == True:
            pygame.draw.circle(surface, (255, 0, 0), (self.pos.x + 5, self.pos.y + 5), 10)
    
class Snake(object):
    def __init__(self):
        self.head = Point(320, 240)
        self.body = []
        self.width = 20
        self.height = 20
        self.direction = Direction["Down"]


    def createSnake(self):
        x = self.head.x
        y = self.head.y - self.height

        for i in range(0, 3):
            self.body.append(Point(x, y))
            y -= self.height

    def checkCollisionWall(self, wallRect):
        wallPos = Point(wallRect.left(), wallRect.top())
        return checkCollision(self.direction, self.head, wallPos, self.width, self.head, wallRect.width(),
                              wallRect.height())

    def checkCollisionSelf(self):
        length = len(self.body)
        for i in range(0, length):
            if checkCollision(self.direction, self.head, self.body[i], self.width, self.height,
                              self.width, self.height):
                return True
        return False

    def move(self, dirs, speed):
        if dirs == self.direction / 2 or dirs == self.direction * 2:
            return

        tail = self.body.pop()
        tail.x = self.head.x
        tail.y = self.head.y

        self.body.insert(0, self.head)
        self.head = tail

        if dirs == Direction["Up"]:
            self.head.y -= speed

        elif dirs == Direction["Down"]:
            self.head.y += speed

        elif dirs == Direction["Left"]:
            self.head.x -= speed

        elif dirs == Direction["Right"]:
            self.head.x += speed

        self.direction = dirs

    def eatFood(self, food):
        if checkCollision(self.direction, self.head, food.pos, self.width, self.height, 10, 10) == True:
            newHead = Point(food.pos.x, food.pos.y)
            self.body.insert(0, self.head)
            self.head = newHead 
            return True 
        
        return False 

    def drawSelf(self, surface):
        length = len(self.body)
        surface.fill((0, 0, 0))
        pygame.draw.rect(surface, (0, 255, 0), (self.head.x, self.head.y, self.width, self.height))
        for i in range(0, length):
            pygame.draw.rect(surface, (0, 0, 255), (self.body[i].x, self.body[i].y, self.width, self.height))


pygame.init()
screen = pygame.display.set_mode([640, 480])
clock = pygame.time.Clock()

#food = Food()

snake = Snake()
snake.createSnake()
dirs = Direction["Up"]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dirs = Direction["Up"]

            elif event.key == pygame.K_DOWN:
                dirs = Direction["Down"]

            elif event.key == pygame.K_LEFT:
                dirs = Direction["Left"]

            elif event.key == pygame.K_RIGHT:
                dirs = Direction["Right"]

    clock.tick(10)
    snake.move(dirs, 20)
    
    #if snake.eatFood(food):
        #food.setEated(True)
        #food.generate()
        
    #food.draw(screen)
    snake.drawSelf(screen)
    pygame.display.update()

pygame.quit()
