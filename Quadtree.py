import pygame as py
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def contains(self, point):
        return self.x + self.w >= point.x >= self.x and self.y + self.h >= point.y >= self.y

    def intersects(self, q_range):
        if (q_range.x > self.x + self.w or
        q_range.x + q_range.w < self.x or
        q_range.y > self.y + self.h or
        q_range.y + q_range.h < self.y):
            return False
        return True


class QuadTree:

    def __init__(self, boundary, n):
        self.boundary = boundary
        self.points = []
        self.limit = n
        self.divided = False
        self.northwest, self.northeast, self.southwest, self.southeast = (None, None, None, None)

    def insert(self, point):
        if not self.boundary.contains(point):
            return False
        if len(self.points) < self.limit:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
                self.assign_points()
            if self.northwest.insert(point):
                return True
            if self.northeast.insert(point):
                return True
            if self.southwest.insert(point):
                return True
            if self.southeast.insert(point):
                return True

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        self.northwest = QuadTree(Rectangle(x, y, w // 2, h // 2), self.limit)
        self.northeast = QuadTree(Rectangle(x + w // 2, y, w // 2, h // 2), self.limit)
        self.southwest = QuadTree(Rectangle(x, y + h // 2, w // 2, h // 2), self.limit)
        self.southeast = QuadTree(Rectangle(x + w // 2, y + h // 2, w // 2, h // 2), self.limit)
        self.divided = True

    def assign_points(self):
        for p in self.points:
            if self.northwest.boundary.contains(p):
                self.northwest.points.append(p)
            if self.northeast.boundary.contains(p):
                self.northeast.points.append(p)
            if self.southeast.boundary.contains(p):
                self.southeast.points.append(p)
            if self.southwest.boundary.contains(p):
                self.southwest.points.append(p)

    def query(self, q_range, found):
        if found is None:
            found = []
        if not self.boundary.intersects(q_range):
            return
        else:
            for p in self.points:
                if q_range.contains(p):
                    found.append(p)
            if self.divided:
                self.northwest.query(q_range, found)
                self.northeast.query(q_range, found)
                self.southwest.query(q_range, found)
                self.southeast.query(q_range, found)

        return found

    def show(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        py.draw.rect(screen, white, (x, y, w, h), 1)

        if self.divided:
            self.northwest.show()
            self.northeast.show()
            self.southwest.show()
            self.southeast.show()

        for p in self.points:
            py.draw.circle(screen, white, (p.x, p.y), 3)


py.init()

width, height = 700, 700

screen = py.display.set_mode((width, height))

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)

screen.fill(black)

q_tree = QuadTree(Rectangle(0, 0, width, height), 1)

for i in range(500):
    p = Point(random.randint(0, width), random.randint(0, height))
    q_tree.insert(p)

q_tree.show()
found = []
while True:

    q_range = Rectangle(250, 250, 200, 200)
    py.draw.rect(screen, green, (q_range.x, q_range.y, q_range.w, q_range.h), 2)
    points = q_tree.query(q_range, found)
    py.display.update()

    for p in points:
        py.draw.circle(screen, green, (p.x, p.y), 4)

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
