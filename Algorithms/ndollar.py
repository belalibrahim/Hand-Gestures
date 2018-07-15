from Algorithms.Shared.Utils import *
from Algorithms.Shared.Result import *


# NDollarRecognizer constants
NumPoints = 96
OneDThreshold = 0.25    # customize to desired gesture set (usually 0.20 - 0.35)
StartAngleIndex = (NumPoints / 8)   # eighth of gesture length
AngleSimilarityThreshold = Deg2Rad(30.0)


# Unistroke class: a unistroke template
class Unistroke:
    def __init__(self, name, useBoundedRotationInvariance, points):
        self.Name = name
        self.Points = Resample(points, NumPoints)
        radians = IndicativeAngle(self.Points)
        self.Points = RotateBy(self.Points, -radians)
        self.Points = ScaleTo(self.Points, SquareSize, OneDThreshold)
        if useBoundedRotationInvariance:
            self.Points = RotateBy(self.Points, +radians)
        self.Points = TranslateTo(self.Points, Origin)
        self.StartUnitVector = CalcStartUnitVector(self.Points, StartAngleIndex)
        self.Vector = Vectorize(self.Points, useBoundedRotationInvariance)


# Multistroke class: a container for unistrokes
class Multistroke:
    def __init__(self, name, useBoundedRotationInvariance, strokes):
        self.Name = name
        self.NumStrokes = len(strokes)
        order = []      # array of integer indices

        for i in range(len(strokes)):
            order.append(i)  # initialize

        orders = []  # array of integer arrays
        HeapPermute(len(strokes), order, orders)

        unistrokes = MakeUnistrokes(strokes, orders)  # returns array of point arrays
        self.Unistrokes = []  # unistrokes for this multistroke
        for j in range(0, len(unistrokes)):
            self.Unistrokes.append(Unistroke(name, useBoundedRotationInvariance, unistrokes[j]))


