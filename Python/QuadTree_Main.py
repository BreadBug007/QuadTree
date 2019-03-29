import pygame as py
import random
import QuadTree_Class as qt

py.init()

width, height = 1005, 705

screen = py.display.set_mode((width, height))

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)

q_tree = qt.QuadTree(qt.Rectangle(0, 0, width, height), 1)

for i in range(500):
    p = qt.Point(random.randint(0, width), random.randint(0, height))
    q_tree.insert(p)


while True:
    q_tree.show(screen)

    choice = 1
    found = []
    mouse_x, mouse_y = py.mouse.get_pos()

    if choice == 0:
        q_range = qt.Rectangle(mouse_x, mouse_y, 200, 200)
        py.draw.rect(screen, green, (q_range.x, q_range.y, q_range.w, q_range.h), 5)
        points = q_tree.query(q_range, found)
    else:
        q_range = qt.Circle(mouse_x, mouse_y, 100)
        py.draw.circle(screen, green, (q_range.x, q_range.y), q_range.radius, 5)
        points = q_tree.query(q_range, found)

    for p in points:
        py.draw.circle(screen, green, (p.x, p.y), 2)
    py.display.update()

    screen.fill(black)

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
        if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
            py.quit()
