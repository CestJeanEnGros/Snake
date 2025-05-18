import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)

BLOCK_SIZE = 20
SPEED = 10000

class SnakeGameAI:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        self.frame_it = 0
        
        
    def reset(self):
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y),
                      Point(self.head.x-(3*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.healthy_seed_consumed = 0
        self.drug_seed_consumed = 0
        self.healthy_food = Point(np.inf, np.inf)
        self.drug_food = Point(np.inf, np.inf)
        self._place_food(type="healthy")
        # self._place_food(type="drug")
        self.frame_it=0
        self.u_healthy = 1
        self.u_drug = 1
        self.delay = 0
        self.k = 1
        self.rc = 10

    def _place_food(self, type):
        if type == "healthy":
            x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
            y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
            self.healthy_food = Point(x, y)
            if self.healthy_food in self.snake or self.healthy_food in self.drug_food:
                self._place_food(type)
        else:
            x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
            y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
            self.drug_food = Point(x, y)
            if self.drug_food in self.snake or self.drug_food in self.healthy_food:
                self._place_food(type)
        
    def play_step(self,action):
        self.frame_it+=1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
   
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward =0
        game_over = False
        if self.is_collision() or self.frame_it > 100*len(self.snake):
            game_over = True
            reward = -self.rc
            self.snake.pop()
            return reward,game_over,self.score,self.healthy_seed_consumed,self.drug_seed_consumed, len(self.snake)
        
            
        # 4. place new food or just move
        if self.delay > 0:
            self.delay -= 1
        if self.head == self.healthy_food:
            self.score += 1
            self.healthy_seed_consumed += 1
            reward = self.rc
            self._place_food(type="healthy")
            self.delay += self.u_healthy
        elif self.head == self.drug_food:
            self.score += 1
            self.drug_seed_consumed += 1
            reward = self.rc*self.k
            self._place_food(type="drug")
            self.delay += self.u_drug
        elif self.delay <= 0:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score, self.healthy_seed_consumed, self.drug_seed_consumed, len(self.snake)
    
    def is_collision(self,pt=None):
        if pt is None:
            pt=self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.healthy_food.x, self.healthy_food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, YELLOW, pygame.Rect(self.drug_food.x, self.drug_food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score) + "  Healthy seed:" + str(self.healthy_seed_consumed) + "  Drug seed:" + str(self.drug_seed_consumed), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, action):
        clock_wise=[Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action,[1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action,[0, 1, 0]):
            next_idx =(idx+1) % 4
            new_dir = clock_wise[next_idx]
        else :
            next_idx =(idx-1) % 4
            new_dir = clock_wise[next_idx]

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
            