# NDollarRecognizer class
class NDollarRecognizer:
    def __init__(self, useBoundedRotationInvariance=False):
        # one predefined multistroke for each multistroke type
        self.Multistrokes = []
        self.Multistrokes.append(Multistroke("T", useBoundedRotationInvariance, [
            [Point(30, 7), Point(103, 7)],
            [Point(66, 7), Point(66, 87)]
        ]))
        self.Multistrokes.append(Multistroke("N", useBoundedRotationInvariance, [
            [Point(177, 92), Point(177, 2)],
            [Point(182, 1), Point(246, 95)],
            [Point(247, 87), Point(247, 1)]]))
        self.Multistrokes.append(Multistroke("D", useBoundedRotationInvariance, [
            [Point(345, 9), Point(345, 87)],
            [Point(351, 8), Point(363, 8), Point(372, 9), Point(380, 11), Point(386, 14), Point(391, 17),
             Point(394, 22), Point(397, 28), Point(399, 34), Point(400, 42), Point(400, 50), Point(400, 56),
             Point(399, 61), Point(397, 66), Point(394, 70), Point(391, 74), Point(386, 78), Point(382, 81),
             Point(377, 83), Point(372, 85), Point(367, 87), Point(360, 87), Point(355, 88), Point(349, 87)]
        ]))
        self.Multistrokes.append(Multistroke("P", useBoundedRotationInvariance, [
            [Point(507, 8), Point(507, 87)],
            [Point(513, 7), Point(528, 7), Point(537, 8), Point(544, 10), Point(550, 12), Point(555, 15),
             Point(558, 18), Point(560, 22), Point(561, 27), Point(562, 33), Point(561, 37), Point(559, 42),
             Point(556, 45), Point(550, 48), Point(544, 51), Point(538, 53), Point(532, 54), Point(525, 55),
             Point(519, 55), Point(513, 55), Point(510, 55)]
        ]))
        self.Multistrokes.append(Multistroke("X", useBoundedRotationInvariance, [
            [Point(30, 146), Point(106, 222)],
            [Point(30, 225), Point(106, 146)]
        ]))
        self.Multistrokes.append(Multistroke("H", useBoundedRotationInvariance, [
            [Point(188, 137), Point(188, 225)],
            [Point(188, 180), Point(241, 180)],
            [Point(241, 137), Point(241, 225)]
        ]))
        self.Multistrokes.append(Multistroke("I", useBoundedRotationInvariance, [
            [Point(371, 149), Point(371, 221)],
            [Point(341, 149), Point(401, 149)],
            [Point(341, 221), Point(401, 221)]
        ]))
        self.Multistrokes.append(Multistroke("exclamation", useBoundedRotationInvariance, [
            [Point(526, 142), Point(526, 204)],
            [Point(526, 221)]
        ]))
        self.Multistrokes.append(Multistroke("line", useBoundedRotationInvariance, [
            [Point(12, 347), Point(119, 347)]
        ]))
        self.Multistrokes.append(Multistroke("five-point star", useBoundedRotationInvariance, [
            [Point(177, 396), Point(223, 299), Point(262, 396), Point(168, 332), Point(278, 332), Point(184, 397)]
        ]))
        self.Multistrokes.append(Multistroke("null", useBoundedRotationInvariance, [
            [Point(382, 310), Point(377, 308), Point(373, 307), Point(366, 307), Point(360, 310), Point(356, 313),
             Point(353, 316), Point(349, 321), Point(347, 326), Point(344, 331), Point(342, 337), Point(341, 343),
             Point(341, 350), Point(341, 358), Point(342, 362), Point(344, 366), Point(347, 370), Point(351, 374),
             Point(356, 379), Point(361, 382), Point(368, 385), Point(374, 387), Point(381, 387), Point(390, 387),
             Point(397, 385), Point(404, 382), Point(408, 378), Point(412, 373), Point(416, 367), Point(418, 361),
             Point(419, 353), Point(418, 346), Point(417, 341), Point(416, 336), Point(413, 331), Point(410, 326),
             Point(404, 320), Point(400, 317), Point(393, 313), Point(392, 312)],
            [Point(418, 309), Point(337, 390)]
        ]))
        self.Multistrokes.append(Multistroke("arrowhead", useBoundedRotationInvariance, [
            [Point(506, 349), Point(574, 349)],
            [Point(525, 306), Point(584, 349), Point(525, 388)]
        ]))
        self.Multistrokes.append(Multistroke("pitchfork", useBoundedRotationInvariance, [
            [Point(38, 470), Point(36, 476), Point(36, 482), Point(37, 489), Point(39, 496), Point(42, 500),
             Point(46, 503), Point(50, 507), Point(56, 509), Point(63, 509), Point(70, 508), Point(75, 506),
             Point(79, 503), Point(82, 499), Point(85, 493), Point(87, 487), Point(88, 480), Point(88, 474),
             Point(87, 468)],
            [Point(62, 464), Point(62, 571)]
        ]))
        self.Multistrokes.append(Multistroke("six-point star", useBoundedRotationInvariance, [
            [Point(177, 554), Point(223, 476), Point(268, 554), Point(183, 554)],
            [Point(177, 490), Point(223, 568), Point(268, 490), Point(183, 490)]
        ]))
        self.Multistrokes.append(Multistroke("asterisk", useBoundedRotationInvariance, [
            [Point(325, 499), Point(417, 557)],
            [Point(417, 499), Point(325, 557)],
            [Point(371, 486), Point(371, 571)]
        ]))
        self.Multistrokes.append(Multistroke("half-note", useBoundedRotationInvariance, [
            [Point(546, 465), Point(546, 531)],
            [Point(540, 530), Point(536, 529), Point(533, 528), Point(529, 529), Point(524, 530), Point(520, 532),
             Point(515, 535), Point(511, 539), Point(508, 545), Point(506, 548), Point(506, 554), Point(509, 558),
             Point(512, 561), Point(517, 564), Point(521, 564), Point(527, 563), Point(531, 560), Point(535, 557),
             Point(538, 553), Point(542, 548), Point(544, 544), Point(546, 540), Point(546, 536)]
        ]))

    # The N$ Gesture Recognizer API begins here
    def Recognize(self, strokes, useBoundedRotationInvariance=False, requireSameNoOfStrokes=False, useProtractor=False):
        points = CombineStrokes(strokes)  # make one connected unistroke from the given strokes
        points = Resample(points, NumPoints)
        radians = IndicativeAngle(points)
        points = RotateBy(points, -radians)
        points = ScaleTo(points, SquareSize, OneDThreshold)
        if useBoundedRotationInvariance:
            points = RotateBy(points, +radians)  # restore
        points = TranslateTo(points, Origin)
        startv = CalcStartUnitVector(points, StartAngleIndex)
        vector = Vectorize(points, useBoundedRotationInvariance)  # for Protractor

        b = math.inf
        u = -1
        for i in range(len(self.Multistrokes)):  # for each multistroke
            if not requireSameNoOfStrokes or (len(strokes) == self.Multistrokes[i].NumStrokes):  # optional -- only attempt match when same # of component strokes
                for j in range(len(self.Multistrokes[i].Unistrokes)):  # each unistroke within this multistroke
                    if AngleBetweenUnitVectors(startv, self.Multistrokes[i].Unistrokes[j].StartUnitVector) <= AngleSimilarityThreshold:  # strokes start in the same direction
                        if useProtractor:  # for Protractor
                            d = OptimalCosineDistance(self.Multistrokes[i].Unistrokes[j].Vector, vector)
                        else:  # Golden Section Search (original $N)
                            d = DistanceAtBestAngle(points, self.Multistrokes[i].Unistrokes[j], -AngleRange, +AngleRange, AnglePrecision)
                        if d < b:
                            b = d  # best (least) distance
                            u = i  # multistroke owner of unistroke

        if u == -1:
            return Result("Unrecognized.", 0.0)
        else:
            if useProtractor:
                p = 1.0 / b
            else:
                p = 1.0 - b / HalfDiagonal

        return Result(self.Multistrokes[u].Name, p)

    def AddGesture(self, name, strokes, useBoundedRotationInvariance=False):
        self.Multistrokes.append(Multistroke(name, useBoundedRotationInvariance, strokes))
        num = 0
        for i in range(len(self.Multistrokes)):
            if self.Multistrokes[i].Name == name:
                num += 1

        return num


