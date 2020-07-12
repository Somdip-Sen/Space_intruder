import math
import random
import pygame
from pygame import mixer

pygame.init()  # initialize pygame

total_bullet = 0
total_score = 0
enemy_killed = 0
textX = 10
textY = 10
height = 600
width = 800
flag = False
player_life = 5
armour_health = 12
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((width, height))  # create the screen
font = pygame.font.Font('freesansbold.ttf', 20)
shoot_sound = mixer.Sound("shoot.wav")
enemy_killed_sound = mixer.Sound("kill.wav")
kill_sound = mixer.Sound("invaderkilled.wav")

pygame.display.set_caption("Home made Space Intruder")  # rename the window
# upload all image file to project
player_gun = pygame.image.load("spaceship.png")

boss = pygame.image.load("monster.png")
icon = pygame.image.load("shooter.png")
background = pygame.image.load("Background.png")
pygame.display.set_icon(icon)  # update icon

# for player
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# for bullet
bulletX = []  # we will assign and change it in while loop
bulletY = []  # top pixel of the player
bullet_state = []
bullet_img = pygame.image.load("bullet.png")
enemy_bullet_img = pygame.image.load("bullet_1.png")
bulletY_change = 10  # only y axis movement is allowed for bullet
number_of_bullet = 6
for count in range(number_of_bullet):
    bulletX.append(0)
    bulletY.append(480)
    bullet_state.append(False)  # False = No visual of the bullet to the screen
    # True = bullet starts moving


def draw_player(x, y):  # built the player
    pygame.draw.rect(screen, GREEN, (x, y + 35, 3 * armour_health, 5))  # Total health 36 with 12 life
    pygame.draw.rect(screen, RED, (x + 3 * armour_health, y + 36, 3 * (12 - armour_health), 5))
    screen.blit(player_gun, (x, y))


def draw_enemy(x, y, num):  # built the enemy
    screen.blit(enemy[num], (x, y))


def spawn_enemy():
    x = random.randint(0, width - 20)
    # y = random.randint(0, height//4)
    y = 0
    return x, y


def player_bullet_fire(x, y):
    global bullet_state
    screen.blit(bullet_img, (x + 7, y - 10))


def enemy_bullet_fire(x, y):
    screen.blit(enemy_bullet_img, (x, y))


def collision_detection(x1, x2, y1, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if distance < 20:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score: " + str(total_score), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    game_over_font = pygame.font.Font('game_over.ttf', 160)
    game_over_ = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_, (200, 260))


# for enemy
number_of_enemy = 4
enemy = []
enemyX = []
enemyY = []
# enemyX_change = []
enemyY_change = []
# enemy_bullet_X = []
enemy_bullet_Y = []
enemy_bullet_state = [False] * number_of_enemy

