"""A very basic flipper game.
"""
__docformat__ = "reStructuredText"

import pygame

import pymunk
import pymunk.pygame_util

pygame.init()


def main():
    fps = 60
    dt = 1 / fps
    w, h = 600, 600
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    # draw_options = pymunk.pygame_util.DrawOptions(screen)

    space = pymunk.Space()
    space.gravity = 0, 982
    space.use_spatial_hash(4, 100000)

    static_lines = [
        pymunk.Segment(space.static_body, (050.0, 000.0), (050.0, 100.0), 5.0),  # | gauche
        pymunk.Segment(space.static_body, (050.0, 100.0), (500.0, 100.0), 5.0),  # --------
        pymunk.Segment(space.static_body, (100.0, 200.0), (580.0, 200.0), 5.0),  # --------
        pymunk.Segment(space.static_body, (020.0, 000.0), (020.0, 550.0), 5.0),  # | gauche
        pymunk.Segment(space.static_body, (020.0, 300.0), (500.0, 300.0), 5.0),  # --------
        pymunk.Segment(space.static_body, (100.0, 400.0), (580.0, 400.0), 5.0),  # --------
        pymunk.Segment(space.static_body, (020.0, 550.0), (500.0, 550.0), 5.0),  # --------
        pymunk.Segment(space.static_body, (580.0, 000.0), (580.0, 600.0), 5.0),  # | droit
    ]

    space.add(*static_lines)

    particles = []
    for x in range(60):
        for y in range(80):
            b = pymunk.Body()
            s = pymunk.Circle(b, 2)
            s.mass = 1
            b.position = (
                200 + x * 3,
                80 - y * 2,
            )
            space.add(b, s)
            particles.append(b)

    x = space.shapes[100].body.position
    
    # fluid_scale = 1 / 3.0
    fluid_scale = 1 / 1.0
    fw, fh = int(w * fluid_scale), int(h * fluid_scale)
    fluid_surface = pygame.Surface((fw, fh))
    while True:
        # print(space.shapes[100].body.position, flush=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.KEYUP and event.key == pygame.K_p:
                pygame.image.save(screen, "fluid.png")

        color = 4885759  # 74, 140, 255
        # half_color = 4885758  # 74, 140, 254
        half_color = 4880000  # 74, 140, 254
        no_color = 0  # (0, 0, 0)
        white = pygame.Color('white')
        fluid_surface.fill((0, 0, 0))

        with pygame.PixelArray(fluid_surface) as pa:

            pa[102:578, 198] = white  # ----
            pa[102:578, 398] = white  # ----

            pa[52:500, 98] = white  # ----
            pa[22:500, 298] = white  # ----

            pa[22:498, 548] = white  # ----

            pa[52, 0:98] = white  
            pa[22, 0:548] = white  
            pa[578, 0:600] = white 

            for p in particles:

                x = int(p.position.x * fluid_scale)
                y = int(p.position.y * fluid_scale)

                if x < 2 or x > fw - 3 or y < 2:
                    continue

                if y > fh - 3:
                    # print("Avant:", p.position, end="  ")
                    v = pymunk.vec2d.Vec2d(-400, -p.position.y)
                    p.position += v
                    # print("Apres:", p.position, flush=True)
                    continue

                try:
                    pa[x, y] = color

                    if pa[x, y + 1] == half_color:
                        pa[x, y + 1] = color
                    elif pa[x, y + 1] == no_color:
                        pa[x, y + 1] = half_color

                    if pa[x + 1, y] == half_color:
                        pa[x + 1, y] = color
                    elif pa[x + 1, y] == no_color:
                        pa[x + 1, y] = half_color

                    if pa[x - 1, y] == half_color:
                        pa[x - 1, y] = color
                    elif pa[x - 1, y] == no_color:
                        pa[x - 1, y] = half_color

                    if pa[x, y - 1] == half_color:
                        pa[x, y - 1] = color
                    elif pa[x, y - 1] == no_color:
                        pa[x, y - 1] = half_color

                except Exception as e:
                    print(x, y)
                    raise e

        # s = pygame.transform.scale(fluid_surface, (w, h))
        # fluid_surface.
        # screen.blit(s, (0, 0))
        screen.blit(fluid_surface, (0, 0))

        steps = 1
        for x in range(steps):
            space.step(dt / steps)

        pygame.display.flip()
        clock.tick(fps)
        pygame.display.set_caption(f"fps: {clock.get_fps():.1f}")


if __name__ == "__main__":
    main()
