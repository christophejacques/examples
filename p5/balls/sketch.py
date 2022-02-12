import pygame
from __init__ import background, createCanvas, stroke, fill, circle, rect
from __init__ import P5
from ball import Ball
from mover import Mover


mouseX, mouseY = 0, 0
balls = []
for i in range(4):
    balls.append(Ball(50+i*150, 100, 10*i+40))

movers = []
for i in range(4):
    movers.append(Mover(100 + i*150, 100, 20+i*20))


def setup():
    createCanvas(800, 500)
    stroke(20, 200, 50)
    fill(20, 100, 150)


def draw3():
    background(0)
    fill(30, 30, 150)
    rect(0, P5.HEIGHT//2, P5.WIDTH, P5.HEIGHT)
    stroke(150)
    fill(50)
    for mover in movers:
        mover.update()
        mover.edges()
        mover.draw()


def draw2():
    background(0)
    stroke(150)
    fill(50)
    circle(P5.WIDTH/2, P5.HEIGHT/2, 50) 
    for mover in movers:
        mover.update()
        mover.draw()


def draw():
    background(51)
    for ball in balls:
        ball.update()
        ball.display()
        ball.checkBoundaryCollision()
        for other in balls:
            if ball != other:
                ball.checkCollision(other)


if __name__ == "__main__":
    setup()
    running = True
    while running:
        pygame.time.Clock().tick(60)
        draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KMOD_LGUI:
                mouseX, mouseY = event.pos

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.QUIT:
                running = False

    pygame.quit()
