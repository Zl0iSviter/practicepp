import pygame
import math


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    radius = 15
    tool = 'pencil'
    color = (0, 0, 255)

    points = []
    shape_start = None

    canvas = pygame.Surface((640, 480))
    canvas.fill((0, 0, 0))

    palette_colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 165, 0),
        (255, 255, 255),
    ]
    palette_rects = [pygame.Rect(10 + i * 30, 450, 25, 25) for i in range(len(palette_colors))]

    while True:
        mouse_buttons = pygame.mouse.get_pressed()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_p:
                    tool = 'pencil'
                elif event.key == pygame.K_r:
                    tool = 'rect'
                elif event.key == pygame.K_c:
                    tool = 'circle'
                elif event.key == pygame.K_e:
                    tool = 'eraser'
                elif event.key == pygame.K_s:
                    tool = 'square'
                elif event.key == pygame.K_t:
                    tool = 'triangle'
                elif event.key == pygame.K_y:
                    tool = 'eq_triangle'
                elif event.key == pygame.K_h:
                    tool = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos

                    clicked_palette = False
                    for i, rect in enumerate(palette_rects):
                        if rect.collidepoint(mx, my):
                            color = palette_colors[i]
                            clicked_palette = True
                            break

                    if not clicked_palette:
                        if tool in ('pencil', 'eraser'):
                            points = [event.pos]
                        else:
                            shape_start = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and shape_start:

                    ex, ey = event.pos
                    sx, sy = shape_start

                    if tool == 'square':
                        size = min(abs(ex - sx), abs(ey - sy))
                        pygame.draw.rect(canvas, color, (sx, sy, size, size), radius)

                    elif tool == 'rect':
                        pygame.draw.rect(canvas, color,
                                         (min(sx, ex), min(sy, ey),
                                          abs(ex - sx), abs(ey - sy)), radius)

                    elif tool == 'circle':
                        cx = (sx + ex) // 2
                        cy = (sy + ey) // 2
                        rad = int(math.hypot(ex - sx, ey - sy) // 2)
                        pygame.draw.circle(canvas, color, (cx, cy), max(1, rad), radius)

                    elif tool == 'triangle':
                        pygame.draw.polygon(canvas, color, [(sx, sy), (sx, ey), (ex, ey)], radius)

                    elif tool == 'eq_triangle':
                        bx1 = min(ex, sx)
                        bx2 = max(ex, sx)
                        by = max(ey, sy)
                        cx = int((bx1 + bx2) / 2)
                        side = bx2 - bx1
                        height = int(side * math.sqrt(3) / 2)
                        ay = by - height
                        pygame.draw.polygon(canvas, color, [(cx, ay), (bx1, by), (bx2, by)], radius)

                    elif tool == 'rhombus':
                        cx = (sx + ex) // 2
                        cy = (sy + ey) // 2
                        dx = abs(ex - sx) // 2
                        dy = abs(ey - sy) // 2
                        pygame.draw.polygon(canvas, color,
                                            [(cx, cy - dy), (cx + dx, cy),
                                             (cx, cy + dy), (cx - dx, cy)], radius)

                    shape_start = None
                    points = []

            if event.type == pygame.MOUSEMOTION:
                if mouse_buttons[0]:
                    if tool == 'pencil' and points:
                        drawLineBetween(canvas, points[-1], event.pos, radius, color)
                        points.append(event.pos)
                        points = points[-256:]
                    elif tool == 'eraser':
                        pygame.draw.circle(canvas, (0, 0, 0), event.pos, radius)

        screen.blit(canvas, (0, 0))

        for i, rect in enumerate(palette_rects):
            pygame.draw.rect(screen, palette_colors[i], rect)

        if shape_start and mouse_buttons[0]:
            mx, my = pygame.mouse.get_pos()
            sx, sy = shape_start

            if tool == 'square':
                size = min(abs(mx - sx), abs(my - sy))
                pygame.draw.rect(screen, color, (sx, sy, size, size), radius)

            elif tool == 'rect':
                pygame.draw.rect(screen, color,
                                 (min(sx, mx), min(sy, my),
                                  abs(mx - sx), abs(my - sy)), radius)

            elif tool == 'circle':
                cx = (sx + mx) // 2
                cy = (sy + my) // 2
                rad = int(math.hypot(mx - sx, my - sy) // 2)
                pygame.draw.circle(screen, color, (cx, cy), max(1, rad), radius)

            elif tool == 'triangle':
                pygame.draw.polygon(screen, color, [(sx, sy), (sx, my), (mx, my)], radius)

            elif tool == 'eq_triangle':
                bx1 = min(mx, sx)
                bx2 = max(mx, sx)
                by = max(my, sy)
                cx = int((bx1 + bx2) / 2)
                side = bx2 - bx1
                height = int(side * math.sqrt(3) / 2)
                ay = by - height
                pygame.draw.polygon(screen, color, [(cx, ay), (bx1, by), (bx2, by)], radius)

            elif tool == 'rhombus':
                cx = (sx + mx) // 2
                cy = (sy + my) // 2
                dx = abs(mx - sx) // 2
                dy = abs(my - sy) // 2
                pygame.draw.polygon(screen, color,
                                    [(cx, cy - dy), (cx + dx, cy),
                                     (cx, cy + dy), (cx - dx, cy)], radius)

        pygame.display.flip()
        clock.tick(60)


def drawLineBetween(screen, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    if iterations == 0:
        return

    for i in range(iterations):
        progress = i / iterations
        x = int(start[0] + (end[0] - start[0]) * progress)
        y = int(start[1] + (end[1] - start[1]) * progress)
        pygame.draw.circle(screen, color, (x, y), width)


main()