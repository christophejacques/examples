# Star screen saver
import numpy as np
import pygame as pg
import random as rd
import os
from time import perf_counter

# from pygame import gfxdraw

os.environ['SDL_VIDEO_WINDOW_POS'] = "5,30"
pg.init()

# Variables globales
nb_etoiles: int = 1000
ecartement: int = 8
acceleration: int = -4
distanceMaxZ: int = 20

ecran = np.array([1910, 1002])

centre = ecran / 2
distanceMax: float = (distanceMaxZ+10) * centre[0] * centre[1]

# Coordonnees :
# -centre[0] < X < centre[0]
# -centre[1] < Y < centre[1]
#         10 < Z < 10 + distanceMaxZ
# DistanceXY : 0
coords: list = [np.array([rd.random() * ecran[0] - centre[0], 
    rd.random() * ecran[1] - centre[1], 
    rd.random() * distanceMaxZ + 10, 0]) for _ in range(nb_etoiles)]

for coord in coords:
    coord[3] = 1 - abs(coord[0]) * abs(coord[1]) / (centre[0] * centre[1]) 

screen = pg.display.set_mode(tuple(ecran))

clock = pg.time.Clock()
running: bool = True


def get_radius(distance) -> int:
    return (distance[3] * (30-distance[2])) // 8
    return (30 - distance[2]) // 8


def get_color(distance) -> tuple[int, int, int]:
    colorG = int(distance[3] * (255-(distance[2]*8.5)))
    return (0, colorG, colorG) 


dt: float = 0.0
tick: float

while running:
    tick = perf_counter()
        
    screen.fill((0, 0, 0))
    for coord in coords:
        affich = coord.copy()
        affich[:2] /= coord[2] / ecartement
        affich[:2] += centre

        r = int(get_radius(affich))
        pg.draw.rect(screen, get_color(coord), (*affich[:2], r, r))

        coord[2] += acceleration * dt
        if (coord[2] <= 0) or \
           (affich[0] > ecran[0]) or (affich[1] > ecran[1]) or \
        (affich[0] < 0) or (affich[1] < 0):
            coord[0] = rd.random() * ecran[0] - centre[0]
            coord[1] = rd.random() * ecran[1] - centre[1] 
            coord[2] = rd.random() * distanceMaxZ + 10
            coord[3] = 1 - abs(coord[0]) * abs(coord[1]) / (centre[0] * centre[1]) 

    pg.display.update()
    clock.tick(60)
    dt = perf_counter() - tick
    pg.display.set_caption(f"FPS: {clock.get_fps():.1f}  - Vitesse: {-acceleration} pix/frame")

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYUP:
            match event.key:
                case pg.K_ESCAPE:
                    running = False
                case pg.K_KP_PLUS:
                    acceleration -= 1
                case pg.K_KP_MINUS:
                    if acceleration < -1:
                        acceleration += 1


pg.quit()
