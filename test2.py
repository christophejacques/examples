import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 500), flags=pygame.RESIZABLE, display=0)
pygame.display.set_caption("Titre")

running = True

r1 = pygame.Rect(100, 100, 200, 50)
r2 = pygame.Rect(200, 100, 200, 50)

print(dir(r1))
print(r1)
if r1.colliderect(r2):
    print("collision")
else:
    print()
white = (255, 255, 255)

while running:
    pygame.draw.rect(screen, (200, 200, 50), r1, width=2)
    pygame.draw.rect(screen, (200, 200, 50), (400, 100, 200, 50), width=5)
    pygame.draw.line(screen, white, (0, 0), (100, 100))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            running = False
        else:
            pass
            # print(event)

pygame.quit()