for count in range(number_of_enemy):
    enemy.append(pygame.image.load(f"enemy{random.randint(1, 5)}.png"))
    enemy_x, enemy_y = spawn_enemy()
    enemyX.append(enemy_x)  # x coordinate of enemy
    enemyY.append(enemy_y)  # y coordinate of enemy
    # enemyX_change.append(random.randrange(2, 5))   # enemy speed control in X axis
    enemyY_change.append(random.random() + 0.3)  # enemy speed control in Y axis
    # enemy_bullet_X.append(0)
    enemy_bullet_Y.append(random.randrange(15, height // 4))

if __name__ == "__main__":
    while True:
        screen.fill((49, 54, 122))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Left
                    playerX_change = -4

                elif event.key == pygame.K_RIGHT:  # Right
                    playerX_change = 4

                elif event.key == pygame.K_UP:  # Up
                    playerY_change = -4

                elif event.key == pygame.K_DOWN:  # Down
                    playerY_change = 4

                if event.key == pygame.K_SPACE:
                    shoot_sound.play()
                    for n in range(number_of_bullet):
                        if not bullet_state[n]:
                            bulletX[n] = playerX
                            bulletY[n] = playerY
                            player_bullet_fire(bulletX[n], bulletY[n])
                            bullet_state[n] = True
                            total_score -= 20
                            total_bullet += 1
                            break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        if not 0 < (playerX + playerX_change) < 770:  # restrict the movement inside the screen
            playerX_change = 0
        if not 0 < (playerY + playerY_change) < 550:
            playerY_change = 0
        playerX += playerX_change
        playerY += playerY_change

        # --enemy movement --#
        # --X movement
        # for count in range(number_of_enemy):
        #     enemyX[count] += enemyX_change[count]
        #     if not 0 < enemyX[count] < 750:
        #         enemyX_change[count] *= -1  # direction change
        # -- Y movement
        for count in range(number_of_enemy):
            # if 5 > enemyX[count] or enemyX[count] > 730:
            enemyY[count] += enemyY_change[count]
        for count in range(number_of_enemy):
            if enemyY[count] == random.randrange(15, height - 100):
                enemy_bullet_Y[count] = enemyY[count]

        for n in range(number_of_bullet):
            if bulletY[n] <= 0:
                bulletY[n] = 480
                bullet_state[n] = False

        draw_player(playerX, playerY)

        for count in range(number_of_enemy):
            draw_enemy(enemyX[count], enemyY[count], count)

        # player bullet path
        for n in range(number_of_bullet):
            if bullet_state[n] is True:
                bulletY[n] -= bulletY_change
                player_bullet_fire(bulletX[n], bulletY[n])

        # enemy bullet path
        for count in range(number_of_enemy):
            if enemy_bullet_state[count]:
                if enemy_bullet_Y[count] == playerY and enemyX[count] == playerX or enemy_bullet_Y[count] > 585:
                    enemy_bullet_Y[count] = int(enemyY[count]) + 50
                    enemy_bullet_state[count] = False

                else:
                    enemy_bullet_Y[count] += 2  # bullet speed
                    enemy_bullet_fire(enemyX[count], enemy_bullet_Y[count])
            else:
                if enemy_bullet_Y[count] > 585:
                    enemy_bullet_Y[count] = int(enemyY[count]) + 50
                elif enemyY[count] > enemy_bullet_Y[count] - 5:
                    # enemy_bullet_X[count] = enemyX[count]
                    enemy_bullet_state[count] = True

        # enemy killed
        for count in range(number_of_enemy):
            for n in range(number_of_bullet):
                if collision_detection(bulletX[n], enemyX[count], bulletY[n], enemyY[count]):
                    enemy_killed_sound.play()
                    enemy[count] = pygame.image.load(f"enemy{random.randint(1, 5)}.png")
                    enemyX[count], enemyY[count] = spawn_enemy()
                    enemy_bullet_Y[count] = enemyY[count] + 30
                    # enemyX_change[count] *= random.choice([1, -1])
                    bulletY[n] = 480
                    total_score += 100  # kill enemy score
                    bullet_state[n] = False
                    enemy_killed += 1

        # text
        show_score(textX, textY)
        text = font.render("Enemy Killed : " + str(enemy_killed), True, (255, 255, 255))
        text2 = font.render("Bullet Fired : " + str(total_bullet), True, (255, 255, 255))

        screen.blit(text, (600, 10))
        screen.blit(text2, (600, 40))

        # life deduction
        for i in range(number_of_enemy):
            if enemyY[i] > 575:
                player_life -= 1
                enemy[i] = pygame.image.load(f"enemy{random.randint(1, 5)}.png")
                enemyX[i], enemyY[i] = spawn_enemy()
                kill_sound.play()
        for i in range(number_of_enemy):
            if collision_detection(playerX, enemyX[i], playerY+20, enemy_bullet_Y[i]):  # enemy_bullet player collision
                enemy_bullet_Y[i] = int(enemyY[i]) + 50
                armour_health -= 1
                break

        text3 = font.render("Life Line : " + str(player_life), True, (255, 255, 255))
        screen.blit(text3, (300, 10))

        if player_life == 0 or armour_health == 0:
            flag = True

        # Game Over
        if flag:
            game_over()
            pygame.display.update()
            pygame.time.delay(1000)
            quit()
        else:
            for count in range(number_of_enemy):
                if collision_detection(playerX, enemyX[count], playerY, enemyY[count]):  # enemy player collision
                    sound = mixer.Sound("explosion.wav")
                    sound.play()
                    m, n = playerX, playerY
                    # explosion animation
                    for _ in range(9):
                        screen.blit(pygame.image.load(f"Explosion{_}.png"), (m, n))
                        pygame.time.delay(100)
                        pygame.display.update()

                    # enemy disappearance
                    screen.blit(background, (0, 0))
                    pygame.display.update()
                    flag = True
                    break
        pygame.display.update()
    pygame.quit()
