import pygame as pg 
from random import randrange
pg.font.init()


WINDOW =700
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW-TILE_SIZE//2, TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pg.rect.Rect([ 0,0,TILE_SIZE-2,TILE_SIZE-2])
snake.center = get_random_position()
food = snake.copy()
food.center =get_random_position()
length = 1
score =0
segments = [snake.copy()]
snake_dir = (0,0)
time, timestep = 0,110
screen=pg.display.set_mode([WINDOW]*2)
clock=pg.time.Clock()
dirs = {pg.K_w: 1,pg.K_d: 1,pg.K_s: 1,pg.K_a: 1}

font = pg.font.Font('freesansbold.ttf', 32)
text = font.render(f'Score: {score}', True, 'green', 'blue')

def drawGrid():
    screen.fill("black")
    for x in range(0, WINDOW, TILE_SIZE):
        for y in range(0, WINDOW, TILE_SIZE):
            rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pg.draw.rect(screen, (74,74,74), rect, 1)

def drawScore():
    text = font.render(f'Score: {score}', True, 'green')
    screen.blit(text,(0,0))

while True:
    
    for event in pg.event.get():
        if event.type==pg.QUIT:
            exit()
        if event.type==pg.KEYDOWN:
            if event.key ==pg.K_w and dirs[pg.K_w]:
                snake_dir = (0,-TILE_SIZE)
                dirs = {pg.K_w: 1,pg.K_d: 1,pg.K_s: 0,pg.K_a: 1}
            if event.key ==pg.K_s and dirs[pg.K_s]:
                snake_dir = (0,TILE_SIZE)
                dirs = {pg.K_w: 0,pg.K_d: 1,pg.K_s: 1,pg.K_a: 1}
            if event.key ==pg.K_a and dirs[pg.K_a]:
                snake_dir = (-TILE_SIZE,0)
                dirs = {pg.K_w: 1,pg.K_d: 0,pg.K_s: 1,pg.K_a: 1}
            if event.key ==pg.K_d and dirs[pg.K_d]:
                snake_dir = (TILE_SIZE,0)
                dirs = {pg.K_w: 1,pg.K_d: 1,pg.K_s: 1,pg.K_a: 0}
    drawGrid()
    
    self_eating =  pg.Rect.collidelist(snake, segments[:-1]) !=-1
    if snake.left < 0 or snake.right>WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dit = 1,(0,0)
        segments = [snake.copy()]
        score=0

    food_in_tail = pg.Rect.collidelist(food, segments[:-1]) !=-1
    if food_in_tail:
            food.center = get_random_position()
            
    #check food-snake collision
    if snake.center == food.center:
        food.center = get_random_position()
        length+=1
        score+=1
    #Draw snake
    [pg.draw.rect(screen, 'green',segment) for segment in segments]
    #Draw food 
    pg.draw.rect(screen, "red", food)
    #Draw score
    drawScore()
    #Move snake
    time_now = pg.time.get_ticks()
    if time_now-time> timestep:
        time=time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]
    pg.display.flip()
    clock.tick(60)
