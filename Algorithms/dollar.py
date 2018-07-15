from Algorithms.Shared.Utils import *
from Algorithms.Shared.Result import *


# 1DollarRecognizer constants
NumPoints = 64


# Unistroke class: a unistroke template
class Unistroke:
    def __init__(self, name, points):
        self.Name = name
        self.Points = Resample(points, NumPoints)
        radians = IndicativeAngle(self.Points)
        self.Points = RotateBy(self.Points, -radians)
        self.Points = ScaleTo(self.Points, SquareSize)
        self.Points = TranslateTo(self.Points, Origin)
        self.Vector = Vectorize(self.Points)  # for Protractor


# 1DollarRecognizer class
class DollarRecognizer:
    def __init__(self):  # constructor
        self.Unistrokes = []

    # The 1$ Gesture Recognizer API begins here
    def Recognize(self, points, useProtractor=False):
        points = Resample(points, NumPoints)
        radians = IndicativeAngle(points)
        points = RotateBy(points, -radians)
        points = ScaleTo(points, SquareSize)
        points = TranslateTo(points, Origin)
        vector = Vectorize(points)

        b = math.inf
        u = -1
        for i in range(len(self.Unistrokes)):   # for each unistroke
            if useProtractor:    # for Protractor
                d = OptimalCosineDistance(self.Unistrokes[i].Vector, vector)
            else:   # Golden Section Search (original $1)
                d = DistanceAtBestAngle(points, self.Unistrokes[i], -AngleRange, +AngleRange, AnglePrecision)
            if d < b:
                b = d    # best (least) distance
                u = i    # unistroke index

        if u == -1:
            return Result("Unrecognized.", 0.0)
        else:
            if useProtractor:
                p = 1.0 / b
            else:
                p = 1.0 - b / HalfDiagonal

        return Result(self.Unistrokes[u].Name, p)

    def AddGesture(self, name, points):
        self.Unistrokes.append(Unistroke(name, points))  # append new unistroke
        num = 0
        for i in range(len(self.Unistrokes)):
            if self.Unistrokes[i].Name == name:
                num += 1
        return num


def Vectorize(points):  # for Protractor
    sum1 = 0.0
    vector = []
    for i in range(len(points)):
        vector.append(points[i].X)
        vector.append(points[i].Y)
        sum1 += points[i].X * points[i].X + points[i].Y * points[i].Y

    magnitude = math.sqrt(sum1)
    for i in range(len(vector)):
        vector[i] /= magnitude
    return vector
