import pygame
import sys
import traceback
import bullet
import plant
import enemy

from pygame.locals import *
from random import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 560, 495
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")

background = pygame.image.load("images/background.png").convert()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

bullet_sound = pygame.mixer.Sound("music/bullet.wav")
bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("music/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("music/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("music/me_down.wav")
me_down_sound.set_volume(0.2)

def addEnemies(group1, num):
    for i in range(num):
        e1 = enemy.Enemy(bg_size)
        group1.add(e1)

def inc_speed(target, inc):
    for each in target:
        each.speed += inc

def drawPlant():
    global life_num
    if p.active:
        screen.blit(p.image1, p.rect)
    else:
        me_down_sound.play()
        life_num -= 1
        p.reset()
    pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

def drawEnemy():
    global score
    for en in enemies:
        if en.active:
            en.move()
            screen.blit(en.image, en.rect)
        elif not (delay % 3):
            enemy1_down_sound.play()
            score += 300
            en.reset()

def drawScoreLife():
    if life_num:
        for i in range(life_num):
            screen.blit(life_image, \
                        (width - 10 - (i + 1) * life_rect.width, \
                         height - 10 - life_rect.height))

    scoreText = scoreFont.render("Level %s Score : %s" % (str(level), str(score)), True, WHITE)
    screen.blit(scoreText, (10, 5))

def continueOrQuit():
    global record_score, score, life_num
    # 背景音乐停止
    # pygame.mixer.music.stop()

    # 停止全部音效
    pygame.mixer.stop()

    record_scoreText = scoreFont.render("Best : %d" % record_score, True, WHITE)
    screen.blit(record_scoreText, (50, 50))

    gameoverText1 = gameoverFont.render("Your Score:", True, WHITE)
    gameoverText1Rect = gameoverText1.get_rect()
    gameoverText1Rect.left, gameoverText1Rect.top = \
        (width - gameoverText1Rect.width) // 2, height // 3
    screen.blit(gameoverText1, gameoverText1Rect)

    gameoverText2 = gameoverFont.render(str(score), True, (255, 255, 255))
    gameoverText2Rect = gameoverText2.get_rect()
    gameoverText2Rect.left, gameoverText2Rect.top = \
        (width - gameoverText2Rect.width) // 2, \
        gameoverText1Rect.bottom + 10
    screen.blit(gameoverText2, gameoverText2Rect)

    again_rect.left, again_rect.top = \
        (width - again_rect.width) // 2, \
        gameoverText2Rect.bottom + 50
    screen.blit(again_image, again_rect)

    gameover_rect.left, gameover_rect.top = \
        (width - again_rect.width) // 2, \
        again_rect.bottom + 10
    screen.blit(gameover_image, gameover_rect)

    if pygame.mouse.get_pressed()[0]:
        if score > record_score:
            record_score = score
            with open("record.txt", "w") as f:
                f.write(str(score))

        pos = pygame.mouse.get_pos()

        if again_rect.left < pos[0] < again_rect.right and \
                again_rect.top < pos[1] < again_rect.bottom:
            # 调用main函数，重新开始游戏
            life_num = 3
            score = 0
            play()
        elif gameover_rect.left < pos[0] < gameover_rect.right and \
                gameover_rect.top < pos[1] < gameover_rect.bottom:
            pygame.quit()
            sys.exit()

level = 1
score = 0
scoreFont = pygame.font.Font(None, 36)

life_image = pygame.image.load("images/plant.png").convert_alpha()
life_rect = life_image.get_rect()
life_num = 3

with open("record.txt", "r") as f:
    record_score = int(f.read())

gameoverFont = pygame.font.Font(None,48)
again_image = pygame.image.load("images/again.png").convert_alpha()
again_rect = again_image.get_rect()
gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
gameover_rect = gameover_image.get_rect()

p = plant.Plane(bg_size)

enemies = pygame.sprite.Group()
addEnemies(enemies, 10)

bullet1 = []
bullet_index = 0
BULLET_NUM = 4
for i in range(BULLET_NUM):
    bullet1.append(bullet.Bullet1(p.rect.midtop))

delay = 100

INVINCIBLE_TIME = USEREVENT + 2

switch_image = True
clock = pygame.time.Clock()

recorded = False

running = True

def play():

    global bullet_index, delay, bg1_top, bg2_top, \
        bullets, level, switch_image

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # screen.blit(background, (0, 0))

        if level == 1 and score >= 10000:
            level = 2
            upgrade_sound.play()
            addEnemies(enemies, 3)
            inc_speed(enemies, 1)
        elif level == 2 and score >= 50000:
            level = 3
            upgrade_sound.play()
            addEnemies(enemies, 5)
            inc_speed(enemies, 1)
        elif level == 3 and score >= 100000:
            level = 4
            upgrade_sound.play()
            addEnemies(enemies, 5)
            inc_speed(enemies, 1)
        elif level == 4 and score >= 200000:
            level = 5
            upgrade_sound.play()
            addEnemies(enemies, 5)
            inc_speed(enemies, 1)

        screen.blit(background, (0, 0))

        if life_num:
            key_pressed = pygame.key.get_pressed()

            bullets = bullet1

            if key_pressed[K_w] or key_pressed[K_UP]:
                p.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                p.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                p.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                p.moveRight()
            if key_pressed[K_SPACE]:
                if not (delay % 10):
                    bullet_sound.play()
                    bullets[bullet_index].reset(p.rect.midtop)
                    bullet_index = (bullet_index + 1) % BULLET_NUM

            for b in bullets:
                b.move()
                screen.blit(b.image, b.rect)
                enemyHit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                if enemyHit:
                    b.active = False
                    for e in enemyHit:
                        e.active = False
            drawEnemy()

            enemiesDown = pygame.sprite.spritecollide(p, enemies, False, pygame.sprite.collide_mask)
            if enemiesDown and not p.invincible:
                p.active = False
                for e in enemiesDown:
                    e.active = False
            drawPlant()

        elif life_num == 0:
            continueOrQuit()

        drawScoreLife()
        # 切换图片
        if not (delay % 5):
            switch_image = not switch_image

        delay = (delay - 1) if delay else 100

        pygame.display.flip()
        clock.tick(60)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    try:
        play()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