# Private helper functions from here on down
def HeapPermute(n, order,  orders):
    if n == 1:
        orders.append(order[:])     # append copy
    else:
        for i in range(n):
            HeapPermute(n - 1, order, orders)
            if n % 2 == 1:  # swap 0, n-1
                tmp = order[0]
                order[0] = order[n - 1]
                order[n - 1] = tmp
            else:   # swap i, n-1
                tmp = order[i]
                order[i] = order[n - 1]
                order[n - 1] = tmp


def MakeUnistrokes(strokes, orders):
    unistrokes = []     # array of point arrays
    for r in range(len(orders)):
        for b in range(int(math.pow(2, len(orders[r])))):    # use b's bits for directions
            unistroke = []  # array of points
            for i in range(len(orders[r])):
                if ((b >> i) & 1) == 1:  # is b's bit at index i on?
                    pts = strokes[orders[r][i]][:][::-1]   # copy and reverse
                else:
                    pts = strokes[orders[r][i]][:]    # copy
                for p in range(len(pts)):
                    unistroke.append(pts[p])  # append points

            unistrokes.append(unistroke)     # add one unistroke to set

    return unistrokes


def CombineStrokes(strokes):
    points = []
    for s in range(len(strokes)):
        for p in range(len(strokes[s])):
            points.append(Point(strokes[s][p].X, strokes[s][p].Y))

    return points


def Vectorize(points, useBoundedRotationInvariance): # for Protractor
    cos = 1.0
    sin = 0.0
    if useBoundedRotationInvariance:
        iAngle = math.atan2(points[0].Y, points[0].X)
        baseOrientation = (math.pi / 4.0) * math.floor((iAngle + math.pi / 8.0) / (math.pi / 4.0))
        cos = math.cos(baseOrientation - iAngle)
        sin = math.sin(baseOrientation - iAngle)

    sum1 = 0.0
    vector = []
    for i in range(len(points)):
        newX = points[i].X * cos - points[i].Y * sin
        newY = points[i].Y * cos + points[i].X * sin
        vector.append(newX)
        vector.append(newY)
        sum1 += newX * newX + newY * newY

    magnitude = math.sqrt(sum1)
    for i in range(len(vector)):
        vector[i] /= magnitude
    return vector


def CalcStartUnitVector(points, index):
    v = Point(points[index].X - points[0].X, points[index].Y - points[0].Y)
    len1 = math.sqrt(v.X * v.X + v.Y * v.Y)
    return Point(v.X / len1, v.Y / len1)


def AngleBetweenUnitVectors(v1, v2):  # gives acute angle between unit vectors from (0,0) to v1, and (0,0) to v2
    n = (v1.X * v2.X + v1.Y * v2.Y)
    c = max(-1.0, min(1.0, n))  # ensure [-1,+1]
    return math.acos(c)     # arc cosine of the vector dot product


