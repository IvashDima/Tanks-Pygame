import pygame
import os
from modules.mapsetting import map

DIR_PATH = os.path.abspath(__file__ + '/../..')
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
STEP = 50


window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tanks 2D')


class Block(pygame.Rect):
    def __init__(self, x, y, type_block, image):
        super().__init__(x, y, STEP, STEP)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (STEP, STEP))
        self.type_block = type_block

    def blit(self):
        window.blit(self.image, (self.x, self.y))


class Bullet(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20)
        self.image = pygame.image.load(os.path.join(DIR_PATH, 'images/bullet.png'))
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.direction = None
        self.speed = 50
        self.count = 0

    def move(self):
        if self.count != 0:
            window.blit(self.image, (self.x, self.y))
            if self.direction == 0:
                self.y -= self.speed
            elif self.direction == 180:
                self.y += self.speed
            elif self.direction == 90:
                self.x -= self.speed
            elif self.direction == 270:
                self.x += self.speed
            self.count -= 1
            if self.count == 0:
                self.stop()

    def stop(self):
        self.count = 0
        self.x = 100000


class Panzar(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x * STEP, y * STEP, STEP, STEP)
        self.image = None
        self.pos = [x, y]
        self.bullet = Bullet(x, y)
        self.angle = 0

    def move(self):
        pass

    def move_voice(self):
        sound_move = pygame.mixer.Sound(os.path.join(DIR_PATH, 'sounds', 'move.mp3'))
        sound_move.play(loops=0, maxtime=200, fade_ms=0)

    def up(self):
        self.move_voice()
        if map[self.pos[1] - 1][self.pos[0]] == 0:
            self.y -= STEP
            self.pos[1] -= 1
        self.rotate_to(0)

    def down(self):
        self.move_voice()
        if map[self.pos[1] + 1][self.pos[0]] == 0:
            self.y += STEP
            self.pos[1] += 1
        self.rotate_to(180)

    def left(self):
        self.move_voice()
        if map[self.pos[1]][self.pos[0] - 1] == 0:
            self.x -= STEP
            self.pos[0] -= 1
        self.rotate_to(90)

    def right(self):
        self.move_voice()
        if map[self.pos[1]][self.pos[0] + 1] == 0:
            self.x += STEP
            self.pos[0] += 1
        self.rotate_to(270)

    def blit(self):
        self.move()
        window.blit(self.image, (self.x, self.y))

    def rotate_to(self, angle):
        rotate = (360 - self.angle + angle)
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, rotate)

    def strike(self):
        if self.bullet.count == 0:
            sound_shot = pygame.mixer.Sound(os.path.join(DIR_PATH, 'sounds', 'shot.mp3'))
            sound_shot.play()
            self.bullet.x = self.x + STEP / 2 - 10
            self.bullet.y = self.y + STEP / 2 - 10
            self.bullet.count = 10
            self.bullet.direction = self.angle


class Player1(Panzar):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load(os.path.join(DIR_PATH, 'images/panzer.png'))
        self.image = pygame.transform.scale(self.image, (STEP, STEP))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.up()
        elif keys[pygame.K_s]:
            self.down()
        elif keys[pygame.K_a]:
            self.left()
        elif keys[pygame.K_d]:
            self.right()
        elif keys[pygame.K_z]:
            self.strike()


class Player2(Panzar):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load(os.path.join(DIR_PATH, 'images/enemy.png'))
        self.image = pygame.transform.scale(self.image, (STEP, STEP))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.up()
        elif keys[pygame.K_DOWN]:
            self.down()
        elif keys[pygame.K_LEFT]:
            self.left()
        elif keys[pygame.K_RIGHT]:
            self.right()
        elif keys[pygame.K_m]:
            self.strike()