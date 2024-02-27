import copy
from Pacman_game.ghost import Ghost
from Pacman_game.utils import Direction

from Pacman_game.board import boards
import pygame
from math import pi as PI
from collections import namedtuple


pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)
       
fps = 60
Pos = namedtuple('Position', 'x, y')

class PacmanGame:
    
    def __init__(self, WIDTH=900, HEIGHT=950):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        #init display
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption('Pacman')
        self.timer = pygame.time.Clock()
        self.flicker = False
        self.player_images = []
        for i in range(1, 5):
            self.player_images.append(pygame.transform.scale(pygame.image.load(f'Pacman_game/assets/player_images/{i}.png'), (45, 45)))
        self.blinky_img = pygame.transform.scale(pygame.image.load(f'Pacman_game/assets/ghost_images/red.png'), (45, 45))
        self.pinky_img = pygame.transform.scale(pygame.image.load(f'Pacman_game/assets/ghost_images/pink.png'), (45, 45))
        self.inky_img = pygame.transform.scale(pygame.image.load(f'Pacman_game/assets/ghost_images/blue.png'), (45, 45))
        self.clyde_img = pygame.transform.scale(pygame.image.load(f'Pacman_game/assets/ghost_images/orange.png'), (45, 45))
        self.spooked_img = pygame.transform.scale(pygame.image.load(f'Pacman_game/assets/ghost_images/powerup.png'), (45, 45))
        self.dead_img = pygame.transform.scale(pygame.image.load(f'Pacman_game/assets/ghost_images/dead.png'), (45, 45))
        
        #init board
        self.color = 'blue'
        
        #init game state
        self.score = 0
        self.game_over = False
        self.game_won = False
        self.level = copy.deepcopy(boards)
        self.counter = 1
        self.moving = False
        self.startup_counter = 0
        self.turns_allowed = [False, False, False, False]
        self.powerup = False
        self.power_counter = 0
        self.eaten_ghost = [False, False, False, False]
        
        self.lives = 3
        self.player_speed = 2
        self.player = Pos(450,663)
        self.playerDirection = Direction.RIGHT
        self.direction_command = Direction.RIGHT
        
        self.ghost_speeds = [2, 2, 2, 2]
        self.blinkyPos = Pos(56,58)
        self.blinkyDirection = Direction.RIGHT
        self.inkyPos = Pos(380,438) 
        self.inkyDirection = Direction.UP
        self.pinkyPos = Pos(440,438)
        self.pinkyDirection = Direction.UP
        self.clydePos = Pos(500,438)
        self.clydeDirection = Direction.UP
        # at the beginning player, and when dead it's the start ghost point
        self.targets = [(self.player.x, self.player.y), (self.player.x, self.player.y), (self.player.x, self.player.y), (self.player.x, self.player.y)]
        self.blinky_dead = False
        self.inky_dead = False
        self.clyde_dead = False
        self.pinky_dead = False
        self.blinky_box = False
        self.inky_box = False
        self.clyde_box = False
        self.pinky_box = False
        
    def draw_board(self):
        num1 = ((self.HEIGHT - 50) // 32)
        num2 = (self.WIDTH // 30)
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] == 1:
                    pygame.draw.circle(self.screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
                if self.level[i][j] == 2 and not self.flicker:
                    pygame.draw.circle(self.screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
                if self.level[i][j] == 3:
                    pygame.draw.line(self.screen, self.color, (j * num2 + (0.5 * num2), i * num1),
                                    (j * num2 + (0.5 * num2), i * num1 + num1), 3)
                if self.level[i][j] == 4:
                    pygame.draw.line(self.screen, self.color, (j * num2, i * num1 + (0.5 * num1)),
                                    (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
                if self.level[i][j] == 5:
                    pygame.draw.arc(self.screen, self.color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                    0, PI / 2, 3)
                if self.level[i][j] == 6:
                    pygame.draw.arc(self.screen, self.color,
                                    [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
                if self.level[i][j] == 7:
                    pygame.draw.arc(self.screen, self.color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                    3 * PI / 2, 3)
                if self.level[i][j] == 8:
                    pygame.draw.arc(self.screen, self.color,
                                    [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                    2 * PI, 3)
                if self.level[i][j] == 9:
                    pygame.draw.line(self.screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                    (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

    def draw_player(self):   
            if self.playerDirection == Direction.RIGHT:
                self.screen.blit(self.player_images[self.counter // 5], (self.player.x, self.player.y))
            elif self.playerDirection == Direction.LEFT:
                self.screen.blit(pygame.transform.flip(self.player_images[self.counter // 5], True, False), (self.player.x, self.player.y))
            elif self.playerDirection == Direction.UP:
                self.screen.blit(pygame.transform.rotate(self.player_images[self.counter // 5], 90), (self.player.x, self.player.y))
            elif self.playerDirection == Direction.DOWN:
                self.screen.blit(pygame.transform.rotate(self.player_images[self.counter // 5], 270), (self.player.x, self.player.y))

    def draw_misc(self):
        score_text = font.render(f'Score: {self.score}', True, 'white')
        self.screen.blit(score_text, (10, 920))
        if self.powerup:
            pygame.draw.circle(self.screen, 'blue', (140, 930), 15)
        for i in range(self.lives):
            self.screen.blit(pygame.transform.scale(self.player_images[0], (30, 30)), (650 + i * 40, 915))
        if self.game_over:
            pygame.draw.rect(self.screen, 'white', [50, 200, 800, 300],0, 10)
            pygame.draw.rect(self.screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
            self.screen.blit(gameover_text, (100, 300))
        if self.game_won:
            pygame.draw.rect(self.screen, 'white', [50, 200, 800, 300],0, 10)
            pygame.draw.rect(self.screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
            self.screen.blit(gameover_text, (100, 300))

    def handle_counter(self):
        self.timer.tick(fps)
        if self.counter < 19:
            self.counter += 1
            # points flicker 3 times a second
            if self.counter > 3:
                self.flicker = False
        else :
            self.counter = 0
            self.flicker = True
        if self.powerup and self.power_counter < 600:
            self.power_counter += 1
        elif self.powerup and self.power_counter >= 600:
            self.power_counter = 0
            self.powerup = False
            self.eaten_ghost = [False, False, False, False]
        if self.startup_counter < 180 :
            self.moving = False
            self.startup_counter += 1
        else:
            self.moving = True

    def update_ui(self):
        pass
        
    def user_input(self):
        run = True
        for event in pygame.event.get():
                if event.type == pygame.QUIT: #Red button X
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and (self.game_over or self.game_won):
                        self.take_damage()
                        self.score = 0
                        self.lives = 3
                        self.level = copy.deepcopy(boards)
                        self.game_over = False
                        self.game_won = False
                        
                """ if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT and self.direction_command == Direction.RIGHT:
                        self.direction_command = self.playerDirection
                    if event.key == pygame.K_LEFT and self.direction_command == Direction.LEFT:
                        self.direction_command = self.playerDirection
                    if event.key == pygame.K_UP and self.direction_command == Direction.UP:
                        self.direction_command = self.playerDirection
                    if event.key == pygame.K_DOWN and self.direction_command == Direction.DOWN:
                        self.direction_command = self.playerDirection
                 """
        return run
    
    def check_position(self):
        # if the player can go somewhere
        # if there is no wall
        turns = [False, False, False, False]
        num1 = (self.HEIGHT - 50) // 32
        num2 = (self.WIDTH // 30)
        num3 = 15
        # check collisions based on center x and center y of player +/- fudge number
        if self.center.x // 30 < 29:
            if self.playerDirection == Direction.RIGHT:
                if self.level[self.center.y // num1][(self.center.x - num3) // num2] < 3:
                    turns[1] = True
            if self.playerDirection == Direction.LEFT:
                if self.level[self.center.y // num1][(self.center.x + num3) // num2] < 3:
                    turns[0] = True
            if self.playerDirection == Direction.UP:
                if self.level[(self.center.y + num3) // num1][self.center.x // num2] < 3:
                    turns[3] = True
            if self.playerDirection == Direction.DOWN:
                if self.level[(self.center.y - num3) // num1][self.center.x // num2] < 3:
                    turns[2] = True

            if self.playerDirection == Direction.UP or self.playerDirection == Direction.DOWN:
                if 12 <= self.center.x % num2 <= 18:
                    if self.level[(self.center.y + num3) // num1][self.center.x // num2] < 3:
                        turns[3] = True
                    if self.level[(self.center.y - num3) // num1][self.center.x // num2] < 3:
                        turns[2] = True
                if 12 <= self.center.y % num1 <= 18:
                    if self.level[self.center.y // num1][(self.center.x - num2) // num2] < 3:
                        turns[1] = True
                    if self.level[self.center.y // num1][(self.center.x + num2) // num2] < 3:
                        turns[0] = True
                        
            if self.playerDirection == Direction.RIGHT or self.playerDirection == Direction.LEFT:
                if 12 <= self.center.x % num2 <= 18:
                    if self.level[(self.center.y + num1) // num1][self.center.x // num2] < 3:
                        turns[3] = True
                    if self.level[(self.center.y - num1) // num1][self.center.x // num2] < 3:
                        turns[2] = True
                if 12 <= self.center.y % num1 <= 18:
                    if self.level[self.center.y // num1][(self.center.x - num3) // num2] < 3:
                        turns[1] = True
                    if self.level[self.center.y // num1][(self.center.x + num3) // num2] < 3:
                        turns[0] = True
        else:
            turns[0] = True
            turns[1] = True

        return turns

    def set_direction(self):
        if self.direction_command  == Direction.RIGHT and self.turns_allowed[0]:
            self.playerDirection = Direction.RIGHT
        if self.direction_command == Direction.LEFT and self.turns_allowed[1]:
            self.playerDirection = Direction.LEFT
        if self.direction_command  == Direction.UP and self.turns_allowed[2]:
            self.playerDirection = Direction.UP
        if self.direction_command  == Direction.DOWN and self.turns_allowed[3]:
            self.playerDirection = Direction.DOWN

    def move_player(self):
        player_x = self.player.x
        player_y = self.player.y
        if self.playerDirection == Direction.RIGHT and self.turns_allowed[0]:
            player_x += self.player_speed
        elif self.playerDirection == Direction.LEFT and self.turns_allowed[1]:
            player_x -= self.player_speed
        if self.playerDirection == Direction.UP and self.turns_allowed[2]:
            player_y -= self.player_speed
        elif self.playerDirection == Direction.DOWN and self.turns_allowed[3]:
            player_y += self.player_speed
        
        self.player = Pos(player_x, player_y)
    
    def check_collisions(self):
        num1 = (self.HEIGHT - 50) // 32
        num2 = self.WIDTH // 30
        if 0 < self.player.x < 870:
            if self.level[self.center.y // num1][self.center.x // num2] == 1:
                self.level[self.center.y  // num1][self.center.x // num2] = 0
                self.score += 10
                self.reward = 5
            if self.level[self.center.y  // num1][self.center.x // num2] == 2:
                self.level[self.center.y  // num1][self.center.x // num2] = 0
                self.score += 50
                self.reward = 10
                self.powerup = True
                self.power_count = 0
                self.eaten_ghosts = [False, False, False, False]
    
    def get_targets(self):
        if self.player.x < 450:
            runaway_x = 900
        else:
            runaway_x = 0
        if self.player.y < 450:
            runaway_y = 900
        else:
            runaway_y = 0
        return_target = (380, 400)
        if self.powerup:
            if not self.blinky_dead and not self.eaten_ghost[0]:
                blink_target = (runaway_x, runaway_y)
            elif not self.blinky_dead and self.eaten_ghost[0]:
                if 340 < self.blinkyPos.x < 560 and 340 < self.blinkyPos.y < 500:
                    blink_target = (400, 100)
                else:
                    blink_target = (self.player.x, self.player.y)
            else:
                blink_target = return_target
            if not self.inky_dead and not self.eaten_ghost[1]:
                ink_target = (runaway_x, self.player.y)
            elif not self.inky_dead and self.eaten_ghost[1]:
                if 340 < self.inkyPos.x < 560 and 340 < self.inkyPos.y < 500:
                    ink_target = (400, 100)
                else:
                    ink_target = (self.player.x, self.player.y)
            else:
                ink_target = return_target
            if not self.pinky_dead:
                pink_target = (self.player.x, runaway_y)
            elif not self.pinky_dead and self.eaten_ghost[2]:
                if 340 < self.pinkyPos.x < 560 and 340 < self.pinkyPos.y < 500:
                    pink_target = (400, 100)
                else:
                    pink_target = (self.player.x, self.player.y)
            else:
                pink_target = return_target
            if not self.clyde_dead and not self.eaten_ghost[3]:
                clyd_target = (450, 450)
            elif not self.clyde_dead and self.eaten_ghost[3]:
                if 340 < self.clydePos.x < 560 and 340 < self.clydePos.y < 500:
                    clyd_target = (400, 100)
                else:
                    clyd_target = (self.player.x, self.player.y)
            else:
                clyd_target = return_target
        else:
            if not self.blinky_dead:
                if 340 < self.blinkyPos.x  < 560 and 340 < self.blinkyPos.y  < 500:
                    blink_target = (400, 100)
                else:
                    blink_target = (self.player.x, self.player.y)
            else:
                blink_target = return_target
            if not self.inky_dead:
                if 340 < self.inkyPos.x  < 560 and 340 < self.inkyPos.y < 500:
                    ink_target = (400, 100)
                else:
                    ink_target = (self.player.x, self.player.y)
            else:
                ink_target = return_target
            if not self.pinky_dead:
                if 340 < self.pinkyPos.x  < 560 and 340 < self.pinkyPos.y < 500:
                    pink_target = (400, 100)
                else:
                    pink_target = (self.player.x, self.player.y)
            else:
                pink_target = return_target
            if not self.clyde_dead:
                if 340 < self.clydePos.x  < 560 and 340 < self.clydePos.y < 500:
                    clyd_target = (400, 100)
                else:
                    clyd_target = (self.player.x, self.player.y)
            else:
                clyd_target = return_target
        return [blink_target, ink_target, pink_target, clyd_target]

    def take_damage(self):
        #take_damage game state
        self.direction_command = Direction.RIGHT
        self.powerup = False
        self.power_counter = 0
        self.eaten_ghost = [False, False, False, False]
        self.startup_counter = 0
        self.lives -= 1        
        self.player = Pos(450,663)
        self.playerDirection = Direction.RIGHT
        self.blinkyPos = Pos(56,58)
        self.blinkyDirection = Direction.RIGHT
        self.inkyPos = Pos(380,438) 
        self.inkyDirection = Direction.UP
        self.pinkyPos = Pos(440,438)
        self.pinkyDirection = Direction.UP
        self.clydePos = Pos(500,438)
        self.clydeDirection = Direction.UP
        self.blinky_dead = False
        self.inky_dead = False
        self.clyde_dead = False
        self.pinky_dead = False
        self.reward = -10

    def check_damage(self):
        # add to if not powerup to check if eaten ghosts
        if not self.powerup:
            if (self.player_circle.colliderect(self.blinky.rect) and not self.blinky.dead) or \
                    (self.player_circle.colliderect(self.inky.rect) and not self.inky.dead) or \
                    (self.player_circle.colliderect(self.pinky.rect) and not self.pinky.dead) or \
                    (self.player_circle.colliderect(self.clyde.rect) and not self.clyde.dead):
                if self.lives > 0:
                    self.take_damage()
                else:
                    self.reward = -15
                    self.game_over = True
                    self.moving = False
                    self.startup_counter = 0
        if self.powerup and self.player_circle.colliderect(self.blinky.rect) and self.eaten_ghost[0] and not self.blinky.dead:
            if self.lives > 0:
                self.take_damage()
            else:
                self.reward = -15
                self.game_over = True
                self.moving = False
                self.startup_counter = 0
        if self.powerup and self.player_circle.colliderect(self.inky.rect) and self.eaten_ghost[1] and not self.inky.dead:
            if self.lives > 0:
                self.take_damage()
            else:
                self.reward = -15
                self.game_over = True
                self.moving = False
                self.startup_counter = 0
        if self.powerup and self.player_circle.colliderect(self.pinky.rect) and self.eaten_ghost[2] and not self.pinky.dead:
            if self.lives > 0:
                self.take_damage()
            else:
                self.reward = -15
                self.game_over = True
                self.moving = False
                self.startup_counter = 0
        if self.powerup and self.player_circle.colliderect(self.clyde.rect) and self.eaten_ghost[3] and not self.clyde.dead:
            if self.lives > 0:
                self.take_damage()
            else:
                self.reward = -15
                self.game_over = True
                self.moving = False
                self.startup_counter = 0
        if self.powerup and self.player_circle.colliderect(self.blinky.rect) and not self.blinky.dead and not self.eaten_ghost[0]:
            self.blinky_dead = True
            self.eaten_ghost[0] = True
            self.score += (2 ** self.eaten_ghost.count(True)) * 100
            self.reward = 15
        if self.powerup and self.player_circle.colliderect(self.inky.rect) and not self.inky.dead and not self.eaten_ghost[1]:
            self.inky_dead = True
            self.eaten_ghost[1] = True
            self.score += (2 ** self.eaten_ghost.count(True)) * 100
            self.reward = 15
        if self.powerup and self.player_circle.colliderect(self.pinky.rect) and not self.pinky.dead and not self.eaten_ghost[2]:
            self.pinky_dead = True
            self.eaten_ghost[2] = True
            self.score += (2 ** self.eaten_ghost.count(True)) * 100
            self.reward = 15
        if self.powerup and self.player_circle.colliderect(self.clyde.rect) and not self.clyde.dead and not self.eaten_ghost[3]:
            self.clyde_dead = True
            self.eaten_ghost[3] = True
            self.score += (2 ** self.eaten_ghost.count(True)) * 100
            self.reward = 15

    def set_ghosts_speed(self):
        if self.powerup:
            self.ghost_speeds = [1, 1, 1, 1]
        else:
            self.ghost_speeds = [2, 2, 2, 2]
        if self.eaten_ghost[0]:
            self.ghost_speeds[0] = 2
        if self.eaten_ghost[1]:
            self.ghost_speeds[1] = 2
        if self.eaten_ghost[2]:
            self.ghost_speeds[2] = 2
        if self.eaten_ghost[3]:
            self.ghost_speeds[3] = 2
        if self.blinky_dead:
            self.ghost_speeds[0] = 4
        if self.inky_dead:
            self.ghost_speeds[1] = 4
        if self.pinky_dead:
            self.ghost_speeds[2] = 4
        if self.clyde_dead:
            self.ghost_speeds[3] = 4

    def play_action(self, action):
        self.reward = 0
                
        self.handle_counter()
        self.screen.fill('black')
        self.draw_board()
        
        # Player is a circle so select its center
        self.center = Pos(self.player.x+23, self.player.y + 24)
        
        self.set_ghosts_speed()
        
        self.game_won = True
        for i in range(len(self.level)):
            if 1 in self.level[i] or 2 in self.level[i]:
                self.game_won = False
                
        if self.game_won == True: 
            self.game_over = True
                
        if self.game_over == True:
            reward = -10
            return self.score, self.game_over, self.game_won, self.reward

        
        self.player_circle = pygame.draw.circle(self.screen, 'black', (self.center.x, self.center.y), 20, 2) 
        
        self.draw_player()

        self.blinky = Ghost(self.blinkyPos, self.targets[0], self.ghost_speeds[0], self.blinky_img, self.blinkyDirection, self.blinky_dead,
                self.blinky_box, 0, self)
        self.inky = Ghost(self.inkyPos, self.targets[1], self.ghost_speeds[1], self.inky_img, self.inkyDirection, self.inky_dead,
                    self.inky_box, 1, self)
        self.pinky = Ghost(self.pinkyPos, self.targets[2], self.ghost_speeds[2], self.pinky_img, self.pinkyDirection, self.pinky_dead,
                    self.pinky_box, 2, self)
        self.clyde = Ghost(self.clydePos, self.targets[3], self.ghost_speeds[3], self.clyde_img, self.clydeDirection, self.clyde_dead,
                    self.clyde_box, 3, self)
        
        self.draw_misc()
        
        self.targets = self.get_targets()

        self.turns_allowed = self.check_position()
        
        if self.moving :
            self.move_player()
            if not self.blinky_dead and not self.blinky.in_box:
                self.blinkyPos, self.blinkyDirection = self.blinky.move_blinky()
            else:
                self.blinkyPos, self.blinkyDirection = self.blinky.move_clyde()
            if not self.pinky_dead and not self.pinky.in_box:
                self.pinkyPos, self.pinkyDirection = self.pinky.move_pinky()
            else:
                self.pinkyPos,self.pinkyDirection = self.pinky.move_clyde()
            if not self.inky_dead and not self.inky.in_box:
                self.inkyPos, self.inkyDirection = self.inky.move_inky()
            else:
                self.inkyPos, self.inkyDirection = self.inky.move_clyde()
            self.clydePos, self.clydeDirection = self.clyde.move_clyde()
        
        
        self.check_collisions()
        
        self.check_damage()        
        
        if self.user_input() == False :
            pygame.quit()
            quit()
        
        self.direction_command = action
        
        self.set_direction()
        
        # Joystick movements
        if self.player.x > 900:
            self.player = Pos(-47, self.player.y)
        elif self.player.x < -50:
            self.player = Pos(897, self.player.y)
            
        if self.blinky.in_box and self.blinky_dead:
            self.blinky_dead = False
        if self.inky.in_box and self.inky_dead:
            self.inky_dead = False
        if self.pinky.in_box and self.pinky_dead:
            self.pinky_dead = False
        if self.clyde.in_box and self.clyde_dead:
            self.clyde_dead = False
        
        pygame.display.flip()
        
        return self.score, self.game_over, self.game_won, self.reward

    def stop_game():
        pygame.quit()

    
