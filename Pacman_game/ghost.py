import pygame
from collections import namedtuple

from utils import Direction

Pos = namedtuple('Position', 'x, y')

class Ghost:
    def __init__(self, position, target, speed, img, direct, dead, box, id, game):
        self.pos = position
        self.center = Pos(position.x +22, position.y + 22)
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.game = game
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not self.game.powerup and not self.dead) or (self.game.eaten_ghost[self.id] and self.game.powerup and not self.dead):
            self.game.screen.blit(self.img, (self.pos.x, self.pos.y))
        elif self.game.powerup and not self.dead and not self.game.eaten_ghost[self.id]:
            self.game.screen.blit(self.game.spooked_img, (self.pos.x, self.pos.y))
        else:
            self.game.screen.blit(self.game.dead_img, (self.pos.x, self.pos.y))
        ghost_rect = pygame.rect.Rect((self.center.x - 18, self.center.y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        num1 = ((self.game.HEIGHT - 50) // 32)
        num2 = (self.game.WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center.x // 30 < 29:
            if self.game.level[(self.center.y - num3) // num1][self.center.x // num2] == 9:
                self.turns[2] = True
            if self.game.level[self.center.y // num1][(self.center.x - num3) // num2] < 3 \
                    or (self.game.level[self.center.y // num1][(self.center.x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if self.game.level[self.center.y // num1][(self.center.x + num3) // num2] < 3 \
                    or (self.game.level[self.center.y // num1][(self.center.x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if self.game.level[(self.center.y + num3) // num1][self.center.x // num2] < 3 \
                    or (self.game.level[(self.center.y + num3) // num1][self.center.x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if self.game.level[(self.center.y - num3) // num1][self.center.x // num2] < 3 \
                    or (self.game.level[(self.center.y - num3) // num1][self.center.x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == Direction.UP or self.direction == Direction.DOWN:
                if 12 <= self.center.x % num2 <= 18:
                    if self.game.level[(self.center.y + num3) // num1][self.center.x // num2] < 3 \
                            or (self.game.level[(self.center.y + num3) // num1][self.center.x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if self.game.level[(self.center.y - num3) // num1][self.center.x // num2] < 3 \
                            or (self.game.level[(self.center.y - num3) // num1][self.center.x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center.y % num1 <= 18:
                    if self.game.level[self.center.y // num1][(self.center.x - num2) // num2] < 3 \
                            or (self.game.level[self.center.y // num1][(self.center.x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if self.game.level[self.center.y // num1][(self.center.x + num2) // num2] < 3 \
                            or (self.game.level[self.center.y // num1][(self.center.x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == Direction.RIGHT or self.direction == Direction.LEFT:
                if 12 <= self.center.x % num2 <= 18:
                    if self.game.level[(self.center.y + num3) // num1][self.center.x // num2] < 3 \
                            or (self.game.level[(self.center.y + num3) // num1][self.center.x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if self.game.level[(self.center.y - num3) // num1][self.center.x // num2] < 3 \
                            or (self.game.level[(self.center.y - num3) // num1][self.center.x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center.y % num1 <= 18:
                    if self.game.level[self.center.y // num1][(self.center.x - num3) // num2] < 3 \
                            or (self.game.level[self.center.y // num1][(self.center.x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if self.game.level[self.center.y // num1][(self.center.x + num3) // num2] < 3 \
                            or (self.game.level[self.center.y // num1][(self.center.x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.pos.x < 550 and 370 < self.pos.y < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_clyde(self):
        # clyde is going to turn whenever advantageous for pursuit
        pos_x = self.pos.x
        pos_y = self.pos.y
        if self.direction == Direction.RIGHT:
            if self.target[0] >pos_x and self.turns[0]:
                pos_x += self.speed
            elif not self.turns[0]:
                if self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.target[0] <pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
            elif self.turns[0]:
                if self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                if self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                else:
                    pos_x += self.speed
        elif self.direction == Direction.LEFT:
            if self.target[1] > pos_y and self.turns[3]:
                self.direction = Direction.DOWN
            elif self.target[0] <pos_x and self.turns[1]:
                pos_x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.target[0] >pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
            elif self.turns[1]:
                if self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                if self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                else:
                    pos_x -= self.speed
        elif self.direction == Direction.UP:
            if self.target[0] <pos_x and self.turns[1]:
                self.direction = Direction.LEFT
                pos_x -= self.speed
            elif self.target[1] < pos_y and self.turns[2]:
                self.direction = Direction.UP
                pos_y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.target[0] <pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
            elif self.turns[2]:
                if self.target[0] > pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.target[0] < pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                else:
                    pos_y -= self.speed
        elif self.direction == Direction.DOWN:
            if self.target[1] > pos_y and self.turns[3]:
                pos_y += self.speed
            elif not self.turns[3]:
                if self.target[0] >pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.target[0] <pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
            elif self.turns[3]:
                if self.target[0] >pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.target[0] <pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                else:
                    pos_y += self.speed
        if pos_x < -30:
            pos_x = 900
        elif pos_x > 900:
            pos_x = - 30
            
        return Pos(pos_x, pos_y), self.direction
    
    def move_blinky(self):
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        pos_x = self.pos.x
        pos_y = self.pos.y
        if self.direction == Direction.RIGHT:
            if self.target[0] > pos_x and self.turns[0]:
                pos_x += self.speed
            elif not self.turns[0]:
                if self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.target[0] < pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
            elif self.turns[0]:
                pos_x += self.speed
        elif self.direction == Direction.LEFT:
            if self.target[0] < pos_x and self.turns[1]:
                pos_x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.target[0] > pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
            elif self.turns[1]:
                pos_x -= self.speed
        elif self.direction == Direction.UP:
            if self.target[1] < pos_y and self.turns[2]:
                self.direction = Direction.UP
                pos_y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.target[0] < pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
            elif self.turns[2]:
                pos_y -= self.speed
        elif self.direction == Direction.DOWN:
            if self.target[1] > pos_y and self.turns[3]:
                pos_y += self.speed
            elif not self.turns[3]:
                if self.target[0] > pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.target[0] < pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
            elif self.turns[3]:
                pos_y += self.speed
        if pos_x < -30:
            pos_x = 900
        elif pos_x > 900:
            pos_x = -30
        return Pos(pos_x, pos_y), self.direction

    def move_inky(self):
        # inky turns up or down at any point to pursue, but left and right only on collision
        pos_x = self.pos.x
        pos_y = self.pos.y
        if self.direction == Direction.RIGHT:
            if self.target[0] > pos_x and self.turns[0]:
                pos_x += self.speed
            elif not self.turns[0]:
                if self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.target[0] < pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
            elif self.turns[0]:
                if self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                if self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                else:
                    pos_x += self.speed
        elif self.direction == Direction.LEFT:
            if self.target[1] > pos_y and self.turns[3]:
                self.direction = Direction.DOWN
            elif self.target[0] < pos_x and self.turns[1]:
                pos_x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.target[0] > pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
            elif self.turns[1]:
                if self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                if self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                else:
                    pos_x -= self.speed
        elif self.direction == Direction.UP:
            if self.target[1] < pos_y and self.turns[2]:
                self.direction = Direction.UP
                pos_y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.target[0] < pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
            elif self.turns[2]:
                pos_y -= self.speed
        elif self.direction == Direction.DOWN:
            if self.target[1] > pos_y and self.turns[3]:
                pos_y += self.speed
            elif not self.turns[3]:
                if self.target[0] > pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.target[0] < pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
            elif self.turns[3]:
                pos_y += self.speed
        if pos_x < -30:
            pos_x = 900
        elif pos_x > 900:
            pos_x -= 30
        return Pos(pos_x, pos_y), self.direction


    def move_pinky(self):
        # pinky is going to turn left or right whenever advantageous, but only up or down on collision
        pos_x = self.pos.x
        pos_y = self.pos.y
        if self.direction == Direction.RIGHT:
            if self.target[0] > pos_x and self.turns[0]:
                pos_x += self.speed
            elif not self.turns[0]:
                if self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.target[0] < pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
            elif self.turns[0]:
                pos_x += self.speed
        elif self.direction == Direction.LEFT:
            if self.target[1] > pos_y and self.turns[3]:
                self.direction = Direction.DOWN
            elif self.target[0] < pos_x and self.turns[1]:
                pos_x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.target[0] > pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
            elif self.turns[1]:
                pos_x -= self.speed
        elif self.direction == Direction.UP:
            if self.target[0] < pos_x and self.turns[1]:
                self.direction = Direction.LEFT
                pos_x -= self.speed
            elif self.target[1] < pos_y and self.turns[2]:
                self.direction = Direction.UP
                pos_y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.target[0] < pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.target[1] > pos_y and self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.turns[3]:
                    self.direction = Direction.DOWN
                    pos_y += self.speed
                elif self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
            elif self.turns[2]:
                if self.target[0] > pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.target[0] < pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                else:
                    pos_y -= self.speed
        elif self.direction == Direction.DOWN:
            if self.target[1] > pos_y and self.turns[3]:
                pos_y += self.speed
            elif not self.turns[3]:
                if self.target[0] > pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.target[0] < pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.target[1] < pos_y and self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[2]:
                    self.direction = Direction.UP
                    pos_y -= self.speed
                elif self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                elif self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
            elif self.turns[3]:
                if self.target[0] > pos_x and self.turns[0]:
                    self.direction = Direction.RIGHT
                    pos_x += self.speed
                elif self.target[0] < pos_x and self.turns[1]:
                    self.direction = Direction.LEFT
                    pos_x -= self.speed
                else:
                    pos_y += self.speed
        if pos_x < -30:
            pos_x = 900
        elif pos_x > 900:
            pos_x -= 30
        return Pos(pos_x, pos_y), self.direction

