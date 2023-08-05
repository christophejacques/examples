#! c:\bat\python.bat -3.11
import settings
from __init__ import createCanvas
from __init__ import *
from game import Game

 
g = Game()


def keyPressed():
    if P5.keyCode == pygame.K_SPACE:
        g.activate()


def setup():
    createCanvas(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
    textSize(20)


def draw():
    g.update()
    g.draw()
