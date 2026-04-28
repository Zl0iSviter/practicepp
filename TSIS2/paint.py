import pygame
import math
import datetime
from tools import (
    draw_pencil, draw_line, draw_rect, draw_square, draw_circle,
    draw_triangle, draw_eq_triangle, draw_rhombus,
    flood_fill, draw_eraser, draw_preview
)

# --- constants ---
SCREEN_W = 1000
SCREEN_H = 800
TOOLBAR_H = 50  # toolbar at the bottom
CANVAS_H = SCREEN_H - TOOLBAR_H

# toolbar button width
BTN_W = 55
BTN_H = 36


def make_toolbar_buttons():
    # returns list of (rect, label, tool_name or action_name)
    # tools on the left, brush sizes in the middle, save on the right
    tools = [
        ('pencil', 'P pencil'),
        ('line', 'L line'),
        ('rect', 'R rect'),
        ('square', 'S sq'),
        ('circle', 'C circ'),
        ('triangle', 'T tri'),
        ('eq_triangle', 'Y eq-t'),
        ('rhombus', 'H rhmb'),
        ('fill', 'F fill'),
        ('eraser', 'E erase'),
        ('text', 'X text'),
    ]

    buttons = []
    x = 5
    for tool_id, label in tools:
        rect = pygame.Rect(x, CANVAS_H + 7, BTN_W, BTN_H)
        buttons.append((rect, label, tool_id))
        x += BTN_W + 3

    return buttons


def make_size_buttons():
    # three brush size buttons
    sizes = [(2, '1 sm'), (5, '2 md'), (10, '3 lg')]
    buttons = []
    x = SCREEN_W - 3 * (BTN_W + 3) - 100  # right side area
    for size_val, label in sizes:
        rect = pygame.Rect(x, CANVAS_H + 7, BTN_W, BTN_H)
        buttons.append((rect, label, size_val))
        x += BTN_W + 3
    return buttons


