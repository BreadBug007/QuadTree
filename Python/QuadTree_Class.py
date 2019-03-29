import pygame as py


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def contains(self, point):
        return self.x + self.w >= point.x >= self.x and self.y + self.h >= point.y >= self.y

    def intersects_rectangle(self, q_range):
        if (q_range.x > self.x + self.w
           or q_range.x + q_range.w < self.x
           or q_range.y > self.y + self.h
           or q_range.y + q_range.h < self.y):
            return False
        return True

    def intersects_circle(self, q_range):
        delta_x = q_range.x - max(self.x, min(q_range.x, self.x + self.w))
        delta_y = q_range.y - max(self.y, min(q_range.y, self.y + self.h))
        return delta_x ** 2 + delta_y ** 2 < q_range.radius ** 2


class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.radius = r

    def contains(self, p):
        return (p.x - self.x) ** 2 + (p.y - self.y) ** 2 < self.radius ** 2


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
        try:
            if not self.boundary.intersects_circle(q_range):
                return
        except AttributeError:
            if not self.boundary.intersects_rectangle(q_range):
                return
        if self.divided:
            self.northwest.query(q_range, found)
            self.northeast.query(q_range, found)
            self.southwest.query(q_range, found)
            self.southeast.query(q_range, found)
        else:
            for p in self.points:
                if q_range.contains(p):
                    found.append(p)
        return found

    def show(self, screen):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        py.draw.rect(screen, (255, 255, 255), (x, y, w, h), 1)

        if self.divided:
            self.northwest.show(screen)
            self.northeast.show(screen)
            self.southwest.show(screen)
            self.southeast.show(screen)

        for p in self.points:
            py.draw.circle(screen, (255, 255, 255), (p.x, p.y), 2)
