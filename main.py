import pygame  # importing pygame library
from pygame import mixer  # importing mixer library for sound adding and playing
import random  # random library for using random in our code
import math  # math library for using mathematical function

# intiallize the pygame
pygame.init()

# create a screen
screen = pygame.display.set_mode((800, 600))  # screen resolution is of 800X600
# background
background = pygame.image.load('background.png')  # background image storing

# background sound:
mixer.music.load('back sound.wav')  # background sound player
mixer.music.play(-1)

# title and Icon
pygame.display.set_caption("Ship Of Hope")
icon = pygame.image.load('spaceship.png')  # title logo
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('hero.png')  # player image to be displayed
playerX = 370  # player original position
playerY = 540  # player original position
playerX_change = 0

# ENemy
enemyImg = []  # array system where all enemies image will be stored
enemyX = []  # array system where all enemies X axis position will be stored
enemyY = []  # array system where all enemies Y axis position will be stored
enemyX_change = []  # array system where all enemies movement speed in X axis  will be stored
enemyY_change = []  # array system where all enemies movement speed in Y axis will be stored
num_of_enemies = 25# number of enemy
for i in range(num_of_enemies):  # creating multiple enemy and storing each enemy values in array using for loop
    enemyImg.append(pygame.image.load('villain.png'))
    enemyX.append(random.randint(0, 762))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet:
# 1.ready - you cant se bullet on screen
# 2.fire-the bullet is moving

bulletImg = pygame.image.load('bullet.png')  # image of bullet is stored
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10  # bullet speed
bullet_state = "ready"  # originally we can not see bullet until space is not pressed

# FOnt

score_value = 0
font = pygame.font.Font('Game Of Squids.ttf', 32)  # Font of score and its size

textX = 10  # position of score font in x axis
textY = 10  # position of score font in Y axis

# GAme over text
over_font = pygame.font.Font('Game Of Squids.ttf', 64)  # game over text format and size


# Functions are created which will be invoked during program

def show_score(x, y):  # function for displaying score
    score = font.render("Score:" + str(score_value), True, (0, 255, 255))  # colour and font of score
    screen.blit(score, (x, y))


def game_over_text():  # function for displaying game over text
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))


def player(x, y, ):  # function for spaceship
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):  # funtion for enemy working
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):  # function for bullet movement
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y + 32))  # position of starting bullet is from nose of spaceship


def isCollison(enemyX, enemyY, bulletX, bulletY):  # funtion for colliding of bullet and enemy
    # distance between enemy and bullet
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop

running = True
while running:  # main while loop all action and event are one inside this while so that it remains on screen for all time
    # Red Green Blue colour screen
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():#getting events in que
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -3  # player speed
            if event.key == pygame.K_RIGHT:
                playerX_change = 3  # player speed

            if event.key == pygame.K_SPACE:  # when spacebar is pressed
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser sound.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # checking for boundary of spaceship so that it does not go out
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 764:
        playerX = 764

    # Enemy movemet

    for i in range(num_of_enemies):
        ##game over
        if enemyY[i] > playerY:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2.7 # enemy speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 764:
            enemyX_change[i] = -2.7 # enemy speed
            enemyY[i] += enemyY_change[i]

        # collison of bullet and enemy
        collison = isCollison(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison:
            explosion = mixer.Sound('collison.wav')
            explosion.play()
            bulletY = 570
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 762)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
