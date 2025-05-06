import pygame
from pygame import mixer
import math
import random

from pygame.examples.aliens import Score

pygame.init()
#for game window
screen=pygame.display.set_mode((800,600))
running=True

#for sound
mixer.music.load(".\\images\\background.wav")
mixer.music.play(-1)

#Setting the title of game window
pygame.display.set_caption('My Space Game')
#for setting the icon of game
icon=pygame.image.load('.\\images\\ufo.png')
pygame.display.set_icon(icon)

#For player
playerimg=pygame.image.load(".\\images\\player.png")
playerX=370
playerY=480
player_change=0

def player(playerX,playerY):
    screen.blit(playerimg,(playerX,playerY))

# for enemy
enemyimg=pygame.image.load(".\\images\\enemy.png")
enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('.\\images\\enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

#for bullet
bulletImg=pygame.image.load(('.\\images\\bullet.png'))
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state='ready'

#Score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)

textX=10
textY=10

#Game over
over_font=pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score=font.render("Score : " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))


def fire_Bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletImg,(x+16,y+10))

def bullet(x,y):
    screen.blit(bulletImg,(x,y))

#Collision
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2)+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False

#for setting the background
background=pygame.image.load('.\\images\\background.png')

while running:
    #to close the game window
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                player_change=-3
            elif event.key==pygame.K_RIGHT:
                player_change=3
            elif event.key==pygame.K_SPACE:
                if bullet_state=='ready':
                    bullet_sound=mixer.Sound('.\\images\\laser.wav')
                    bullet_sound.play()
                    bulletX=playerX
                    fire_Bullet(bulletX,bulletY)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                player_change=0

    #for setting the boundary of the player
    if playerX<=0:
        playerX=0
    if playerX>=740:
        playerX=740
    playerX=playerX+player_change

    #Enemy movement
    for i in range(num_of_enemies):
        #Game over
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break

        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=2
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-2
            enemyY[i]+=enemyY_change[i]

        #collision
        collision=isCollision(enemyX[i],enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound=mixer.Sound('.\\images\\explosion.wav')
            explosionSound.play()
            bulletY=480
            bullet_state="ready"
            score_value+=1
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)
    #for bullet
    if bulletY<=0:
        bulletY=480
        bullet_state='ready'

    if bullet_state=='fire':
        fire_Bullet(bulletX,bulletY)
        bulletY=bulletY-bulletY_change


    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
