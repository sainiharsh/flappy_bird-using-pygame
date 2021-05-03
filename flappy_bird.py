import pygame
from pygame.locals import*
import random

# sound config
pygame.mixer.pre_init(frequency = 44100,size = 32,channels = 1,buffer = 512)
# initalize
pygame.init()

gravity = 0.35  # gravity
bird_movement = 0  # move

display_width = 285  
display_height = 510

game_on = True

score = 0
high_score = 0
scoring_timer = 100

# display
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Flappy Bird Game')

speed = pygame.time.Clock()

# background
background_list = ['assets/sprites/background-day.png','assets/sprites/background-night.png']
background = pygame.image.load(random.choice(background_list)).convert()

# base
base = pygame.image.load('assets/sprites/base.png').convert()
base_x_pos = 0

# bird
bird_list = ['assets/sprites/yellowbird-midflap.png','assets/sprites/redbird-midflap.png']
bird_sur = pygame.image.load(random.choice(bird_list)).convert_alpha()
bird_rect = bird_sur.get_rect(center = (25,255))

# pipes
pipes_list = ['assets/sprites/pipe-green.png','assets/sprites/pipe-red.png']
pipe_surface = pygame.image.load(random.choice(pipes_list))
pipes_list2 = []
show_pipe = pygame.USEREVENT
pygame.time.set_timer(show_pipe,1100)
pipe_heights = [200,300,400]

# font
font = pygame.font.Font('EvilEmpire-4BBVK.ttf',35)

game_over_sur = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
game_over_rectangle = game_over_sur.get_rect(center=(143,255))

# sounds
flap_sound = pygame.mixer.Sound('assets/audio/wing.wav')
lose_sound = pygame.mixer.Sound('assets/audio/hit.wav')
scoring_sound = pygame.mixer.Sound('assets/audio/point.wav')
die_sound = pygame.mixer.Sound('assets/audio/die.wav')

 # functions
def base_move():
    game_display.blit(base,(base_x_pos,435))
    game_display.blit(base,(base_x_pos +285,435))    

def adding_pipes():
    random_pipe_height = random.choice(pipe_heights)
    base_pipe = pipe_surface.get_rect(midbottom = (288,random_pipe_height-180))
    top_pipe = pipe_surface.get_rect(midtop = (288,random_pipe_height))
    return base_pipe,top_pipe

def pipes_move(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes    

def show_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 510:
            game_display.blit(pipe_surface,pipe)
        else:
            reverse_pipe = pygame.transform.flip(pipe_surface,False,True)
            game_display.blit(reverse_pipe,pipe)

def collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            lose_sound.play()
            die_sound.play()
            return False
    if bird_rect.top <= -25 or bird_rect.bottom >= 450 :
        return False  
    return True

def bird_rotation(bird):
    bird_flapping = pygame.transform.rotozoom(bird_sur,bird_movement*2.5,1)
    return bird_flapping

def display_score(game):
    if game == 'game_on':
        score_sur = font.render('Score: {}'.format(str(int(score))),True,(255,255,255))
        score_rectangle = score_sur.get_rect(center=(143,30))
        game_display.blit(score_sur,score_rectangle)    
    
    elif game == 'game_over':
        score_sur = font.render('Score: {}'.format(str(int(score))),True,(255,255,255))
        score_rectangle = score_sur.get_rect(center=(143,30))
        game_display.blit(score_sur,score_rectangle) 

        high_score_sur = font.render('High Score: {}'.format(str(int(high_score))),True,(255,255,255))
        high_score_rectangle = high_score_sur.get_rect(center=(143,100))
        game_display.blit(high_score_sur,high_score_rectangle) 

def high_score_update(score,high_score):
    if score > high_score:
        high_score = score
    return high_score    

while True:
    for event in pygame.event.get():
        if event.type == QUIT or ( 
            event.type == KEYDOWN and (
                event.key == K_ESCAPE or 
                event.key == K_q)):
                pygame.quit()
                quit()
        elif event.type == pygame.KEYDOWN and game_on == True:
            if event.key == pygame.K_UP:
                bird_movement = 0  
                bird_movement -= 9
                flap_sound.play()

        elif event.type == pygame.KEYDOWN and game_on== False:
            if event.key == pygame.K_SPACE:
                pipes_list2.clear()
                game_on = True
                bird_rect.center =(25,255)
                bird_movement = 0 
                score = 0

            if (random.choice(background_list) == background_list[0] or background == pygame.image.load(background_list[0])
               and random.choice(pipes_list) == pipes_list[0] or pipe_surface == pygame.image.load(pipes_list[0]) 
               and random.choice(bird_list) == bird_list[0] or bird_sur == pygame.image.load(bird_list[0])):
                background = pygame.image.load(background_list[1])
                pipe_surface = pygame.image.load(pipes_list[1])
                bird_sur = pygame.image.load(bird_list[1])
            else:
                background = pygame.image.load(background_list[0])
                pipe_surface = pygame.image.load(pipes_list[0])     
                bird_sur = pygame.image.load(bird_list[0])
    
        if event.type == show_pipe:
            pipes_list2.extend(adding_pipes())

       
    speed.tick(65)
    game_display.blit(background,(0,0))  

    if game_on:
        bird_movement += gravity
        flappy_bird = bird_rotation(bird_sur)
        bird_rect.centery += int(bird_movement)
        game_display.blit(flappy_bird,bird_rect)
        game_on = collision(pipes_list2)
        pipes_list2 = pipes_move(pipes_list2)  
        show_pipes(pipes_list2)
        score += 0.01
        display_score('game_on')
        scoring_timer -= 1
        if scoring_timer <= 0:
            scoring_sound.play()
            scoring_timer = 100 

    else:
        high_score = high_score_update(score,high_score)
        display_score('game_over')
        game_display.blit(game_over_sur,game_over_rectangle)

    base_move() 
    base_x_pos -= 1             

    if base_x_pos <= -285:
       base_x_pos = 0

    pygame.display.update() 