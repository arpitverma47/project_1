import pygame as py
import math
import random
from pygame import mixer

# print(py.__doc__)
# print(py.__dict__)

# initialize the pygame
py.init()

# for blank screen

screen = py.display.set_mode((800, 600))
#Title and icon

py.display.set_caption("Space Invader")
icon = py.image.load("spaceship (3).png")
py.display.set_icon(icon)


# Background image


background = py.image.load("Background.png")

# background music
mixer.music.load("background.wav")
mixer.music.play(-1)


# player

playerimg = py.image.load("spaceship (3).png")
playerX = 370
playerY = 480
playerX_change = 0


# bullen icon
bulletimg = py.image.load("bullet (1).png")
bulletX = 0
bulletY = 480

bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"  # ready:- not showing the bullet but it is in the game


# score

score_value = 0
font = py.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10


# Enemy


enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemy = 8
for i in range(num_of_enemy):

    enemyimg.append(py.image.load("enemy (1).png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

over_font = py.font.Font("freesansbold.ttf", 64)


def player(x, y):
    screen.blit(playerimg, (x, y))


# for enemy


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


# for bullet

def fire_bullet(x, y):
    global bullet_state
    screen.blit(bulletimg, (x+16, y+10))
    bullet_state = "fire"

# for killing the enemy


def iscollision(enemyX, bulletX, enemyY, bulletY):
    distance = math.sqrt(math.pow((enemyX-bulletX), 2) +
                         math.pow((enemyY-bulletY), 2))
    if distance < 27:
        return True
    else:
        return False

# for scoring


def show_score(x, y):
    score = font.render("score:"+str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# for holding the display

running = True

while running:
    screen.fill((0, 0, 0))  # for filling colour

    screen.blit(background, (0, 0))

    # bullet implement

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

        if event.type == py.KEYDOWN:
            if event.key == py.K_LEFT:
                playerX_change = -3
            elif event.key == py.K_RIGHT:
                playerX_change = 3

            elif event.key == py.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX

                    fire_bullet(bulletX, bulletY)

        if event.type == py.KEYUP or event.type == py.K_RIGHT:
            playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # for enemy movement

    for i in range(num_of_enemy):
        if enemyY[i] > 440:
            for j in range(num_of_enemy):
                enemyY[j] = 2000

            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 750:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        collision = iscollision(enemyX[i], bulletX, enemyY[i], bulletY)
        if collision:
            explsion_sound = mixer.Sound("explosion.wav")
            explsion_sound.play()
            bullet_state = "ready"
            bulletY = 480
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # for regenerate of bullet
    if bulletY == 45:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # for  collision between enemy and bullet

    player(playerX, playerY)
    show_score(textX, textY)

    py.display.update()
