import pygame , random

pygame.init()

WIN_WIDTH = 1000
WIN_HEIGHT = 400

screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pygame.display.set_caption("Feed The Dragon Game")

#set FPS
FPS = 60
clock = pygame.time.Clock()
#set values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 8
COIN_ST_VELOCITY = 8
COIN_ACCELERATION = .5
BUFFER_DISTANCE = -100
score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_ST_VELOCITY
#set color
GREEN = (0,255,0)
DRGREEN = (10,50,10)
WHITE = (255,255,255)
BLACK = (0,0,0)
#set txt and font
font = pygame.font.Font('game_assets/AttackGraffiti.ttf',32)
score_txt = font.render("Score: " + str(score),True,GREEN,DRGREEN)
score_rect = score_txt.get_rect(topleft = (10,10))

title_txt = font.render("Feed The Dragon",True,GREEN,WHITE)
title_rect = title_txt.get_rect(centerx = WIN_WIDTH//2)
title_rect.y = 10

lives_txt = font.render("Lives: " + str(player_lives),True,GREEN,DRGREEN)
lives_rect = score_txt.get_rect(topright = (WIN_WIDTH-10,10))

game_over_txt = font.render("GAMEOVER!",True,GREEN,DRGREEN)
game_over_rect = game_over_txt.get_rect(center = (WIN_WIDTH//2,WIN_HEIGHT//2))

continue_txt = font.render("PRESS ANY KEY TO CONTINUE",True,GREEN,DRGREEN)
continue_rect = continue_txt.get_rect(center = (WIN_WIDTH//2 , WIN_HEIGHT//2 + 32))
#set music
coin_snd = pygame.mixer.Sound('game_assets/coin_sound.wav')
miss_snd = pygame.mixer.Sound('game_assets/miss_sound.wav')
miss_snd.set_volume(.1)
# game_bgsnd = pygame.mixer_music('game_assets/ftd_background_music.wav')
pygame.mixer.music.load('game_assets/ftd_background_music.wav')
#set images
player_img = pygame.image.load('game_assets/dragon_right.png')
player_rect = player_img.get_rect(topleft = (32,WIN_HEIGHT//2))

coin_img = pygame.image.load('game_assets/coin.png')
coin_rect = player_img.get_rect()
coin_rect.x = WIN_WIDTH+BUFFER_DISTANCE
coin_rect.y = random.randint(64,WIN_HEIGHT-32)

pygame.mixer.music.play(-1)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN and running == False:
        #     player_lives = PLAYER_STARTING_LIVES
        #     score = 0
        #     running = True
    
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.top >64:
        player_rect.y -= PLAYER_VELOCITY
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_rect.bottom <WIN_HEIGHT:
        player_rect.y += PLAYER_VELOCITY
    if coin_rect.x<0:  #coin missed
        player_lives -= 1 
        miss_snd.play()
        coin_rect.x = WIN_WIDTH+BUFFER_DISTANCE
        coin_rect.y = random.randint(64,WIN_HEIGHT-32)
    else:
        coin_rect.x -= coin_velocity
    #collision.
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_snd.play()
        coin_rect.x = WIN_WIDTH+BUFFER_DISTANCE
        coin_rect.y = random.randint(64,WIN_HEIGHT-32)
        coin_velocity += COIN_ACCELERATION

    score_txt = font.render("Score: " + str(score),True,GREEN,DRGREEN)
    lives_txt = font.render("Lives: " + str(player_lives),True,GREEN,DRGREEN)

    if player_lives == 0:
        screen.blit(game_over_txt,game_over_rect)
        screen.blit(continue_txt,continue_rect)
        pygame.display.update()

        #pause game until player presees any key
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    player_rect.y = WIN_HEIGHT//2
                    coin_velocity=  COIN_ST_VELOCITY
                    pygame.mixer.music.play(-1,0.0)
                    is_paused = False
                else: #quit
                    if ev.type == pygame.QUIT:
                        is_paused = False
                        running = False
    screen.fill(BLACK)

    screen.blit(score_txt,score_rect)
    screen.blit(title_txt,title_rect)
    screen.blit(lives_txt,lives_rect)

    pygame.draw.line(screen,WHITE,(0,64),(WIN_WIDTH,64),3)

    screen.blit(player_img,player_rect)
    screen.blit(coin_img,coin_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()