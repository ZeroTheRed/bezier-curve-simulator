import numpy as np
import math
import pygame

pygame.init()
surface = pygame.display.set_mode((800, 600))
surface.fill((0,0,0))

def binomial(n, i):
    return ( math.factorial(n) / ( math.factorial(n-i) * math.factorial(i) ) )

def bernstein(t, n, i):
    return binomial(n, i) * (t ** i) * ( (1 - t) ** (n - i))

def bezier(points, t):
    n = len(points) - 1
    x = y = 0
    for i, pos in enumerate(points):
        x += pos[0] * bernstein(t, n, i)
        y += pos[1] * bernstein(t, n, i)
    return (x, y)

def plot_points(points):
    total = len(points)
    for i in range(total):
        pygame.draw.circle(surface, (0, 255, 0), points[i], 4)

def plot_lines(points):
    line_total = len(points) - 1
    for i in range(line_total):
        pygame.draw.line(surface, (100, 100, 100), points[i], points[i+1], 1)

def bezier_draw(points, n):
    positions = []
    samples = np.array(np.linspace(0, n, 1000))
    for j in np.linspace(0, n-1, 1000):
        t = j / (n - 1)
        (pos_x, pos_y) = bezier(points, t)
        positions.append((pos_x, pos_y))
    pygame.draw.lines(surface, (255, 174, 0), False, positions, 2)

def bounding_boxes(points):
    n = len(points)
    for i in range(n):
        x1, y1 = points[i][0] - 10, points[i][1] - 10
        x2, y2 = points[i][0] + 10, points[i][1] + 10
        boxes.append(pygame.Rect(x1, y1, x2-x1, y2-y1))
        pygame.draw.rect(surface, (255,0,255), boxes[i], 2)

def control_points_generator():
    n = int(input("How many Bezier control points? (Enter a number greater than 2):  "))
    ctrl_points = []

    for i in range(n):
        ctrl_x = np.random.randint(0, 800)
        ctrl_y = np.random.randint(0, 600)
        ctrl_points.append([ctrl_x, ctrl_y])

    return ctrl_points

def control_coordinates(points):
    n = len(points)
    text = []
    textRect = []
    font = pygame.font.Font('freesansbold.ttf', 16)
    for i in range(n):
        c_x = points[i][0]
        c_y = points[i][1] - 15
        coords = "(" + str(c_x) + "," + str(c_y) + ")"
        text_render = font.render(coords, True, (0, 255, 0))
        text.append(text_render)
        textRect_rect = text[i].get_rect()
        textRect.append(textRect_rect)
        textRect[i].center = (c_x, c_y)
        surface.blit(text[i], textRect[i])

ctrl_points = control_points_generator()
n = len(ctrl_points)
drag_points = False

while True:
    boxes = []
    plot_points(ctrl_points)
    bounding_boxes(ctrl_points)
    plot_lines(ctrl_points)
    bezier_draw(ctrl_points, n)
    control_coordinates(ctrl_points)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame,quit()
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
           if event.button == 1:
               mouse_pos = pygame.mouse.get_pos()
               for i in range(n):
                   if boxes[i].collidepoint(mouse_pos):
                       drag_points = True
                       mouse_x, mouse_y = mouse_pos
                       offset_x = boxes[i].x - mouse_x
                       offset_y = boxes[i].y - mouse_y
                       break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                   drag_points = False

        elif event.type == pygame.MOUSEMOTION:
            if drag_points:
                mouse_x, mouse_y = event.pos
                ctrl_points[i][0] = mouse_x + offset_x
                ctrl_points[i][1] = mouse_y + offset_y

    surface.fill((0,0,0))




