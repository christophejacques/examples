import pygame
from sketch import P5
from sketch import preload, setup, draw
from sketch import mousePressed, mouseReleased
from sketch import keyPressed, keyReleased
from time import perf_counter
clock = pygame.time.Clock()


def main():
    debut = perf_counter()
    preload()
    setup()
    running = True
    while running:
        clock.tick(P5.FRAME_RATE)
        if P5.LOOP:
            draw()
            pygame.display.update()
            P5.frameCount += 1
        # else:
        #     print("Excution:", f"{perf_counter()-debut:.2f}")
        #     exit()

        for event in pygame.event.get():
            if event.type == pygame.KMOD_LGUI:
                P5.pmouseX, P5.pmouseY = P5.mouseX, P5.mouseY
                P5.mouseX, P5.mouseY = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                P5.mouseIsPressed = True
                mousePressed() 

            elif event.type == pygame.MOUSEBUTTONUP:
                P5.mouseIsPressed = False
                mouseReleased()

            elif event.type == pygame.KEYDOWN:
                P5.keyIsPressed = True
                P5.keyCode = event.key
                keyPressed()

            elif event.type == pygame.KEYUP:
                P5.keyIsPressed = False
                keyReleased()
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.QUIT:
                running = False

    pygame.quit()


main()
