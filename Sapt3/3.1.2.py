
"""
2. Model the following:
a) a Point class that has two values, x and y, representing coordinates
Add suport for the following
- addition and substraction of two points
- equality
- string representation
Make examples showcasing these capabilities

b) a PointCollection class that has a list of points
Add support for the following
- check that a point is in the collection
- len support
- comparison between two point collections (based on length)
- addition and substraction (for both Point and PointCollection)
- string representation
Make examples showcasing these capabilities

c) a Triangle class that has 3 Point objects representing the corners of the triangle
Add support for the following
- validate that the points form a valid triangle (not a line)
- equality
- string representation
- len support (based on triangle area)
- comparison between other triangles (based on triangle area)
- in support (a triangle is within another triangle, a point is in the triangle, a point collection is in a triangle)

d) a Rectangle class that has 4 Point obejcts representing the corners of the rectangle
Add support for the following
- validate that the points form a valid rectangle
- equality
- string representation
- len support (based on rectangle area)
- comparison between other rectangles (based on rectangle area)
- in support  (a rectangle is within another rectangle, a point is in the rectangle, a point collection is in a rectangle)
"""
from __future__ import annotations
import math
from numbers import Number
from functools import total_ordering
from typing import Self, Iterable
from collections.abc import Sequence

@total_ordering
class Point:
    __slots__ = ('x', 'y')

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Point) -> Self:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Self:
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Point):
            return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
        if isinstance(other, Number):
            return math.isclose(self.x, other) and math.isclose(self.y, other)
        return NotImplemented

    def __lt__(self, other: Point) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) < (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)

    def dist_sq(self, other: Point) -> float:
        return (self.x - other.x)**2 + (self.y - other.y)**2

@total_ordering
class PointCollection(Sequence):
    def __init__(self, points: Iterable[Point] | None = None) -> None:
        self._points: list[Point] = list(points) if points else []

    def __getitem__(self, index: int) -> Point:
        return self._points[index]

    def __len__(self) -> int:
        return len(self._points)

    def __contains__(self, value: object) -> bool:
        return super().__contains__(value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PointCollection):
            return NotImplemented
        return len(self) == len(other)

    def __lt__(self, other: PointCollection) -> bool:
        if not isinstance(other, PointCollection):
            return NotImplemented
        return len(self) < len(other)

    def __add__(self, other: Point | PointCollection) -> Self:
        if isinstance(other, Point):
            return self.__class__(self._points + [other])
        if isinstance(other, PointCollection):
            return self.__class__(self._points + other._points)
        return NotImplemented

    def __sub__(self, other: Point | PointCollection) -> Self:
        other_points = set([other] if isinstance(other, Point) else other)
        new_points = [p for p in self._points if p not in other_points]
        return self.__class__(new_points)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._points})"

    def __repr__(self) -> str:
        return str(self)

