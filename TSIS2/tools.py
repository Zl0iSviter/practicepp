import pygame
import math
from collections import deque


# pencil tool - draws continuously while mouse is held
def draw_pencil(canvas, start, end, color, radius):
    pygame.draw.line(canvas, color, start, end, radius * 2)
    # also draw circles at endpoints so there are no gaps
    pygame.draw.circle(canvas, color, end, radius)


# straight line tool - draws a line from start to end
def draw_line(canvas, start, end, color, radius):
    pygame.draw.line(canvas, color, start, end, radius * 2)


# rectangle tool
def draw_rect(canvas, start, end, color, radius):
    sx, sy = start
    ex, ey = end
    pygame.draw.rect(canvas, color,
                     (min(sx, ex), min(sy, ey),
                      abs(ex - sx), abs(ey - sy)), radius)


# square tool - makes width = height
def draw_square(canvas, start, end, color, radius):
    sx, sy = start
    ex, ey = end
    size = min(abs(ex - sx), abs(ey - sy))
    pygame.draw.rect(canvas, color, (sx, sy, size, size), radius)


# circle tool - uses bounding box center
def draw_circle(canvas, start, end, color, radius):
    sx, sy = start
    ex, ey = end
    cx = (sx + ex) // 2
    cy = (sy + ey) // 2
    rad = int(math.hypot(ex - sx, ey - sy) // 2)
    pygame.draw.circle(canvas, color, (cx, cy), max(1, rad), radius)


# right triangle tool
def draw_triangle(canvas, start, end, color, radius):
    sx, sy = start
    ex, ey = end
    pygame.draw.polygon(canvas, color, [(sx, sy), (sx, ey), (ex, ey)], radius)


# equilateral triangle tool
def draw_eq_triangle(canvas, start, end, color, radius):
    sx, sy = start
    ex, ey = end
    bx1 = min(ex, sx)
    bx2 = max(ex, sx)
    by = max(ey, sy)
    cx = int((bx1 + bx2) / 2)
    side = bx2 - bx1
    height = int(side * math.sqrt(3) / 2)
    ay = by - height
    pygame.draw.polygon(canvas, color, [(cx, ay), (bx1, by), (bx2, by)], radius)


# rhombus tool
def draw_rhombus(canvas, start, end, color, radius):
    sx, sy = start
    ex, ey = end
    cx = (sx + ex) // 2
    cy = (sy + ey) // 2
    dx = abs(ex - sx) // 2
    dy = abs(ey - sy) // 2
    pygame.draw.polygon(canvas, color,
                        [(cx, cy - dy), (cx + dx, cy),
                         (cx, cy + dy), (cx - dx, cy)], radius)


# flood fill tool - fills connected area with same color
# uses bfs (breadth first search) to find all connected pixels
def flood_fill(canvas, pos, fill_color):
    x, y = pos
    w, h = canvas.get_size()

    # get the color we are replacing
    target_color = canvas.get_at((x, y))[:3]  # ignore alpha

    # dont fill if clicking on the same color
    if target_color == fill_color[:3]:
        return

    # use a queue for bfs traversal
    queue = deque()
    queue.append((x, y))
    visited = set()
    visited.add((x, y))

    # lock surface for faster pixel access
    canvas.lock()

    while queue:
        cx, cy = queue.popleft()

        # check bounds
        if cx < 0 or cx >= w or cy < 0 or cy >= h:
            continue

        # check if this pixel matches target color
        current = canvas.get_at((cx, cy))[:3]
        if current != target_color:
            continue

        # paint the pixel
        canvas.set_at((cx, cy), fill_color)

        # add neighbors to queue
        for nx, ny in [(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]:
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))

    canvas.unlock()


# eraser - just draws black circle over canvas
def draw_eraser(canvas, pos, radius):
    pygame.draw.circle(canvas, (0, 0, 0), pos, radius * 2)


# helper to draw shape preview on screen (before mouse release)
def draw_preview(screen, tool, start, end, color, radius):
    sx, sy = start
    ex, ey = end

    if tool == 'line':
        pygame.draw.line(screen, color, start, end, radius * 2)

    elif tool == 'rect':
        pygame.draw.rect(screen, color,
                         (min(sx, ex), min(sy, ey),
                          abs(ex - sx), abs(ey - sy)), radius)

    elif tool == 'square':
        size = min(abs(ex - sx), abs(ey - sy))
        pygame.draw.rect(screen, color, (sx, sy, size, size), radius)

    elif tool == 'circle':
        cx = (sx + ex) // 2
        cy = (sy + ey) // 2
        rad = int(math.hypot(ex - sx, ey - sy) // 2)
        pygame.draw.circle(screen, color, (cx, cy), max(1, rad), radius)

    elif tool == 'triangle':
        pygame.draw.polygon(screen, color, [(sx, sy), (sx, ey), (ex, ey)], radius)

    elif tool == 'eq_triangle':
        bx1 = min(ex, sx)
        bx2 = max(ex, sx)
        by = max(ey, sy)
        cx = int((bx1 + bx2) / 2)
        side = bx2 - bx1
        height = int(side * math.sqrt(3) / 2)
        ay = by - height
        pygame.draw.polygon(screen, color, [(cx, ay), (bx1, by), (bx2, by)], radius)

    elif tool == 'rhombus':
        cx = (sx + ex) // 2
        cy = (sy + ey) // 2
        dx = abs(ex - sx) // 2
        dy = abs(ey - sy) // 2
        pygame.draw.polygon(screen, color,
                            [(cx, cy - dy), (cx + dx, cy),
                             (cx, cy + dy), (cx - dx, cy)], radius)
