import pygame
try:
    from sketch import P5
    from sketch import preload, setup, draw
    from sketch import mousePressed, mouseReleased
    from sketch import keyPressed, keyReleased
    from sketch import JoyMotion, JoyButtonReleased, JoyButtonPressed
except Exception:
    pass
from time import perf_counter
clock = pygame.time.Clock()


def get_pygame_const_name(index):
    for c in dir(pygame):
        if c[1] in "AZERTYUIOPMLKJHGFDSQWXCVBN":
            if type(getattr(pygame, c)) == int and getattr(pygame, c) == index:
                return c


def main(not_main):
    debut = perf_counter()
    if not_main:
        preload()
        setup()
        P5.keys = pygame.key.get_pressed()
    else:
        pygame.init()
        pygame.display.set_mode((1200, 600), 0)

    running = True
    while running:
        if not not_main:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.JOYDEVICEADDED:
                    pygame.joystick.init()
                    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

                elif event.type in (pygame.JOYHATMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP) and joysticks:
                    # for j in range(len(joysticks)):
                    #     print([joysticks[j].get_button(x) for x in range(joysticks[j].get_numbuttons())], end=" ")
                    #     print([joysticks[j].get_hat(x) for x in range(joysticks[j].get_numhats())])
                    pass
                    
                else:
                    print("event:", get_pygame_const_name(event.type))

            continue

        clock.tick(P5.FRAME_RATE)
        if P5.LOOP:
            draw()
            pygame.display.update()
            P5.frameCount += 1
        # else:
        #     print("Excution:", f"{perf_counter()-debut:.2f}")
        #     exit()

        for event in pygame.event.get():
            P5.keys = pygame.key.get_pressed()
            
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

            elif event.type == pygame.JOYDEVICEADDED:
                pygame.joystick.init()
                P5.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

            elif event.type == pygame.JOYHATMOTION:
                JoyMotion()

            elif event.type == pygame.JOYBUTTONDOWN:
                JoyButtonPressed()

            elif event.type == pygame.JOYBUTTONUP:
                JoyButtonReleased()

            elif event.type == pygame.QUIT:
                running = False
                
            # else:
            #     print("event:", get_pygame_const_name(event.type))

    pygame.quit()


main(__name__ != "__main__")
