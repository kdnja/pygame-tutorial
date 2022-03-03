""" 
Title: Space Invaders
Author: Caden Jamason
Date: 03/02/2022
Course: Introduction to Computer Programming, 2
Description: A clone of space invaders
"""
# ----------------------------------------- Packages --------------------------------------------- #
import random
import math

# Pygame
import pygame

# Used for audio
from pygame import mixer

# Initialize Pygame
pygame.init()
# ------------------------------------------------------------------------------------------------ #


# ------------------------------------------ Screen ---------------------------------------------- #
# Create the screen
screen = pygame.display.set_mode((800, 600))
# ------------------------------------------------------------------------------------------------ #


# ---------------------------------------- Background -------------------------------------------- #
# Loads the background
background = pygame.image.load("background.jpg")
# ------------------------------------------------------------------------------------------------ #


# -------------------------------------- Background Music ---------------------------------------- #
# Loads and loops the background music
mixer.music.load("background.wav")
mixer.music.play(-1)
# ------------------------------------------------------------------------------------------------ #


# --------------------------------------- Title and Icon ----------------------------------------- #
# Sets the caption of the program to "Space Invaders"
title = "Space Invaders"
pygame.display.set_caption(title)
# Sets the icon of the program to a spaceship
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
# ------------------------------------------------------------------------------------------------ #


# -------------------------------------------- Player -------------------------------------------- #
# Loads the player image
playerImg = pygame.image.load("spaceship.png")
# Initialize player coordinates
playerX = 370
playerY = 480
playerX_change = 0
# ------------------------------------------------------------------------------------------------ #


# -------------------------------------------- Enemy --------------------------------------------- #
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
# ------------------------------------------------------------------------------------------------ #


# ----------------------------------------- Missile ---------------------------------------------- #
# Image associated with the missile
missileImg = pygame.image.load("missile.png")
# Coordinates of the missile
missileX = 0
missileY = 480
# Change over time of the missile's coordinates
missileX_change = 0
missileY_change = -1
# Ready - You can't see the missile on the screen
# Fire - The missile is on the screen and currently moving
missileState = "ready"
# ------------------------------------------------------------------------------------------------ #


# ------------------------------------------- Font ----------------------------------------------- #
# Score value
scoreValue = 0
# Creates a new Font for the score
font = pygame.font.Font("freesansbold.ttf", 32)
# Coordinates of the score text
textX = 10
textY = 10

# Game Over text
overFont = pygame.font.Font("freesansbold.ttf", 64)
# ------------------------------------------------------------------------------------------------ #


# ----------------------------------------- Functions -------------------------------------------- #
# Show the player's score in the top left corner
def showScore(x, y):
    score = font.render("Score: " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Show a big "GAME OVER" in the middle of the screen when the player loses
def gameOverText():
    overText = overFont.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(overText, (200, 250))


# Changes the position of the player
def player(x, y):
    screen.blit(playerImg, (x, y))


# Changes the position of the current enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Display a missile in front of the player's spaceship
def fireMissile(x, y):
    global missileState
    missileState = "fire"
    screen.blit(missileImg, (x + 16, y + 10))


# Detect collision between the enemy and the spaceship using distance formula
def isCollision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt(
        math.pow(enemyX - missileX, 2) + math.pow(enemyY - missileY, 2)
    )
    # If the distance between the enemy is less than 27 pixels, return True
    if distance < 27:
        return True
    else:
        return False


# ------------------------------------------------------------------------------------------------ #


# ---------------------------------------- Game Loop --------------------------------------------- #
running = True
while running:
    # RGB - red, green, blue
    screen.fill((21, 21, 21))
    # Display a background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # If the program is closed using the X icon, prevent game from looping
        if event.type == pygame.QUIT:
            running = False

        # If a key is pressed, check whether it's escape, right, left, or space
        if event.type == pygame.KEYDOWN:
            # If the key is escape, quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            # If the key is left, make the spaceship go left
            if event.key == pygame.K_LEFT:
                playerX_change = -0.7
            # If the key is right, make the spaceship go right
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.7
            # If the key is space, check if the missile state is ready
            if event.key == pygame.K_SPACE:
                if missileState == "ready":
                    # Play a laser sound
                    missileSound = mixer.Sound("laser.wav")
                    missileSound.play()
                    # Set the x coordinate of the missile to the x coordinate of the spaceship
                    missileX = playerX
                    # Fire a missile from the player's last known position
                    fireMissile(missileX, missileY)
        # If a key is released, check whether it's left or right
        if event.type == pygame.KEYUP:
            # If the key is left or right, set the player's change in x to zero (not moving)
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement
    # Change the player's x-position based on the x-change value
    playerX += playerX_change
    # If the player goes too far to the left, return them to the playfield
    if playerX <= 0:
        playerX = 0
    # If the player goes too far to the right, return them to the playfield
    elif playerX >= 736:
        playerX = 736

    # For each enemy
    for i in range(numOfEnemies):
        # If an enemy's y-position is more than 440,
        # remove the enemies from the screen, display "game over", and break the loop
        if enemyY[i] > 440:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            gameOverText()
            break

        # Enemy movement
        # The current enemy changes its x-position based on its own x-change value
        enemyX[i] += enemyX_change[i]
        # If the current enemy's x-position is less than or equal to zero,
        # make the current enemy move right constantly and move down a little
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        # If the current enemy's x-position is more than or equal to 736,
        # make the current enemy move left constantly and move down a little
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]
        # If the missile is off-screen,
        # reset the missile's y-position and change its state to "ready"
        if missileY <= -64:
            missileY = 480
            missileState = "ready"
        # If the missile is fired,
        # call the associated function and change its y-value based on its y-change value
        if missileState == "fire":
            fireMissile(missileX, missileY)
            missileY += missileY_change

        # Checks for collision beteween enemy and missile
        collision = isCollision(enemyX[i], enemyY[i], missileX, missileY)
        # If there is a collision between enemy and missile,
        # play an explosion sound, reset the missile, increase and update the score,
        # and "respawn" the enemy by moving them to a random given position on the screen
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            missileY = 480
            missileState = "ready"
            scoreValue += 1
            print(scoreValue)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        # Update the current enemy's position
        enemy(enemyX[i], enemyY[i], i)

    # Update the player's position
    player(playerX, playerY)
    # Show the current score
    showScore(textX, textY)
    # Update the entire screen
    pygame.display.update()
# ------------------------------------------------------------------------------------------------ #
