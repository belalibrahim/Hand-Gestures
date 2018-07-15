import math
from Algorithms.Shared.Point import *
from Algorithms.Shared.Rectangle import *


def Deg2Rad(d):
    return d * math.pi / 180.0


# DollarRecognizer constants
NumMultistrokes = 16
SquareSize = 250.0
Origin = Point(0, 0)
Diagonal = math.sqrt(SquareSize * SquareSize + SquareSize * SquareSize)
HalfDiagonal = 0.5 * Diagonal
AngleRange = Deg2Rad(45.0)
AnglePrecision = Deg2Rad(2.0)
Phi = 0.5 * (-1.0 + math.sqrt(5.0))


def Resample(points, n):
    I = PathLength(points) / (n - 1)    # interval length
    D = 0.0
    newpoints = [points[0]]
    for i in range(1, len(points)):
        d = Distance(points[i-1], points[i])
        if (D + d) >= I:
            qx = points[i-1].X + ((I - D) / d) * (points[i].X - points[i-1].X)
            qy = points[i-1].Y + ((I - D) / d) * (points[i].Y - points[i-1].Y)
            q = Point(qx, qy)
            newpoints.append(q)     # append new point 'q'
            points.insert(i, q)  # insert 'q' at position i in points s.t. 'q' will be the next i
            D = 0.0
        else:
            D += d

    if len(newpoints) == n - 1:     # sometimes we fall a rounding-error short of adding the last point, so add it if so
        newpoints.append(Point(points[-1].X, points[-1].Y))
    return newpoints


def IndicativeAngle(points):
    c = Centroid(points)
    return math.atan2(c.Y - points[0].Y, c.X - points[0].X)


def RotateBy(points, radians):  # rotates points around centroid
    c = Centroid(points)
    cos = math.cos(radians)
    sin = math.sin(radians)
    newpoints = []
    for i in range(len(points)):
        qx = (points[i].X - c.X) * cos - (points[i].Y - c.Y) * sin + c.X
        qy = (points[i].X - c.X) * sin + (points[i].Y - c.Y) * cos + c.Y
        newpoints.append(Point(qx, qy))

    return newpoints


def ScaleTo(points, size, ratio1D=0.0):     # scales bbox uniformly for 1D, non-uniformly for 2D
    newpoints = []
    B = BoundingBox(points)
    uniformly = (min(B.Width / B.Height, B.Height / B.Width) <= ratio1D)    # 1D or 2D gesture test
    for i in range(len(points)):
        if uniformly:
            qx = points[i].X * (size / max(B.Width, B.Height))
            qy = points[i].Y * (size / max(B.Width, B.Height))
        else:
            qx = points[i].X * (size / B.Width)
            qy = points[i].Y * (size / B.Height)
        newpoints.append(Point(qx, qy))

    return newpoints


def TranslateTo(points, pt):    # translates points' centroid
    c = Centroid(points)
    newpoints = []
    for i in range(len(points)):
        qx = points[i].X + pt.X - c.X
        qy = points[i].Y + pt.Y - c.Y
        newpoints.append(Point(qx, qy))

    return newpoints


def OptimalCosineDistance(v1, v2):  # for Protractor
    a = 0.0
    b = 0.0
    for i in range(0, len(v1), 2):
        a += v1[i] * v2[i] + v1[i+1] * v2[i+1]
        b += v1[i] * v2[i+1] - v1[i+1] * v2[i]

    angle = math.atan(b / a)
    return math.acos(a * math.cos(angle) + b * math.sin(angle))


def DistanceAtBestAngle(points, T, a, b, threshold):
    x1 = Phi * a + (1.0 - Phi) * b
    f1 = DistanceAtAngle(points, T, x1)
    x2 = (1.0 - Phi) * a + Phi * b
    f2 = DistanceAtAngle(points, T, x2)
    while abs(b - a) > threshold:
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = Phi * a + (1.0 - Phi) * b
            f1 = DistanceAtAngle(points, T, x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = (1.0 - Phi) * a + Phi * b
            f2 = DistanceAtAngle(points, T, x2)

    return min(f1, f2)


def DistanceAtAngle(points, T, radians):
    newpoints = RotateBy(points, radians)
    return PathDistance(newpoints, T.Points)


def Centroid(points):
    x = 0.0
    y = 0.0
    for i in range(0, len(points)):
        x += points[i].X
        y += points[i].Y
    x /= len(points)
    y /= len(points)
    return Point(x, y)


def BoundingBox(points):
    minX = +math.inf
    maxX = -math.inf
    minY = +math.inf
    maxY = -math.inf

    for i in range(0, len(points)):
        minX = min(minX, points[i].X)
        minY = min(minY, points[i].Y)
        maxX = max(maxX, points[i].X)
        maxY = max(maxY, points[i].Y)

    return Rectangle(minX, minY, maxX - minX, maxY - minY)


def PathDistance(pts1, pts2):   # average distance between corresponding points in two paths
    d = 0.0
    for i in range(min(len(pts1), len(pts2))):   # assumes pts1.length == pts2.length
        d += Distance(pts1[i], pts2[i])

    return d / max(len(pts1), len(pts2))


def PathLength(points):     # length traversed by a point path
    d = 0.0
    for i in range(1, len(points)):
        d += Distance(points[i-1], points[i])
    return d


def Distance(p1, p2):  # distance between two points
    dx = p2.X - p1.X
    dy = p2.Y - p1.Y
    return math.sqrt(dx * dx + dy * dy)


