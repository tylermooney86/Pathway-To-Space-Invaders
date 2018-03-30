# Pathway To Space Invaders
# by Tyler Mooney

import turtle
import os
import math
import random
import time
from pygame import mixer

#set up screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Pathway To Space Invaders")

#background music
mixer.init()
mixer.music.load("sounds/music.wav")
mixer.music.play(loops=-1)

#register shapes
turtle.register_shape("images/chris.gif")
turtle.register_shape("images/ship.gif")
turtle.register_shape("images/bullet.gif")
turtle.register_shape("images/explosionblue.gif")

#draw title
screen.bgpic("images/background.gif")
title_string = "PATHWAY TO SPACE"
title_pen = turtle.Turtle()
title_pen.hideturtle()
title_pen.speed(1)
title_pen.color("white")
title_pen.penup()
title_pen.setposition(0,200)
title_pen.write(title_string,False,align="center",font=("space_invaders.ttf", 60,"bold"))
time.sleep(0.5)

title_string = "INVADERS!"
title_pen.setposition(0,0)
title_pen.write(title_string,False,align="center",font=("space_invaders.ttf", 80,"bold"))
title_pen.hideturtle()
time.sleep(1)

title_string = "BY: TYLER MOONEY"
title_pen.setposition(0,-200)
title_pen.write(title_string,False,align="center",font=("space_invaders.ttf", 40,"bold"))
title_pen.hideturtle()
time.sleep(3)

screen.clear()
screen.bgpic("images/background_with_logo.gif")

#draw border
border_pen = turtle.Turtle()
border_pen.speed(5)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-400,-350)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    if side%2 == 0:
        border_pen.fd(800)
        border_pen.lt(90)
    else:
        border_pen.fd(700)
        border_pen.lt(90)
border_pen.hideturtle()


#Score
score = 0
score_pen = turtle.Turtle()
score_pen.penup()
score_pen.speed(0)
score_pen.color("white")
score_pen.setposition(-390,320)
scorestring = "SCORE: %s" %score
score_pen.write(scorestring,False,align="left",font=("space_invaders.ttf", 18, "normal"))
score_pen.hideturtle()

#create player
player = turtle.Turtle()
player.hideturtle()
player.penup()
player.color("blue")
player.shape("images/ship.gif")
player.speed(0)
player.setposition(0,-300)
player.setheading(90)
player.showturtle()

playerspeed = 15