def make_palette():
    colors = [
        (0, 0, 0),
        (255, 255, 255),
        (255, 0, 0),
        (0, 200, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 165, 0),
        (180, 0, 255),
        (0, 200, 200),
        (255, 100, 150),
    ]
    rects = []
    x = SCREEN_W - len(colors) * 28 - 5
    for i, c in enumerate(colors):
        rect = pygame.Rect(x + i * 28, CANVAS_H + 13, 24, 24)
        rects.append((rect, c))
    return rects


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("paint - practice 12")
    clock = pygame.time.Clock()

    # font for toolbar labels and text tool
    font_small = pygame.font.SysFont('consolas', 11)
    font_text = pygame.font.SysFont('consolas', 20)  # used when placing text on canvas

    # --- state ---
    radius = 5  # brush radius (half the stroke width)
    tool = 'pencil'
    color = (0, 0, 0)

    points = []  # stores mouse positions for pencil
    shape_start = None  # start point for shape/line tools

    # text tool state
    text_active = False  # are we in text input mode?
    text_pos = (0, 0)  # where user clicked
    text_buffer = ''  # characters typed so far

    # canvas - this is what gets saved
    canvas = pygame.Surface((SCREEN_W, CANVAS_H))
    canvas.fill((255, 255, 255))  # white background

    toolbar_buttons = make_toolbar_buttons()
    size_buttons = make_size_buttons()
    palette = make_palette()

    running = True
    while running:
        mouse_buttons = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()

        # --- event handling ---
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # keyboard shortcuts
            if event.type == pygame.KEYDOWN:

                # text tool active - capture typed characters
                if text_active:
                    if event.key == pygame.K_RETURN:
                        # commit text to canvas permanently
                        if text_buffer:
                            text_surf = font_text.render(text_buffer, True, color)
                            canvas.blit(text_surf, text_pos)
                        text_active = False
                        text_buffer = ''

                    elif event.key == pygame.K_ESCAPE:
                        # cancel text input
                        text_active = False
                        text_buffer = ''

                    elif event.key == pygame.K_BACKSPACE:
                        text_buffer = text_buffer[:-1]

                    else:
                        # add typed character to buffer
                        if event.unicode and event.unicode.isprintable():
                            text_buffer += event.unicode

                    continue  # skip other shortcuts while typing

                # ctrl+s = save canvas
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f'canvas_{timestamp}.png'
                    pygame.image.save(canvas, filename)
                    pygame.display.set_caption(f'paint - saved {filename}')
                    continue

                # escape exits app (only when not in text mode)
                if event.key == pygame.K_ESCAPE:
                    running = False

                # tool shortcuts
                if event.key == pygame.K_p:
                    tool = 'pencil'
                elif event.key == pygame.K_l:
                    tool = 'line'
                elif event.key == pygame.K_r:
                    tool = 'rect'
                elif event.key == pygame.K_s:
                    tool = 'square'
                elif event.key == pygame.K_c:
                    tool = 'circle'
                elif event.key == pygame.K_t:
                    tool = 'triangle'
                elif event.key == pygame.K_y:
                    tool = 'eq_triangle'
                elif event.key == pygame.K_h:
                    tool = 'rhombus'
                elif event.key == pygame.K_f:
                    tool = 'fill'
                elif event.key == pygame.K_e:
                    tool = 'eraser'
                elif event.key == pygame.K_x:
                    tool = 'text'

                # brush size shortcuts
                elif event.key == pygame.K_1:
                    radius = 2
                elif event.key == pygame.K_2:
                    radius = 5
                elif event.key == pygame.K_3:
                    radius = 10

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_x, click_y = event.pos

                    # check if click is in toolbar area
                    if click_y >= CANVAS_H:
                        # check tool buttons
                        for rect, label, tool_id in toolbar_buttons:
                            if rect.collidepoint(click_x, click_y):
                                tool = tool_id
                                text_active = False
                                text_buffer = ''
                                break

                        # check size buttons
                        for rect, label, size_val in size_buttons:
                            if rect.collidepoint(click_x, click_y):
                                radius = size_val
                                break

                        # check palette
                        for rect, c in palette:
                            if rect.collidepoint(click_x, click_y):
                                color = c
                                break

                        continue  # dont draw if clicked toolbar

                    # --- canvas clicks ---

                    # text tool - start typing at clicked position
                    if tool == 'text':
                        text_active = True
                        text_pos = (click_x, click_y)
                        text_buffer = ''
                        continue

                    # fill tool - run flood fill immediately on click
                    if tool == 'fill':
                        flood_fill(canvas, (click_x, click_y), color)
                        continue

                    # pencil/eraser - start collecting points
                    if tool in ('pencil', 'eraser'):
                        points = [event.pos]

                    else:
                        # shape tools - record starting position
                        shape_start = event.pos

            # mouse button release - finalize shape
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and shape_start and my < CANVAS_H:
                    ex, ey = event.pos
                    sx, sy = shape_start

                    if tool == 'line':
                        draw_line(canvas, shape_start, event.pos, color, radius)
                    elif tool == 'rect':
                        draw_rect(canvas, shape_start, event.pos, color, radius)
                    elif tool == 'square':
                        draw_square(canvas, shape_start, event.pos, color, radius)
                    elif tool == 'circle':
                        draw_circle(canvas, shape_start, event.pos, color, radius)
                    elif tool == 'triangle':
                        draw_triangle(canvas, shape_start, event.pos, color, radius)
                    elif tool == 'eq_triangle':
                        draw_eq_triangle(canvas, shape_start, event.pos, color, radius)
                    elif tool == 'rhombus':
                        draw_rhombus(canvas, shape_start, event.pos, color, radius)

                    shape_start = None
                    points = []

                elif event.button == 1:
                    # released outside canvas or no shape - reset
                    shape_start = None

            # mouse motion - pencil draws continuously
            if event.type == pygame.MOUSEMOTION:
                if mouse_buttons[0] and my < CANVAS_H:
                    if tool == 'pencil' and points:
                        draw_pencil(canvas, points[-1], event.pos, color, radius)
                        points.append(event.pos)
                        points = points[-256:]  # keep buffer small

                    elif tool == 'eraser':
                        draw_eraser(canvas, event.pos, radius)

        # --- drawing ---
        # draw canvas to screen
        screen.blit(canvas, (0, 0))

        # draw text preview if text tool is active
        if text_active and text_buffer:
            preview_surf = font_text.render(text_buffer, True, color)
            screen.blit(preview_surf, text_pos)

        # show blinking cursor for text tool
        if text_active:
            # simple cursor indicator
            cursor_x = text_pos[0] + font_text.size(text_buffer)[0]
            cursor_y = text_pos[1]
            ticks = pygame.time.get_ticks()
            if (ticks // 500) % 2 == 0:  # blink every 500ms
                pygame.draw.line(screen, color,
                                 (cursor_x, cursor_y),
                                 (cursor_x, cursor_y + 20), 2)

        # draw shape preview while dragging
        if shape_start and mouse_buttons[0] and my < CANVAS_H:
            curr_pos = (mx, my)
            if tool in ('line', 'rect', 'square', 'circle',
                        'triangle', 'eq_triangle', 'rhombus'):
                draw_preview(screen, tool, shape_start, curr_pos, color, radius)

        # draw toolbar background
        pygame.draw.rect(screen, (45, 45, 45), (0, CANVAS_H, SCREEN_W, TOOLBAR_H))
        pygame.draw.line(screen, (100, 100, 100), (0, CANVAS_H), (SCREEN_W, CANVAS_H), 1)

        # draw tool buttons
        for rect, label, tool_id in toolbar_buttons:
            active = (tool == tool_id)
            btn_color = (80, 130, 200) if active else (65, 65, 65)
            border_color = (150, 190, 255) if active else (100, 100, 100)
            pygame.draw.rect(screen, btn_color, rect, border_radius=4)
            pygame.draw.rect(screen, border_color, rect, 1, border_radius=4)
            txt = font_small.render(label, True, (255, 255, 255))
            screen.blit(txt, (rect.x + 3, rect.y + (BTN_H - txt.get_height()) // 2))


        # draw color palette swatches
        for rect, c in palette:
            pygame.draw.rect(screen, c, rect, border_radius=3)
            # highlight current color
            if c == color:
                pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=3)
            else:
                pygame.draw.rect(screen, (90, 90, 90), rect, 1, border_radius=3)

        # draw current color indicator square on the right
        cur_rect = pygame.Rect(SCREEN_W - 42, CANVAS_H + 8, 34, 34)
        pygame.draw.rect(screen, color, cur_rect, border_radius=4)
        pygame.draw.rect(screen, (180, 180, 180), cur_rect, 2, border_radius=4)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()