""" 
Title: Space Invaders
Author: Caden Jamason
Date: 03/02/2022
Course: Introduction to Computer Programming, 2
Description: A clone of space invaders
"""

import random
import math

import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.jpg")

# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
title = "Space Invaders"
pygame.display.set_caption(title)
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numOfEnemies = 6

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load("alien-1.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# Missile
missileImg = pygame.image.load("missile.png")
missileX = 0
missileY = 480
missileX_change = 0
missileY_change = -0.4
# Ready - You can't see the missile on the screen
# Fire - The missile is on the screen and currently moving
missileState = "ready"


# Font
scoreValue = 0
font = pygame.font.Font("freesansbold.ttf", 32)


textX = 10
textY = 10

# Game Over text
overFont = pygame.font.Font("freesansbold.ttf", 64)


def showScore(x, y):
    score = font.render("Score: " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))


def gameOverText():
    overText = overFont.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(overText, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fireMissile(x, y):
    global missileState
    missileState = "fire"
    screen.blit(missileImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt(
        math.pow(enemyX - missileX, 2) + math.pow(enemyY - missileY, 2)
    )
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # RGB - red, green, blue
    screen.fill((21, 21, 21))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_LEFT:
                playerX_change = -0.7
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.7
            if event.key == pygame.K_SPACE:
                if missileState == "ready":
                    missileSound = mixer.Sound("laser.wav")
                    missileSound.play()
                    # Get the current x coordinate of the spaceship
                    missileX = playerX
                    fireMissile(missileX, missileY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(numOfEnemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            gameOverText()
            break

        # Enemy movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        if missileY <= -64:
            missileY = 480
            missileState = "ready"

        if missileState == "fire":
            fireMissile(missileX, missileY)
            missileY += missileY_change

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], missileX, missileY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            missileY = 480
            missileState = "ready"
            scoreValue += 1
            print(scoreValue)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
