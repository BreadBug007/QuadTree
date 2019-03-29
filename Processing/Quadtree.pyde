class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, p):
        return self.x + self.w >= p.x >= self.x and self.y + self.h >= p.y >= self.y

    def intersects_rectangle(self, qrange):
        if (qrange.x > self.x + self.w 
            or qrange.x + qrange.w < self.x
            or qrange.y > self.y + self.h 
            or qrange.y + qrange.h < self.y):
            return False
        return True
    
    def intersects_circle(self, qrange):
        deltaX = qrange.x - max(self.x, min(qrange.x, self.x + self.w))
        deltaY = qrange.y - max(self.y, min(qrange.y, self.y + self.h))
        return (deltaX)**2 + (deltaY)**2 < qrange.radius**2
            
            
class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.radius = r
    
    def contains(self, p):
        return (p.x - self.x)**2 + (p.y - self.y)**2 < self.radius**2
 
               
class QuadTree:

    def __init__(self, boundary, n):
        self.boundary = boundary
        self.points = []
        self.limit = n
        self.divided = False
        self.northwest, self.northeast, self.southwest, self.southeast = (None, None, None, None)

    def insert(self, p):
        if not self.boundary.contains(p):
            return False
        if len(self.points) < self.limit:
            self.points.append(p)
            return True
        else:
            if not self.divided:
                self.subdivide()
                self.assign_points()
            if self.northwest.insert(p):
                return True
            elif self.northeast.insert(p):
                return True
            elif self.southwest.insert(p):
                return True
            elif self.southeast.insert(p):
                return True

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        self.northwest = QuadTree(Rectangle(x, y, w / 2, h / 2), self.limit)
        self.northeast = QuadTree(Rectangle(x + w / 2, y, w / 2, h / 2), self.limit)
        self.southwest = QuadTree(Rectangle(x, y + h / 2, w / 2, h / 2), self.limit)
        self.southeast = QuadTree(Rectangle(x + w / 2, y + h / 2, w / 2, h / 2), self.limit)
        self.divided = True


    def query(self, qrange, found):
        try:
            if not self.boundary.intersects_circle(qrange):
                return
        except AttributeError:
            if not self.boundary.intersects_rectangle(qrange):
                return
            
        if self.divided:
            self.northwest.query(qrange, found)
            self.northeast.query(qrange, found)
            self.southwest.query(qrange, found)
            self.southeast.query(qrange, found)
        
        else:
            for p in self.points:
                if qrange.contains(p):
                    found.append(p)

                
        return found
    
    
    def assign_points(self):    
        for p in self.points:    
            if self.northwest.boundary.contains(p):    
                self.northwest.points.append(p)    
            elif self.northeast.boundary.contains(p):    
                self.northeast.points.append(p)    
            elif self.southeast.boundary.contains(p):    
                self.southeast.points.append(p)    
            elif self.southwest.boundary.contains(p):    
                self.southwest.points.append(p)
            
    def show(self):
        stroke(255)
        noFill()
        strokeWeight(1)
        rect(self.boundary.x, self.boundary.y, self.boundary.w*2, self.boundary.h*2)
        if self.divided:
            self.northwest.show()
            self.northeast.show()
            self.southwest.show()
            self.southeast.show()
        
        # for p in self.points:
        #     strokeWeight(5)
        #     point(p.x, p.y)
            
        
def setup():
    global qtree
    size(802, 802)
    
    qtree = QuadTree(Rectangle(0, 0, width, height), 1)
    
    for i in range(500):
        p = Point(random(width), random(height))
        qtree.insert(p)
        

def draw():  
    
    background(0)
    
    qtree.show()

    stroke(0, 255, 0)
    strokeWeight(3)
    choice = 1
    
    found = []
    
    if choice == 0:
        qrange = Rectangle(mouseX, mouseY, 200, 200)
        rect(qrange.x, qrange.y, qrange.w, qrange.h)
        points = qtree.query(qrange, found)
    else:
        qrange = Circle(mouseX, mouseY, 100)
        circle(qrange.x, qrange.y, qrange.radius*2)
        points = qtree.query(qrange, found)

    
    for p in points:
        stroke(0, 255, 0)
        strokeWeight(5)
        point(p.x, p.y)
    

    

    
