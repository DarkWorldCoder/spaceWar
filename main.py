import pygame
from pygame import mixer
import sys
import os
pygame.font.init()
mixer.init()

BORDER = pygame.Rect(500,0,5,700)
WIN = pygame.display.set_mode((1000,700))
WIDTH , HEIGHT = 50,40
BACKGROUND = pygame.image.load(os.path.join("Assets","space.png"))
REDPLYR = pygame.image.load(os.path.join("Assets","spaceship_red.png"))
YELLOWPLYR = pygame.image.load(os.path.join("Assets","spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOWPLYR,(WIDTH,HEIGHT)),90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(REDPLYR,(WIDTH,HEIGHT)),270)
SPEED = 10
BULLET_SPEED = 15
RED = (255,0,0)
YELLOW = (255,255,0)
MAX_BULLET = 3
YELLOW_HIT = pygame.USEREVENT +1
RED_HIT = pygame.USEREVENT +2

HEALTH_FONT = pygame.font.SysFont('Courier', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):

    WIN.blit(BACKGROUND,(0,0))
    pygame.draw.rect(WIN,"white",BORDER)
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, "white")
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, "white")
    WIN.blit(red_health_text, (700, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in yellow_bullets:
	    pygame.draw.rect(WIN,YELLOW,bullet)
	
def control_yellow(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x >0:#LEFT
            yellow.x -= SPEED
    if keys_pressed[pygame.K_d] and yellow.x <460:#LEFT
            yellow.x += SPEED
    if keys_pressed[pygame.K_w] and yellow.y >0 :#LEFT
            yellow.y -= SPEED
    if keys_pressed[pygame.K_s] and yellow.y <650:#LEFT
            yellow.y += SPEED 
def control_red(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x >510:#LEFT
            red.x -= SPEED
    if keys_pressed[pygame.K_RIGHT] and red.x <  960:#Right
            red.x += SPEED
    if keys_pressed[pygame.K_UP] and red.y >0:#LEFT
            red.y -= SPEED
    if keys_pressed[pygame.K_DOWN] and red.y <650:#LEFT
            red.y += SPEED 
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    
	
    for bullet in yellow_bullets:
        bullet.x += BULLET_SPEED
        
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            
        elif bullet.x >1000 :
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)    
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, "WHITE")
    WIN.blit(draw_text, (250, 350))
    pygame.display.update()
    pygame.time.delay(5000)
def main():
    red = pygame.Rect(900,400,WIDTH,HEIGHT)
    yellow = pygame.Rect(60,400,WIDTH,HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health =10
    yellow_health=10
    
    while True:
        clock = pygame.time.Clock()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET:
                                
                    bullet = pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2-2,10,5)

                    yellow_bullets.append(bullet) 
                    mixer.music.load(os.path.join("Assets","Gun+Silencer.mp3"))
                    mixer.music.set_volume(0.2)
                    mixer.music.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) <MAX_BULLET:
                    bullet = pygame.Rect(red.x,red.y+red.height//2-2,10,5)
                    red_bullets.append(bullet)
                    mixer.music.load(os.path.join("Assets","Grenade+1.mp3"))
                    mixer.music.set_volume(0.2)
                    mixer.music.play() 
            if event.type == RED_HIT:
                red_health -=1
            if event.type == YELLOW_HIT:
                yellow_health -=1
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break


           
        
		
        keys_pressed = pygame.key.get_pressed()
		
        control_yellow(keys_pressed,yellow)
        control_red(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)
        pygame.display.update()
if __name__ == "__main__":
    main()