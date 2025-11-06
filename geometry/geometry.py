import math

__all__ = [
    "Point", "Vector", "Line",
    "distance", "midpoint", "line_from_points", "line_slope_intercept",
    "reflect_point_across_axes", "reflect_point_across_line",
    "vector_add", "vector_sub", "vector_dot", "vector_cross", "vector_scale",
    "vector_mag", "vector_unit", "vector_proj"
]

class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def as_tuple(self):
        return (self.x, self.y)

    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def midpoint(self, other):
        return Point((self.x + other.x) / 2.0, (self.y + other.y) / 2.0)

    def translate(self, dx=0.0, dy=0.0):
        return Point(self.x + dx, self.y + dy)

    def to_vector(self):
        return Vector(self.x, self.y)

    def reflect_x(self):
        return Point(self.x, -self.y)

    def reflect_y(self):
        return Point(-self.x, self.y)

    def reflect_origin(self):
        return Point(-self.x, -self.y)

    def reflect_across_line(self, line):
        x, y = self.x, self.y
        a, b, c = line.a, line.b, line.c
        d = a*a + b*b
        if d == 0:
            raise ValueError("Invalid line")
        k = (a*x + b*y + c) / d
        xr = x - 2*a*k
        yr = y - 2*b*k
        return Point(xr, yr)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def as_tuple(self):
        return (self.x, self.y)

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def sub(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def scale(self, k):
        return Vector(self.x * k, self.y * k)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def mag(self):
        return math.hypot(self.x, self.y)

    def unit(self):
        m = self.mag()
        if m == 0:
            raise ValueError("Zero vector has no unit vector")
        return Vector(self.x / m, self.y / m)

    def proj_onto(self, other):
        denom = other.x*other.x + other.y*other.y
        if denom == 0:
            raise ValueError("Cannot project onto zero vector")
        k = self.dot(other) / denom
        return Vector(other.x * k, other.y * k)

    def to_point(self):
        return Point(self.x, self.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


class Line:
    def __init__(self, a, b, c):
        if a == 0 and b == 0:
            raise ValueError("Invalid line coefficients")
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)

    @classmethod
    def from_points(cls, p1, p2):
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        if x1 == x2 and y1 == y2:
            raise ValueError("Need two distinct points")
        a = y1 - y2
        b = x2 - x1
        c = x1*y2 - x2*y1
        return cls(a, b, c)

    @classmethod
    def from_slope_intercept(cls, m, c):
        if m is None:
            raise ValueError("Use Line.vertical for vertical lines")
        return cls(-m, 1.0, -c)

    @classmethod
    def vertical(cls, x_const):
        return cls(1.0, 0.0, -float(x_const))

    def slope(self):
        if self.b == 0:
            return None
        return -self.a / self.b

    def y_intercept(self):
        if self.b == 0:
            return None
        return -self.c / self.b

    def contains(self, p):
        return math.isclose(self.a*p.x + self.b*p.y + self.c, 0.0, abs_tol=1e-9)

    def distance_to_point(self, p):
        return abs(self.a*p.x + self.b*p.y + self.c) / math.hypot(self.a, self.b)

    def intersection(self, other):
        D = self.a*other.b - other.a*self.b
        if math.isclose(D, 0.0, abs_tol=1e-12):
            return None
        Dx = (-self.c)*other.b - (-other.c)*self.b
        Dy = self.a*(-other.c) - other.a*(-self.c)
        x = Dx / D
        y = Dy / D
        return Point(x, y)

    def reflect_point(self, p):
        return p.reflect_across_line(self)

    def as_abc(self):
        return (self.a, self.b, self.c)

    def as_slope_intercept(self):
        return (self.slope(), self.y_intercept())

    def __repr__(self):
        return f"Line({self.a}x + {self.b}y + {self.c} = 0)"


def distance(p1, p2):
    return p1.distance_to(p2)

def midpoint(p1, p2):
    return p1.midpoint(p2)

def line_from_points(p1, p2):
    return Line.from_points(p1, p2)

def line_slope_intercept(m=None, c=None, x_const=None):
    if x_const is not None:
        return Line.vertical(x_const)
    if m is None or c is None:
        raise ValueError("Provide m and c for non-vertical line")
    return Line.from_slope_intercept(m, c)

def reflect_point_across_axes(p, axis="x"):
    axis = axis.lower()
    if axis == "x":
        return p.reflect_x()
    if axis == "y":
        return p.reflect_y()
    if axis == "origin":
        return p.reflect_origin()
    raise ValueError("axis must be 'x', 'y', or 'origin'")

def reflect_point_across_line(p, line):
    return p.reflect_across_line(line)

def vector_add(u, v):
    return u.add(v)

def vector_sub(u, v):
    return u.sub(v)

def vector_dot(u, v):
    return u.dot(v)

def vector_cross(u, v):
    return u.cross(v)

def vector_scale(u, k):
    return u.scale(k)

def vector_mag(u):
    return u.mag()

def vector_unit(u):
    return u.unit()

def vector_proj(u, v):
    return u.proj_onto(v)