number_of_enemies = 5
enemies = []
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.shape("images/chris.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-300,300)
    y = random.randint(150,300)
    enemy.setposition(x,y)

enemyspeed = 6

#create bullet
bullet = turtle.Turtle()
bullet.shape("images/bullet.gif")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.hideturtle()

bulletspeed = 40
bulletstate = "ready"
bulletcount = 0

#create enemy bullet
enemy_bullet = turtle.Turtle()
enemy_bullet.shape("images/bullet.gif")
enemy_bullet.penup()
enemy_bullet.speed(0)
enemy_bullet.setheading(270)
enemy_bullet.hideturtle()

#create enemy bullet
enemy_bullet2 = turtle.Turtle()
enemy_bullet2.shape("images/bullet.gif")
enemy_bullet2.penup()
enemy_bullet2.speed(0)
enemy_bullet2.setheading(270)
enemy_bullet2.hideturtle()

enemy_bullet_speed = 5
enemy_firing = False
enemy2_firing = False

#create explosion
explosion = turtle.Turtle()
explosion.shape("images/explosionblue.gif")
explosion.penup()
explosion.speed(0)
explosion.hideturtle()

#move player left and right
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -380:
        x = -380
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 380:
        x = 380
    player.setx(x)

def fire_bullet():
        os.system("aplay sounds/shoot.wav&")
        x = player.xcor()
        y = player.ycor() + 15
        bullet.setposition(x,y)
        bullet.showturtle()

def fire_enemy_bullet(bullet,x,y):
    os.system("aplay sounds/shoot2.wav&")
    bullet.setposition(x,y)
    bullet.showturtle()

def move_enemy_bullet(bullet):
    y = bullet.ycor()
    y -= enemy_bullet_speed
    bullet.sety(y)


def isCollision(t1,t2):
    dist = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if dist < 20:
        return True
    else:
        return False

def explode(x,y):
    #create explosion
    explosion.setposition(x,y)
    explosion.showturtle()
    time.sleep(0.2)
    explosion.hideturtle()

#create keybindings
turtle.listen()
turtle.onkey(move_left,"Left")
turtle.onkey(move_right,"Right")
turtle.onkey(fire_bullet,"space")

gameover = False
#create main loop
while True:
    for enemy in enemies:
        #move enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        #move down and reverse enemy
        if enemy.xcor() > 380:
            enemyspeed *= -1
            for e in enemies:
                y = e.ycor()
                y -= 50
                e.sety(y)

        if enemy.xcor() < -380:
            enemyspeed *= -1
            for e in enemies:
                y = e.ycor()
                y -= 50
                e.sety(y)

        #fire enemy bullets
        if enemy_firing == False:
            if random.randint(1,5) == 1:
                enemy_firing = True
                fire_enemy_bullet(enemy_bullet,enemy.xcor(),enemy.ycor())
        else:
            move_enemy_bullet(enemy_bullet)

        if enemy2_firing == False:
            if random.randint(1,10) == 1:
                enemy2_firing = True
                fire_enemy_bullet(enemy_bullet2,enemy.xcor(),enemy.ycor())
        else:
            move_enemy_bullet(enemy_bullet2)

        if enemy_bullet.ycor() < -400:
            enemy_bullet.hideturtle()
            #enemy_bullet.setposition(0,500)
            enemy_firing = False

        if enemy_bullet2.ycor() < -400:
            enemy_bullet2.hideturtle()
            #enemy_bullet2.setposition(0,500)
            enemy2_firing = False


    #check if bullet is firing and move
    if bullet.ycor() < 320:
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    #check if bullet is at the top of the screen
    if bullet.ycor() > 320:
        bullet.hideturtle()
        bulletcount -= 1

#check for collision with enemy
    for enemy in enemies:
        if isCollision(bullet,enemy):
            os.system("aplay sounds/mysterykilled.wav&")
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0,400)
            bulletcount -= 1
            #explode
            enemy.hideturtle()
            explode(enemy.xcor(),enemy.ycor())
            #reset enemy
            x = random.randint(-300,300)
            y = random.randint(150,300)
            enemy.setposition(x,y)
            enemy.showturtle()

            #increase score
            score += 10
            scorestring = "SCORE: %s" %score
            score_pen.clear()
            score_pen.write(scorestring,False,align="left",font=("space_invaders.ttf", 18, "normal"))

        if isCollision(player,enemy):
            player.hideturtle()
            explode(player.xcor(),player.ycor())
            enemy.hideturtle()
            explode(enemy.xcor(),enemy.ycor())
            gameover = True
            break

        if isCollision(player,enemy_bullet):
            player.hideturtle()
            explode(player.xcor(),player.ycor())
            enemy_bullet.hideturtle()
            explode(enemy_bullet.xcor(),enemy_bullet.ycor())
            gameover = True
            break

    if gameover:
        os.system("aplay sounds/shipexplosion.wav&")
        ggstring = "GAME OVER"
        screen.clear()
        screen.bgcolor("red")
        ggpen = turtle.Turtle()
        ggpen.penup()
        ggpen.speed(0.5)
        ggpen.color("white")
        ggpen.hideturtle()
        ggpen.setposition(0,100)
        ggpen.write(ggstring,False,align="center",font=("space_invaders.ttf", 88, "bold"))
        time.sleep(1)
        ggpen.setposition(0,-200)
        ggpen.write(scorestring,False,align="center",font=("space_invaders.ttf", 70, "bold"))
        print(ggstring)
        break


delay = input("Press Enter To Exit...")
