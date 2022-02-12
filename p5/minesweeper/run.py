import pygame
from sketch import P5
from sketch import setup, draw
from sketch import mousePressed, mouseReleased
from sketch import keyPressed, keyReleased


def main():
    setup()
    running = True
    while running:
        pygame.time.Clock().tick(60)
        if P5.LOOP:
            draw()
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KMOD_LGUI:
                P5.mouseX, P5.mouseY = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                P5.mouseIsPressed = event.button
                mousePressed() 

            elif event.type == pygame.MOUSEBUTTONUP:
                mouseReleased()
                P5.mouseIsPressed = 0

            elif event.type == pygame.KEYDOWN:
                P5.keyIsPressed = True
                P5.keyCode = event.key
                keyPressed()

            elif event.type == pygame.KEYUP:
                keyReleased()
                P5.keyIsPressed = False
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.QUIT:
                running = False

    pygame.quit()


main()