@total_ordering
class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point) -> None:
        self.corners: tuple[Point, Point, Point] = (p1, p2, p3)
        self._area_val = self._calculate_area()
        if math.isclose(self._area_val, 0):
            raise ValueError("Points must not be collinear.")

    def _calculate_area(self) -> float:
        p1, p2, p3 = self.corners
        return 0.5 * abs(p1.x * (p2.y - p3.y) +
                         p2.x * (p3.y - p1.y) +
                         p3.x * (p1.y - p2.y))

    @property
    def area(self) -> float:
        return self._area_val

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Triangle):
            return NotImplemented
        return set(self.corners) == set(other.corners)

    def __lt__(self, other: Triangle) -> bool:
        if not isinstance(other, Triangle):
            return NotImplemented
        return self.area < other.area

    def __contains__(self, item: object) -> bool:
        if isinstance(item, Point):
            # https://en.wikipedia.org/wiki/Barycentric_coordinate_system
            p1, p2, p3 = self.corners
            d1 = (item.x - p2.x) * (p1.y - p2.y) - (p1.x - p2.x) * (item.y - p2.y)
            d2 = (item.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (item.y - p3.y)
            d3 = (item.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (item.y - p1.y)
            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            return not (has_neg and has_pos)
        if isinstance(item, PointCollection):
            return all(p in self for p in item)
        if isinstance(item, Triangle):
            return all(corner in self for corner in item.corners)
        return False

    def __str__(self) -> str:
        return f"Triangle(p1={self.corners[0]}, p2={self.corners[1]}, p3={self.corners[2]})"

    def __repr__(self) -> str:
        return str(self)

@total_ordering
class Rectangle:
    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point) -> None:
        points = list({p1, p2, p3, p4})
        if len(points) != 4:
            raise ValueError("Rectangle requires four distinct corner points.")
        self._side1_sq, self._side2_sq = self._validate_and_get_sides_sq(points)
        self.corners = self._get_ordered_vertices(points)
        self._sorted_corner_tuples = tuple(sorted((p.x, p.y) for p in self.corners))

    @staticmethod
    def _validate_and_get_sides_sq(points: list[Point]) -> tuple[float, float]:
        # Check sides & diagonals:
        # A rectangle has 2 pairs of equal sides and 2 equal diagonals
        # The sum of squared sides must equal the squared diagonal
        dists_sq = sorted([p1.dist_sq(p2) for i, p1 in enumerate(points) for p2 in points[i+1:]])
        if (math.isclose(dists_sq[0], dists_sq[1]) and
            math.isclose(dists_sq[2], dists_sq[3]) and
            math.isclose(dists_sq[4], dists_sq[5]) and
            math.isclose(dists_sq[0] + dists_sq[2], dists_sq[4])):
            return dists_sq[0], dists_sq[2]
        raise ValueError("Points must form a valid rectangle.")

    @staticmethod
    def _get_ordered_vertices(points: list[Point]) -> tuple[Point, ...]:
        center_x = sum(p.x for p in points) / 4
        center_y = sum(p.y for p in points) / 4
        return tuple(sorted(points, key=lambda p: math.atan2(p.y - center_y, p.x - center_x)))

    @property
    def area(self) -> float:
        return math.sqrt(self._side1_sq * self._side2_sq)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self._sorted_corner_tuples == other._sorted_corner_tuples

    def __lt__(self, other: Rectangle) -> bool:
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.area < other.area

    @staticmethod
    def _cross_product(o: Point, a: Point, b: Point) -> float:
        return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

    def __contains__(self, item: object) -> bool:
        if isinstance(item, Point):

            signs = [math.copysign(1.0, self._cross_product(self.corners[i], self.corners[(i + 1) % 4], item)) for i in range(4)]
            return all(s == signs[0] for s in signs) or all(s == -signs[0] for s in signs)
        if isinstance(item, PointCollection):
            return all(p in self for p in item)
        if isinstance(item, Rectangle):
            return all(corner in self for corner in item.corners)
        return False

    def __str__(self) -> str:
        return f"Rectangle(p1={self.corners[0]}, p2={self.corners[1]}, p3={self.corners[2]}, p4={self.corners[3]})"

    def __repr__(self) -> str:
        return str(self)

# a)
print("Point usage:")
p1, p2 = Point(1, 2), Point(3, 4)
print(f"p1 = {p1}, p2 = {p2}")
print(f"p1 + p2: {p1 + p2}")
print(f"p2 - p1: {p2 - p1}")
print(f"p1 == Point(1, 2): {p1 == Point(1, 2)}")
print(f"p1 > p2: {p1 > p2}")
print()

# b)
print("PointCollection usage:")
pc1 = PointCollection([Point(1, 1), Point(2, 2)])
pc2 = PointCollection([Point(3, 3), Point(4, 4)])
print(f"Point(1, 1) in pc1: {Point(1, 1) in pc1}")
print(f"len(pc1): {len(pc1)}")
print(f"pc1 >= pc2: {pc1 >= pc2}")
print(f"pc1 + Point(0, 0): {pc1 + Point(0, 0)}")
print(f"(pc1 + pc2) - pc1: {(pc1 + pc2) - pc1}")
print()

# c)
print("Triangle usage:")
triangle1 = Triangle(Point(0, 0), Point(4, 0), Point(2, 3))
print(f"triangle1: {triangle1}")
try:
    Triangle(Point(0, 0), Point(1, 1), Point(2, 2))
except ValueError as e:
    print(f"Invalid triangle caught: {e}")
triangle2 = Triangle(Point(0, 0), Point(5, 0), Point(2.5, 4))
print(f"triangle1 < triangle2 (by area): {triangle1 < triangle2}")
print(f"Point(2, 1) in triangle1: {Point(2, 1) in triangle1}")
print(f"PointCollection([Point(1,1)]) in triangle1: {PointCollection([Point(1,1)]) in triangle1}")
print()

# d)
print("Rectangle usage:")
rect1 = Rectangle(Point(0,0), Point(1,1), Point(2,0), Point(1,-1))
print(f"rect1 (rotated): {rect1}")
print()
try:
    Rectangle(Point(0,0), Point(5,0), Point(6,2), Point(1,2))
except ValueError as e:
    print(f"Invalid rectangle caught: {e}")
rect2 = Rectangle(Point(0,0), Point(6,0), Point(6,4), Point(0,4))
print(f"rect1 < rect2 (by area): {rect1 < rect2}")

print(f"Point(1, 0) in rect1: {Point(1, 0) in rect1}")
print(f"Point(0.1, 0.9) in rect1: {Point(0.1, 0.9) in rect1}")

pc_in = PointCollection([Point(1, 0.5), Point(1.5, 0), Point(0.5, 0)])
print(f"{pc_in} in rect1: {pc_in in rect1}")

